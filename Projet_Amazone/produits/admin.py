# shop/admin.py

from django.contrib import admin
from .models import Categorie, Auteur, Produit

admin.site.register(Categorie)
admin.site.register(Auteur)
admin.site.register(Produit)
