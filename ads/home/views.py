from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Confirm, Password
import datetime
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import random
import math
from django.contrib.auth.hashers import make_password
import os


def register(request):
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        username = email
        
        
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect("register")
            
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect("register")
            
            
            else:
                for i in username:
                    if i.isupper():
                        messages.info(request, 'Email must be lowercase')
                        return redirect("register")

                    if i == " ":
                        messages.info(request, 'Email must not contain any Spaces')
                        return redirect("register")
                      
                if Confirm.objects.filter(email=email).exists():
                    confirm_user = Confirm.objects.get(email=email)
                    confirm_user.delete()
                    digits = "0123456789"
                    otp = ""
                    for i in range(6):
                        otp += digits[math.floor(random.random()*10)]
                    new_otp = otp
                    print(new_otp)
                    confirm_user = Confirm.objects.create(username=username, name=first_name, email=email, password=password1, otp=new_otp)
                    confirm_user.save()
                    subject = 'Thank You for registering to Affiliator.in!'
                    message = 'Hi ' + confirm_user.name + '!\n \nWe have recieved an Account Creation request from you.\n\nYour Email Confirmation Code is '+new_otp+'.\n\nAt Affiliator.in, you can easily add Affiliate Products right from your Dedicated Dashboard. Some key features are\n1) No Coding Required\n2) 100% Mobile Responsive\n3) Unlimitted Affiliate Products\n4) Unlimitted Bandwidth\n5) Add Unlimitted Product Categories\n6) Edit any Product Detail\nand many more...\n\nOur Dedicated Management Team is always at your service in case of any Discrepency\nAll the Best\nTeam Affiliator.in.'
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [confirm_user.email]
                    send_mail(subject, message, from_email, to_list, fail_silently=True)
                    messages.info(request, "An Account Confirmation email has been sent to "+confirm_user.email+". Please Enter the code here.")
                    return redirect("confirm_email", email)
                else:
                    digits = "0123456789"
                    otp = ""
                    for i in range(6):
                        otp += digits[math.floor(random.random()*10)]
                    new_otp = otp
                    confirm_user = Confirm.objects.create(username=username, name=first_name, email=email, password=password1, otp=new_otp)
                    confirm_user.save()
                    subject = 'Thank You for registering to Affiliator.in!'
                    message = 'Hi ' + confirm_user.name + '!\n \nWe have recieved an Account Creation request from you.\n\nYour Email Confirmation Code is '+new_otp+'.\n\nAt Affiliator.in, you can easily add Affiliate Products right from your Dedicated Dashboard. Some key features are\n1) No Coding Required\n2) 100% Mobile Responsive\n3) Unlimitted Affiliate Products\n4) Unlimitted Bandwidth\n5) Add Unlimitted Product Categories\n6) Edit any Product Detail\nand many more...\n\nOur Dedicated Management Team is always at your service in case of any Discrepency\nAll the Best\nTeam Affiliator.in.'
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [confirm_user.email]
                    send_mail(subject, message, from_email, to_list, fail_silently=True)
                    messages.info(request, "An Account confirmation email has been sent to "+confirm_user.email)
                    return redirect("confirm_email", email)
    
                
        
        else:
            messages.info(request, 'Password doesnt match')
            return redirect("register")
        
    else:
        return render(request, 'register.html')

def confirm_email(request, uname):
    
    if not Confirm.objects.filter(email=uname).exists():
        messages.info(request, "Please register first")
        return redirect("register")
    else:
        confirm_email = Confirm.objects.get(email=uname)
        old_otp = confirm_email.otp
        print(old_otp)
        
        if request.method == 'POST':
            otp = request.POST['otp']
            if otp == old_otp:
                user = User.objects.create_user(username=confirm_email.username, password=confirm_email.password, first_name=confirm_email.name, email=confirm_email.email)
                user.save()
                confirm_email.delete()
                messages.info(request, "Email confirmed successfully!")
                messages.info(request, "Login to continue.")
                return redirect("login")
            else:
                if confirm_email.attempts < 4:
                    confirm_email.attempts +=1
                    confirm_email.save()
                    messages.info(request, "Incorrect Otp, Try Again.")
                    messages.info(request, str((5-confirm_email.attempts))+ " attempts left.")
                    return redirect("confirm_email", uname)
                else:
                    confirm_email.attempts = 0
                    confirm_email.save()
                    messages.info(request, "Maximum Attempts held for this confirmation code. We've sent a new Confirmation code to "+confirm_email.email+". Please enter the new Code.")
                    return redirect("resend_code", confirm_email.email)

        

        return render(request, "confirm_email_otp.html", {'confirm_email':confirm_email})


