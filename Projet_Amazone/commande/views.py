from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required
from produits.models import Produit
from django.core.paginator import Paginator
from .models import *

def ajouter_au_panier(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    panier = request.session.get('panier', {})

    if request.method == 'POST':
        quantite = int(request.POST.get('quantite', 1))
        if str(produit_id) in panier:
            panier[str(produit_id)]['quantite'] += quantite
        else:
            panier[str(produit_id)] = {
                'nom': produit.nom,
                'prix': float(produit.prix),
                'quantite': quantite,
                'image': produit.image.url if produit.image else None
            }

        request.session['panier'] = panier
        return JsonResponse({'message': 'Produit ajouté au panier'}, status=200)

    return redirect('liste_produits')

def voir_panier(request):
    panier = request.session.get('panier', {})
    total = round(sum(item['prix'] * item['quantite'] for item in panier.values()), 2)
    return render(request, 'panier.html', {'panier': panier, 'total': total})

def supprimer_du_panier(request, produit_id):
    panier = request.session.get('panier', {})
    if str(produit_id) in panier:
        del panier[str(produit_id)]
        request.session['panier'] = panier
    return redirect('voir_panier')

def modifier_quantite(request, produit_id):
    if request.method == 'POST':
        panier = request.session.get('panier', {})
        nouvelle_quantite = int(request.POST.get('quantite', 1))
        if str(produit_id) in panier:
            if nouvelle_quantite > 0:
                panier[str(produit_id)]['quantite'] = nouvelle_quantite
            else:
                del panier[str(produit_id)]

        request.session['panier'] = panier
        return redirect('voir_panier')

    return redirect('voir_panier')

@login_required
def payer(request):
    if request.method == 'POST':
        produit_id = request.POST.get('produit_id')
        quantite = int(request.POST.get('quantite', 1))
        produit = get_object_or_404(Produit, id=produit_id)
        total = produit.prix * quantite

        context = {
            'produit': produit,
            'quantite': quantite,
            'total': format(total, '.2f') 
        }

        return render(request, 'payer.html', context)

@login_required
def paiement_succes(request):
    panier = request.session.get('panier', {})
    if not panier:
        return redirect('voir_panier')  # Rediriger si le panier est vide

    total = sum(item['prix'] * item['quantite'] for item in panier.values())
    commande = Commande.objects.create(utilisateur=request.user, total=total)

    for produit_id, details in panier.items():
        produit = get_object_or_404(Produit, id=produit_id)
        CommandeProduit.objects.create(commande=commande, produit=produit, quantite=details['quantite'])

    # Vider le panier après la création de la commande
   # request.session['panier'] = {}

    return render(request, 'success.html', {'username': request.user.username, 'commande': commande})


@login_required
def payer_tout(request):
    panier = request.session.get('panier', {})
    total = sum(item['prix'] * item['quantite'] for item in panier.values())
    quantite_totale = sum(item['quantite'] for item in panier.values())

    context = {
        'panier': panier,
        'total': format(total, '.2f'),
        'quantite_totale': quantite_totale
    }

    return render(request, 'payer_tout.html', context)

def vider_panier(request):
    if request.method == 'POST':
        request.session['panier'] = {}
    return redirect('voir_panier')

@login_required
def liste_Commandes(request):
    commandes_list = Commande.objects.all()
    paginator = Paginator(commandes_list, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'liste_commandes.html', {'page_obj': page_obj})

@login_required
def supprimer_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id, utilisateur=request.user)
    if request.method == 'POST':
        commande.delete()
        return redirect('liste_Commandes')
    return render(request, 'supprimer_commande.html', {'commande': commande})