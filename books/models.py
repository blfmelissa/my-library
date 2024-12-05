from django.db import models
from django.contrib.auth.models import User  # On utilise le modèle User par défaut de Django
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions

# Modèle de livre
class Book(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.CharField(max_length=255)
    genre = models.CharField(max_length=50)
    synopsis = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=1, db_column='added_by')  
    couverture = models.ImageField(upload_to='covers/', null=True, blank=True)

    def delete(self, *args, **kwargs):
        # Supprimer la couverture de l'Azure Blob Storage
        if self.couverture:
            self.couverture.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        db_table = 'books'

    def __str__(self):
        return self.titre
    
    def average_rating(self):
        ratings = self.ratings.all()  
        if ratings.exists():
            return ratings.aggregate(models.Avg('score'))['score__avg'] 
        return 0  # Si aucune note, renvoie 0

class Rating(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ratings")
    score = models.PositiveIntegerField(null=False, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('book', 'user')

# Modèle de recommandation
class Recommandation(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations_sent')
    recommendee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations_received')
    id_livre = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_recommendation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recommandations'
        constraints = [
            models.UniqueConstraint(fields=['id_user', 'id_livre', 'recommendee'], name='unique_recommendation')
        ]

    def clean(self) : 
        cleaned_data = super().clean()
        id_user = self.initial['id_user']
        id_livre = cleaned_data.get('id_livre')
        recommendee = cleaned_data.get('recommendee')

        # Vérifier l'existence de la recommandation
        if Recommandation.objects.filter(id_user=id_user, id_livre=id_livre, recommendee=recommendee).exists():
            raise forms.ValidationError("Vous avez déjà recommandé ce livre à cet utilisateur.")
        return cleaned_data
