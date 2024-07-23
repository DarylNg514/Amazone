from django.shortcuts import render, redirect,get_object_or_404
from .form import *
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator



# Create your views here.
def inscription(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('connexion')
    else:
        form = CustomUserCreationForm()
    return render(request, 'inscription.html', {'form': form})

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('acceuil')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    return render(request, 'connexion.html')


def acceuil(request):
    return render(request, 'acceuil.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')

@login_required
def modifier_compte(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserChangeFormClient(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre compte a été mis à jour avec succès.')
            return redirect('acceuil')
    else:
        form = CustomUserChangeFormClient(instance=user)
    return render(request, 'modifier_compte.html', {'form': form})

@login_required
def modifier_mot_de_passe(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(request.POST, user=user)
        if form.is_valid():
            user.set_password(form.cleaned_data.get('new_password1'))
            user.save()
            messages.success(request, 'Votre mot de passe a été mis à jour avec succès.')
            return redirect('acceuil')
    else:
        form = PasswordChangeForm(user=user)
    return render(request, 'modifier_mot_de_passe.html', {'form': form})

@login_required
def supprimer_compte(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Votre compte a été supprimé avec succès.')
        return redirect('inscription')
    return render(request, 'supprimer_compte.html')


# List all users
@login_required
def list_users(request):
    users = CustomUser.objects.all()
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'list_users.html', {'page_obj': page_obj})

# Update a user
@login_required
def update_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('list_users')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'update_user.html', {'form': form})

# Delete a user
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('list_users')
    return render(request, 'delete_user.html', {'user': user})


def send_email_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        # Envoyer l'e-mail
        send_mail(
            f'Message from {name}',
            f'From: {name} <{email}>\n\n{message}',
            settings.EMAIL_HOST_USER,  # Votre adresse e-mail (optionnelle)
            [''],  # Destinataire(s)
            fail_silently=False,
        )
        return HttpResponseRedirect('/thank-you/')  # Rediriger vers une page de remerciement par exemple

    return render(request, 'your_template.html')  # Remplacez 'your_template.html' par le nom de votre template

