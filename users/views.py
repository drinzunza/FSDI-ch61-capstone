from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import SignupForm

# Create your views here.
class SignupView(CreateView):
    model = User
    form_class = SignupForm
    template_name = "users/signup.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        # change the way the data is validated before is saved
        user = form.save(commit=False)
        text = form.cleaned_data["password"]
        user.set_password(text) # <- will hash the text
        user.save()

        if user.email:
            send_mail(
                subject="Welcome to Notespace",
                message=(
                    f"Hi {user.first_name or user.username},\n\n"
                    "Welcome to Notespace! You're all set to capture ideas, organize notes, and share updates.\n\n"
                    "If you have any questions, just reply to this email.\n\n"
                    "Thanks,\n"
                    "The Notespace Team"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )

        return super().form_valid(form)
    

class UserLoginView(LoginView):
    template_name = "users/login.html"  

class UserLogoutView(LogoutView):
    next_page = reverse_lazy("login")
