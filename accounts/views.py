from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from chats.models import UserProfile


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    template_name = 'accounts/login.html'


class LogoutUser(LogoutView):
    next_page = reverse_lazy('login')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, name=instance.username)
    instance.profile.save()
