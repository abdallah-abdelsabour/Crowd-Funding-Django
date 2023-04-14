from django.shortcuts import render ,redirect
from django.http import HttpResponse
from .forms import UserForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from django.contrib.auth.models import User

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('home')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('home')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activation_user.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')






# abdallah
@user_not_authenticated
def signup(request):

    # get form handle
    if request.method == "GET":
        form = UserForm()
        return render(request, "user/signup.html" ,{'form':form})
    

# post validate and registrion login  
    if request.method =="POST":
        form  = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('profile_page')
        
        # not vlalid trquest
        return render(request, "user/signup.html" ,{'form':form})

# youssef
def login(request):
    pass
# get 
# return login form 

# post 
# handle login form 


@login_required
def update(request):
    pass
#    user  = User.objects.filter(username=request.user.username)
#    print( user)
#    if user :
#     form =UserForm(instance=user)
    

       



# karem
def delete_account(request):
    pass
# delete accoutt



def profile_page(request):

    return render (request , "user/profile.html",{'user':request.user})