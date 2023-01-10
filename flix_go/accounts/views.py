from django.shortcuts import render
from email import message
from email.message import EmailMessage
from email.policy import default
from django.shortcuts import render,redirect,HttpResponse
from accounts.models import Account
from .forms import RegistrationForm
from django.contrib import messages,auth
from django.contrib .auth.decorators import login_required

#verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django .core.mail import EmailMessage

import requests

def register(request):
    if request.method ==  'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
        # database registration  process
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_number=form.cleaned_data['phone_number']
            password=form.cleaned_data['password']
            username = email.split('@')[0]
            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email, username = username ,password=password)
            user.phone_number =phone_number
            user.save()
            # user activation
            current_site = get_current_site(request)
            mail_subject = 'Please activate Urlinfotech account'
            message = render_to_string('accounts/account_verification_email.html',{
                'user':user, 
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            # success mesage
            messages.success(request,'Thank you for registring with us. please check your Email  and verify account.')
            return redirect('/login/?command=verification&email='+email)
    else:
        
        form = RegistrationForm()
    context = {
            'form': form,
        }
    return render(request,'accounts/register.html',context)
# Create your views here.
def login(request):

    if(request.method =='POST'):
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email,  password=password)
        # auth.login(request,user)     
        if user is not None:
            auth.login(request,user)
            #messages.success(request,'you are now Loged in.')
            return redirect('home')
        else:
            messages.error(request,'Invalid Login Credentials')
            return redirect('login')
    return render(request,'accounts/signin.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out.')
    return redirect('login')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user =Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user =None

    if(user is not None and default_token_generator.check_token(user, token)):
        user.is_active = True
        user.save()
        messages.success(request,'congratulation! your account is activated')
        return redirect('login')

    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')
    
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__iexact=email)
            # reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset your Password'
            message = render_to_string('accounts/reset_password_email.html',{
                'user':user, 
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            # success mesage
            messages.success(request,'Password reset email has been sent to your email address.')
            return redirect('login')

        else:
            messages.error(request,'Account does not exist!')
            return redirect('forgotPassword')
    return render(request,'accounts/forgotPassword.html')
def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user =Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user =None
    if(user is not None and default_token_generator.check_token(user, token)):
        request.session['uid']=uid
        messages.success(request,'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.eror(request,'This link is expired!')
        return redirect('login')
        # return HttpResponse('ok')



def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        conform_password = request.POST['conform_password']

        if password == conform_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'PAssword reset successful')
            return redirect ('login')
        else:
            messages.error(request,'password do not match!')
            return redirect('resetPassword')
    else:
        return render(request,'accounts/resetPassword.html')

    
@login_required(login_url = 'login')      
def dashboard(request):
    return render(request,'accounts/dashboard.html')

