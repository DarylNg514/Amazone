# shop/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Produit, Categorie, Auteur
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import ProduitForm, CategorieForm, AuteurForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required



def liste_produits(request):
    categorie_id = request.GET.get('categorie')
    if categorie_id:
        produits = Produit.objects.filter(categorie_id=categorie_id)
    else:
        produits = Produit.objects.all()
    
    paginator = Paginator(produits, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Categorie.objects.all()
    
    return render(request, 'liste_produits.html', {'categories': categories, 'page_obj': page_obj, 'categorie_id': categorie_id})

def recherche_produits(request):
    query = request.GET.get('q')
    if query:
        produits = Produit.objects.filter(
            Q(nom__icontains=query) |
            Q(auteurs__nom__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
    else:
        produits = []

    paginator = Paginator(produits, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'recherche_produits.html', {'page_obj': page_obj, 'query': query})

@login_required
def produits(request):
    if request.path == '/produits/':
        produits = Produit.objects.all()
        paginator = Paginator(produits, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'produits.html', {'page_obj': page_obj})

@login_required
def get_auteurs_by_categorie(request):
    categorie_id = request.GET.get('categorie_id')
    auteurs = Auteur.objects.filter(categorie_id=categorie_id).values_list('id', 'nom')
    return JsonResponse(dict(auteurs), safe=False)

@login_required
def creer_produit(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('produits')
    else:
        form = ProduitForm()
    return render(request, 'creer_produit.html', {'form': form})

@login_required
def modifier_produit(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=produit)
        if form.is_valid():
            form.save()
            return redirect('produits')
    else:
        form = ProduitForm(instance=produit)
    return render(request, 'modifier_produit.html', {'form': form, 'produit': produit})

@login_required
def supprimer_produit(request, produit_id):
    produit = get_object_or_404(Produit, pk=produit_id)
    if request.method == 'POST':
        produit.delete()
        return redirect('produits')
    return render(request, 'supprimer_produit.html', {'produit': produit})

@login_required
def liste_categories(request):
    categories = Categorie.objects.all()
    paginator = Paginator(categories, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'liste_categories.html', {'page_obj': page_obj})

@login_required
def creer_categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_categories')
    else:
        form = CategorieForm()
    return render(request, 'creer_categorie.html', {'form': form})

@login_required
def modifier_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, pk=categorie_id)
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=categorie)
        if form.is_valid():
            form.save()
            return redirect('liste_categories')
    else:
        form = CategorieForm(instance=categorie)
    return render(request, 'modifier_categorie.html', {'form': form, 'categorie': categorie})

@login_required
def supprimer_categorie(request, categorie_id):
    categorie = get_object_or_404(Categorie, pk=categorie_id)
    if request.method == 'POST':
        categorie.delete()
        return redirect('liste_categories')
    return render(request, 'supprimer_categorie.html', {'categorie': categorie})

@login_required
def liste_auteurs(request):
    auteurs = Auteur.objects.all()
    paginator = Paginator(auteurs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'liste_auteurs.html', {'page_obj': page_obj})

@login_required
def creer_auteur(request):
    if request.method == 'POST':
        form = AuteurForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_auteurs')
    else:
        form = AuteurForm()
    return render(request, 'creer_auteur.html', {'form': form})

@login_required
def modifier_auteur(request, auteur_id):
    auteur = get_object_or_404(Auteur, pk=auteur_id)
    if request.method == 'POST':
        form = AuteurForm(request.POST, instance=auteur)
        if form.is_valid():
            form.save()
            return redirect('liste_auteurs')
    else:
        form = AuteurForm(instance=auteur)
    return render(request, 'modifier_auteur.html', {'form': form, 'auteur': auteur})

@login_required
def supprimer_auteur(request, auteur_id):
    auteur = get_object_or_404(Auteur, pk=auteur_id)
    if request.method == 'POST':
        auteur.delete()
        return redirect('liste_auteurs')
    return render(request, 'supprimer_auteur.html', {'auteur': auteur})