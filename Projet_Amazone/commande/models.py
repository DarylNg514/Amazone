from django.db import models
from auth_app.models import CustomUser
from produits.models import Produit
class Commande(models.Model):
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    produits = models.ManyToManyField(Produit, through='CommandeProduit')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Commande {self.id} de {self.utilisateur.username}'

class CommandeProduit(models.Model):
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.produit.nom} (x{self.quantite})'
