from django.core.files.storage import Storage
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from django.conf import settings
from io import BytesIO

class AzureStorage(Storage):
    def __init__(self, *args, **kwargs):
        # Connexion au service Azure Blob Storage
        self.blob_service_client = BlobServiceClient(account_url=f"https://{settings.AZURE_ACCOUNT_NAME}.blob.core.windows.net", credential=settings.AZURE_ACCOUNT_KEY)
        self.container_client = self.blob_service_client.get_container_client('book-covers')

    def _open(self, name, mode='rb'):
        # Ouvrir un fichier existant (en lecture)
        blob_client = self.container_client.get_blob_client(name)
        stream = BytesIO()
        blob_client.download_blob().readinto(stream)
        stream.seek(0)
        return stream

    def _save(self, name, content):
        # Sauvegarder un fichier (en écriture)
        blob_client = self.container_client.get_blob_client(name)
        blob_client.upload_blob(content, overwrite=True)
        return name

    def delete(self, name):
        # Supprimer un fichier
        blob_client = self.container_client.get_blob_client(name)
        blob_client.delete_blob()

    def exists(self, name):
        # Vérifier si le fichier existe déjà
        blob_client = self.container_client.get_blob_client(name)
        try:
            blob_client.get_blob_properties()
            return True
        except:
            return False

    def url(self, name):
        # Retourner l'URL d'accès direct au fichier
        return f"{settings.AZURE_URL}{name}"
