
from mysite import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .token import generatoToken

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage

# Create your views here.
def home(request):
    return render(request, 'app/index.html')

def register(request):
    if request.method =='POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password1 = request.POST['password1']
        if User.objects.filter(username=username):
            messages.error(request, 'ce nom a deja ete pris')
            return redirect('register')
        if User.objects.filter(email=email):
            messages.error(request, 'cet email a deja un compte')
            return redirect('register')
        if not username.isalnum():
            messages.error(request, 'Le nom doit etre alphanumeric')
            return redirect('register')
        if password != password1:
            messages.error(request, 'les deux password ne correspond pas')
            return redirect('register')
        
        nom_utilisateur = User.objects.create_user(username, email, password)
        nom_utilisateur.first_name = firstname
        nom_utilisateur.last_name = lastname
        nom_utilisateur.is_active = False
        nom_utilisateur.save()
        messages.success(request, "votre compte a ete creer avec success")
        
        # envoi d'email de bienvenu
        
        subject = "Bienvenu sur donfack pro django system login"
        message =  "Bienvenu " + nom_utilisateur.first_name + " " + nom_utilisateur.last_name + "\n Nous somme heureux de vous compte parmi nous\n\n\n Merci \n\n donfack programmeur"
        from_email = settings.EMAIL_HOST_USER
        to_list = [nom_utilisateur.email]
        send_mail(subject, message, from_email, to_list, fail_silently=False)
        
        #email de comfirmation
        current_site = get_current_site(request)
        email_subject = "Confirmation de l'adress email sur donfack pro"
        messageConfirm = render_to_string("emailconfirm.html", {
            "name": nom_utilisateur.first_name,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(nom_utilisateur.pk)),
            "token": generatoToken.make_token(nom_utilisateur)
        })
        email = EmailMessage(
            email_subject,
            messageConfirm,
            settings.EMAIL_HOST_USER,
            [nom_utilisateur.email]
        )
        email.fail_silently = False
        email.send()
        
        return redirect('login')
    
    return render(request, 'app/register.html')

def logIn(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        my_user = User.objects.get(username=username)
        if user is not None:
            login(request, user)
            firstname = user.first_name
            return render(request, 'app/index.html', context={"firstname": firstname})
        
        elif my_user.is_active == False:
            messages.error(request, "vous n'avez pas confirmer votre address email faut le avans de vous connecter merci!")
                        
        else:
            messages.error(request, 'mauvaise authentification')
            return redirect('login')
    return render(request, 'app/login.html')

def lOgout(request):
    logout(request)
    messages.success(request, 'vous avez ete bien deconnecter')
    return redirect('home')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and generatoToken.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'votre compte a ete activer felicitation connectez vous maintenant')
        return redirect('login')
    else:
        messages.error(request, 'activation echoue!!!')
        return redirect('home')