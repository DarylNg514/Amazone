# shop/models.py

from django.db import models

class Categorie(models.Model):
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom

class Auteur(models.Model):
    nom = models.CharField(max_length=255)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom

class Produit(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    auteurs = models.ManyToManyField(Auteur)
    image = models.ImageField(upload_to='produits/', blank=True, null=True)
    quantite = models.PositiveIntegerField(default=1)


    def __str__(self):
        return self.nom
