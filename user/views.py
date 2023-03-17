#----------------------- Imports------------------------------------------
from user.forms import UserForm,ProfileForm
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.shortcuts import render, redirect 
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from .forms import UpdateUserForm, UpdateProfileForm
from django.contrib import messages
from projects.models import Project,Donation
from django.db.models import Sum
from django.utils.encoding import force_bytes, force_str



#------------------------------------------------------------------------
# views.functions
#-----------------------------------------------------------------------
# ________________________________
# email 
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
        return redirect('profile')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('profile')

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


# ___________________




def index(request):
    return render(request,'Users/index.html') 
#------------------------------------------------------------------------
@login_required
def special(request):
    return HttpResponse("You are logged in !")

#-------------------------------------------------------------------------

def users_register(request):
    if request.user.is_authenticated:
        return redirect('/user/profile/')
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = ProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            # set to false to prevent users from login without confirming email
            user.is_active = False
            user.save()

            print()
            activateEmail(request, user, user_form.cleaned_data.get('email'))
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request,'Users/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

#-----------------------------------------------------------------

def users_login(request):
    if request.user.is_authenticated:
        messages.success="you already logged in "
        return redirect('/user/profile/')
    # toDo@ add make message here 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # messages.error(request, "Error.  not sent.")
        try:
           user = authenticate(username=User.objects.get(email=username) ,password=password)
        except :
            user =None 
            print("user exception happend")  
            messages.error(request, "Error.  not user fount try create account .")
        print(user)
        if user is not None:
            print("user: " ,user)
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/user/profile/')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponseRedirect('/user/register/')
    else:
        return render(request, 'Users/login.html', {})



# login here 
@login_required(login_url='/user/login/')
def user_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form =UpdateProfileForm(request.POST,
                                        request.FILES,
                                        instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"Your account has been updated!")
            return redirect('/user/profile/')
    else :
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request,'Users/profile.html',context)



# get donation 
@login_required()
def my_donations(request):
    user = request.user
    donations = Donation.objects.values('project')\
        .annotate(total_donation=Sum('amount'))\
        .filter(user=user)
    donation_list = []
    for donate in donations:
        title = Project.objects.filter(id=donate['project']).first()
        donation_list.append({
            'id':donate['project'],
            'title':title,
            'donation':donate['total_donation']
        })
    context = {
        'donations' : donation_list
    }
    return render(request, 'Users/my_donations.html', context)



# get projects 
@login_required()
def my_projects(request):
    user = request.user
    projects = Project.objects.filter(user_id=user)
    context = {
        'projects' : projects
    }
    return render(request, 'Users/my_projects.html',context)
@login_required()
def delete_account(request):
    user = request.user.id
    if request.method == 'POST':
        User.objects.filter(id=user).delete()
        return redirect('/user/login/')
    else :
        return render(request, 'Users/confirm_delete.html')
#--------------------------------------------------------------------------------
def users_logout(request):
    request.session.flush()
    return render(request, 'Users/login.html')



# @login_required
# def password_change(request):
#     user = request.user
#     if request.method == 'POST':
#         form = SetPasswordForm(user, request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Your password has been changed")
#             return redirect('login')
#         else:
#             for error in list(form.errors.values()):
#                 messages.error(request, error)

#     form = SetPasswordForm(user)
#     return render(request, 'password_reset_confirm.html', {'form': form})