from django.contrib import admin
from django.urls import path
from auth_app import views
from produits import views as vs
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('inscription', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('', views.acceuil, name='acceuil'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('modifier_compte/', views.modifier_compte, name='modifier_compte'),
    path('modifier_mot_de_passe/', views.modifier_mot_de_passe, name='modifier_mot_de_passe'),
    path('supprimer_compte/', views.supprimer_compte, name='supprimer_compte'),
    path('list/', views.list_users, name='list_users'),
    path('update/<int:user_id>/', views.update_user, name='update_user'),
    path('delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('send-email/', views.send_email_view, name='send_email'),

    path('produit/', vs.liste_produits, name='liste_produits'),
    path('recherche/', vs.recherche_produits, name='recherche_produits'),

     # Produits
    path('produits/', vs.produits, name='produits'),
    path('get-auteurs-by-categorie/', vs.get_auteurs_by_categorie, name='get_auteurs_by_categorie'),
    path('produits/creer/', vs.creer_produit, name='creer_produit'),
    path('produits/modifier/<int:produit_id>/', vs.modifier_produit, name='modifier_produit'),
    path('produits/supprimer/<int:produit_id>/', vs.supprimer_produit, name='supprimer_produit'),

    # Catégories
    path('categories/', vs.liste_categories, name='liste_categories'),
    path('categories/creer/', vs.creer_categorie, name='creer_categorie'),
    path('categories/modifier/<int:categorie_id>/', vs.modifier_categorie, name='modifier_categorie'),
    path('categories/supprimer/<int:categorie_id>/', vs.supprimer_categorie, name='supprimer_categorie'),

    # Auteurs
    path('auteurs/', vs.liste_auteurs, name='liste_auteurs'),
    path('auteurs/creer/', vs.creer_auteur, name='creer_auteur'),
    path('auteurs/modifier/<int:auteur_id>/', vs.modifier_auteur, name='modifier_auteur'),
    path('auteurs/supprimer/<int:auteur_id>/', vs.supprimer_auteur, name='supprimer_auteur'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)