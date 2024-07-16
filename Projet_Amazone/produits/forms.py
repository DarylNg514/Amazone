# shop/forms.py
'''
from django import forms
from .models import Produit, Categorie, Auteur


class ProduitForm(forms.ModelForm):
    categorie = forms.ModelChoiceField(queryset=Categorie.objects.all(), empty_label="Sélectionnez une catégorie")
    auteurs = forms.ModelMultipleChoiceField(queryset=Auteur.objects.none(), required=False)

    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'image','quantite', 'categorie', 'auteurs']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True
        if 'categorie' in self.data:
            try:
                categorie_id = int(self.data.get('categorie'))
                self.fields['auteurs'].queryset = Auteur.objects.filter(categorie_id=categorie_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['auteurs'].queryset = self.instance.categorie.auteur_set.all()
            
class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom']

class AuteurForm(forms.ModelForm):
    categorie = forms.ModelChoiceField(queryset=Categorie.objects.all(), empty_label=None)

    class Meta:
        model = Auteur
        fields = ['nom', 'categorie']
'''


from django import forms
from .models import Produit, Categorie, Auteur

class ProduitForm(forms.ModelForm):
    categorie = forms.ModelChoiceField(queryset=Categorie.objects.all(), empty_label="Sélectionnez une catégorie")
    auteurs = forms.ModelMultipleChoiceField(queryset=Auteur.objects.none(), required=False)

    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'image', 'quantite', 'categorie', 'auteurs']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
        if 'categorie' in self.data:
            try:
                categorie_id = int(self.data.get('categorie'))
                self.fields['auteurs'].queryset = Auteur.objects.filter(categorie_id=categorie_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['auteurs'].queryset = self.instance.categorie.auteur_set.all()
            
class CategorieForm(forms.ModelForm):
    class Meta:
        model = Categorie
        fields = ['nom']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True

class AuteurForm(forms.ModelForm):
    categorie = forms.ModelChoiceField(queryset=Categorie.objects.all(), empty_label=None)

    class Meta:
        model = Auteur
        fields = ['nom', 'categorie']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
