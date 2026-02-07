from django.shortcuts import render
from django.core.mail import send_mail


# Create your views here.

def home_view(request):
    return render(request, 'pages/home.html')



def about_view(request):
    return render(request, "pages/about.html")


def contact_view(request):    
    return render(request, "pages/contact.html", {'form': 1})
