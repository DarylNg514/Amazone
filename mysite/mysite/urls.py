from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('', views.home, name='home'),
]
