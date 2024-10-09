from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm

# Create your views here.
# LOGIN FUNCTION
def home(request):
    # records=Record.objects.all()
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            

            messages.success(request,'You have login succesfully!')
            return redirect('home')
        else:
            messages.success(request,"We couldn't find an account with that username. Try another, or get a new  account.") 
            return redirect('home')
    else:
          return render(request,'home.html')

    return render(request,'home.html')

# LOGOUT FUNCTION   
def logout_user(request):
    logout(request) 
    messages.success(request,"You have been logout succesfully") 
    return redirect('home')

# REGISTER FUNCTION
def Register_user(request):
    form=SignUpForm()
    if request.method=='POST':
      form=SignUpForm(request.POST)
      
      if form.is_valid():
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        
        current_site = get_current_site(request)  
        mail_subject = 'Activation link has been sent to your email id'   
        message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
        to_email = form.cleaned_data.get('email')  
        email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
        email.send()  
        messages.success(request,"Please confirm your email address to complete the registration") 
        return redirect('home')
       
      else:  
          
          form = SignUpForm()  
          return render(request, 'register.html', {'form': form})
    return render(request, 'register.html')