def resend_code(request, uname):
    if Confirm.objects.filter(email=uname).exists():
        confirm_user = Confirm.objects.get(email=uname)
        digits = "0123456789"
        otp = ""
        for i in range(6):
            otp += digits[math.floor(random.random()*10)]
        new_otp = otp
        confirm_user.otp = new_otp
        confirm_user.save()
        subject = 'Your new Password Confirmation Code is '+new_otp+'.'
        message = 'Hi ' + confirm_user.name + '!\n \nWe have recieved an Account Creation request from you.\n\nYour New Email Confirmation Code is '+new_otp+'.\n\nAt Affiliator.in, you can easily add Affiliate Products right from your Dedicated Dashboard. Some key features are\n1) No Coding Required\n2) 100% Mobile Responsive\n3) Unlimitted Affiliate Products\n4) Unlimitted Bandwidth\n5) Add Unlimitted Product Categories\n6) Edit any Product Detail\nand many more...\n\nOur Dedicated Management Team is always at your service in case of any Discrepency\nAll the Best\nTeam Affiliator.in.'
        from_email = settings.EMAIL_HOST_USER
        to_list = [confirm_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        messages.info(request, "Account confirmation email has been sent to "+confirm_user.email)
        return redirect("confirm_email", uname)
    else:
        messages.info(request, "Please register first!")
        return redirect("register")
    




def login(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        for i in email:
            if i.isupper():
                messages.info(request, 'Username must be lowercase')
                return redirect("login")

        if User.objects.filter(email=email).exists():
            arpan = User.objects.get(email=email)
            
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
        
        user = auth.authenticate(username=arpan.username, password=password)
        
        if user is not None:
            auth.login(request, user)
            confirm_user = User.objects.get(email=email)
            subject = 'New login activity on your Affiliator.in account!'
            '''message = 'Hi ' + confirm_user.first_name + '!\n \nHope you are having a great time with Affiliator.in Affiliate Management Program.\n\nWe have detected a new login activity to your Affiliator.in Account with following details:-\nDate :- '+datetime.datetime.now().strftime("%d")+' '+datetime.datetime.now().strftime("%B")+' '+datetime.datetime.now().strftime("%Y")+'\nTime :- '+datetime.datetime.now().strftime("%H:%M:%S")+'\nDevice Name :- '+request.user_agent.device.family+'\nOperating System :- '+request.user_agent.os.family+' '+request.user_agent.os.version_string+'\nBrowser :- '+request.user_agent.browser.family+' '+request.user_agent.browser.version_string+'\n\nHopefully it was you who logged in your Affiliator.in Affiliate Managemment Account.\n\nIf it was not you, please contact our Management Team to secure your account from fraud.\n\nThank You\nTeam Affiliator.in' 
            '''
            message = 'hi' + confirm_user.first_name
            from_email = settings.EMAIL_HOST_USER
            to_list = [confirm_user.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            return redirect("home")
        
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')
        
    else:
        return render(request, 'login.html')
    

def logout(request):
    auth.logout(request)
    
    return redirect('/')

def forgot_password(request):
    if request.method == "POST":
        uname = request.POST['email']
        if uname:
            if User.objects.filter(email=uname).exists():
                
                if Password.objects.filter(email=uname).exists():
                    messages.info(request, "We have already sent the confirmation code to the email address associated with "+uname)
                    return redirect("enter_otp", uname)
                else:
                    curr_user = User.objects.get(email=uname)
                    digits = "0123456789"
                    otp = ""
                    for i in range(6):
                        otp += digits[math.floor(random.random()*10)]
                    new_otp = otp
                    print(new_otp)
                    pass_user = Password.objects.create(email=uname, otp=new_otp)
                    pass_user.save()
                    subject = 'Password Reset Request on Affiliator.in!'
                    message = 'Hi ' + curr_user.first_name + '!\n \nWe have recieved a password reset request on your User Account.\n\nYour Password reset code is ' + pass_user.otp +'\nIf it was not you, then please ignore.\n\nOur dedicated customer support team is always at your service.\nWishing you a happy online journey.\n\nThank You.\nTeam Affiliator.in'
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [curr_user.email]
                    send_mail(subject, message, from_email, to_list, fail_silently=True)
                    messages.info(request, "Enter the OTP sent to registered email address asssociated with "+uname)
                    return redirect("enter_otp", uname)
            else:
                messages.info(request, "No user with Username " + uname)
                messages.info(request, "Please enter your registered Username")
                return redirect("forgot_password")
        else:
            messages.info(request, "Enter the username")
            return redirect("forgot_password")
    return render(request, "enter_email.html")

def enter_otp(request, uname):
    if Password.objects.filter(email=uname).exists():
        pass_user = Password.objects.get(email=uname)
        curr_user = User.objects.get(email=uname)
        if request.method == "POST":
            curr_otp = request.POST['otp']
            if pass_user.otp == curr_otp:
                pass_user.confirmed = True
                pass_user.save()
                messages.info(request, "Email address confirmed")
                return redirect("new_password", uname)
            else:
                if pass_user.attempts < 4:
                    pass_user.attempts += 1
                    pass_user.save()
                    messages.info(request, "Incorrect otp, try again!" +str(5-pass_user.attempts)+" attempts left.")
                    return redirect("enter_otp", uname)
                else:
                    pass_user.attempts = 0
                    pass_user.save()
                    messages.info(request, "Maximum attempts held for this confirmation code. Sending another code to email associated with "+pass_user.email)
                    return redirect("resend_pass_code", uname)
        return render(request, "confirm_email_password.html", {'pass_user':pass_user})
    else:
        messages.info(request,"Enter the Registered username for which you want to change the Account Password.")
        return redirect("forgot_password")

def new_password(request, uname):
    if Password.objects.get(email=uname):
        pass_user = Password.objects.get(email=uname)
        curr_user = User.objects.get(email=uname)
        if request.method == "POST":
            if pass_user.confirmed:
                password1 = request.POST['password1']
                password2 = request.POST['password2']
                if password1:
                    if password1 == password2:
                        password = make_password(password1, hasher='default')
                        curr_user.password = password
                        pass_user.delete()
                        curr_user.save()
                        messages.info(request, "Password changed successfully.")
                        return redirect("login")
                    else:
                        messages.info(request, "Passwords Don't Match. Please re-enter the Passwords.")
                        return redirect("new_password")
                else:
                    messages.info(request, "Password Fields cannot be blank.")
                    return redirect("new_password")
            else:
                messages.info(request, "Please enter your username registered with Affiliator.in")
                return redirect("forgot_password")
        return render(request, "new_password.html")
    else:
        messages.info(request, "Please enter your username registered with Affiliator.in")
        return redirect("forgot_password")

def resend_pass_code(request, uname):
    if Password.objects.filter(email=uname).exists():
        curr_user = User.objects.get(email=uname)
        pass_user = Password.objects.get(email=uname)
        digits = "0123456789"
        otp = ""
        for i in range(6):
            otp += digits[math.floor(random.random()*10)]
        new_otp = otp
        pass_user.otp = new_otp
        print(new_otp)
        pass_user.save()
        subject = 'Password Reset Request on Affiliator.in!'
        message = 'Hi ' + curr_user.first_name + '!\n \nWe have recieved a password reset request on your User Account.\n\nYour Password reset code is ' + pass_user.otp +'\nIf it was not you, then please ignore.\n\nOur dedicated customer support team is always at your service.\n Wishing you a happy online journey.\n\nThank You.\nTeam Affiliator.in'
        from_email = settings.EMAIL_HOST_USER
        to_list = [curr_user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        messages.info(request, "Password reset code has been sent to email address associated with "+uname)
        return redirect("enter_otp", uname)
    else:
        messages.info(request, "Please enter the username first")
        return redirect("forgot_password")



def home(request):
    return render(request, 'index.html')

