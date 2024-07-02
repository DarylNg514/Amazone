from django.contrib import admin
from django.urls import path
from auth_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inscription', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
    path('', views.acceuil, name='acceuil'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('modifier_compte/', views.modifier_compte, name='modifier_compte'),
    path('modifier_mot_de_passe/', views.modifier_mot_de_passe, name='modifier_mot_de_passe'),
    path('supprimer_compte/', views.supprimer_compte, name='supprimer_compte'),
    path('send-email/', views.send_email_view, name='send_email'),

]