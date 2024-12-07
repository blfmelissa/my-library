from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Book, Recommandation, Rating
from .forms import BookForm, UserForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Avg

def unlogin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('catalogue')  
        return view_func(request, *args, **kwargs)
    return wrapper

# Page d'accueil
@unlogin_required
def home(request):
    return render(request, 'books/home.html')

# Page d'inscription
@unlogin_required
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalogue') 
        elif 'username' in form.errors:
            messages.error(request, "Le nom d'utilisateur est déjà utilisé.")
        else :
            messages.error(request, "Les mots de passe ne correspondent pas.")
        return render(request, 'registration/register.html', {'form': form})
    else:
        form = UserForm()
    return render(request, 'registration/register.html', {'form': form})

# Page de connexion
@unlogin_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('catalogue')  
        else:
            return render(request, 'registration/login.html', {'error': 'Identifiants incorrects'})
    return render(request, 'registration/login.html')

# Déconnexion
def logout_view(request):
    logout(request)
    return redirect('home')  

# Catalogue des livres
@login_required
def catalogue(request):
    books = Book.objects.select_related('added_by').order_by('titre')  
    paginator = Paginator(books, 5)  
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)

    if request.method == 'POST':
        book_id = request.POST.get('book_id')  
        book = get_object_or_404(Book, id=book_id)
        score = request.POST.get('score')

        if not score or not score.isdigit() or int(score) < 1 or int(score) > 5:
            return JsonResponse({'error': 'Invalid score provided'}, status=400)

        score = int(score)
        rating, created = Rating.objects.get_or_create(user=request.user, book=book)
        rating.score = score
        rating.save()

        avg_rating = Rating.objects.filter(book=book).aggregate(Avg('score'))['score__avg'] or 0
        return JsonResponse({'average_rating': avg_rating})

    for book in page_obj:
        if book.couverture:
            book.cover_image_url = f"{settings.MEDIA_URL}{book.couverture.name}"
        else:
            book.cover_image_url = None

    return render(request, 'books/catalogue.html', {'page_obj': page_obj, 'numbers': range(1, 6)})


# Ajouter un livre
@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.added_by = request.user  
            book.save()  
            messages.success(request, f"Le livre \"{book.titre}\" a bien été ajouté au catalogue !")
            return redirect('catalogue')  
    else:
        form = BookForm()

    return render(request, 'books/add_book.html', {'form': form})

# Recommander un livre à un autre utilisateur
@login_required
def recommend(request, book_id):
    book = get_object_or_404(Book, id=book_id) 
    
    if request.method == 'POST':
        recommendee_username = request.POST.get('username')  

        try:
            recommendee = User.objects.get(username=recommendee_username)
        except User.DoesNotExist:
            messages.error(request, f"L'utilisateur '{recommendee_username}' n'existe pas.")
            return redirect('recommend', book_id=book_id)
        
        if Recommandation.objects.filter(id_user=request.user, id_livre=book, recommendee=recommendee).exists():
            messages.error(request, f"Vous avez déjà recommandé '{book.titre}' à {recommendee_username}.")
            return redirect('recommend', book_id=book_id)

        try:
            Recommandation.objects.create(
                id_user=request.user,
                id_livre=book,
                recommendee=recommendee
            )
            messages.success(request, f"Le livre '{book.titre}' a été recommandé à {recommendee_username} !")
            return redirect('recommend', book_id=book_id)
        except IntegrityError:
            messages.error(request, "Une erreur est survenue lors de l'enregistrement de la recommandation.")
            return redirect('recommend', book_id=book_id)

    return render(request, 'books/recommend.html', {'book': book})

@login_required
def recommended_books(request):
    recommandations = Recommandation.objects.filter(recommendee=request.user).select_related('id_livre', 'id_user')
    
    # Créer une liste avec les livres et l'utilisateur qui a recommandé chaque livre
    recommended_books = []
    for recommandation in recommandations:
        recommended_books.append({
            'book': recommandation.id_livre,  
            'recommender': recommandation.id_user.username,
            'date': recommandation.date_recommendation
        })
        
    return render(request, 'books/recommended_books.html', {'recommended_books': recommended_books})

@login_required
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.added_by != request.user:
        return HttpResponseForbidden("Vous n'avez pas la permission de supprimer ce livre.")
    
    book.delete()
    return redirect('catalogue') 

