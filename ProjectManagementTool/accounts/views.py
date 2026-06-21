from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate,login,logout)
from .forms import (RegisterForm,LoginForm)
from django.contrib import messages


#landings page: contains links to register and login pages.
def home(request):
    return render(
        request,
        'accounts/home.html'
    )

#register view: handles user registration. If the request method is POST, it validates the form and creates a new user. If the form is valid, it redirects to the login page. If the request method is GET, it renders the registration form.



def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            messages.success(
                request,
                "Registration Successful."
            )

            return redirect('login')

        else:

            for field, errors in form.errors.items():

                for error in errors:
                    messages.error(
                        request,
                        f"{field.capitalize()}: {error}"
                    )

    else:

        form = RegisterForm()

    return render(
        request,
        'accounts/register.html',
        {'form': form}
    )

#login view: handles user login. If the request method is POST, it validates the form and authenticates the user. If the authentication is successful, it logs in the user and redirects to the dashboard. If the request method is GET, it renders the login form.



def login_view(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)

            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            if user is not None:

                login(request, user)

                return redirect('analytics_dashboard')

            else:

                messages.error(
                    request,
                    'Invalid email or password'
                )

        except User.DoesNotExist:

            messages.error(
                request,
                'Invalid email or password'
            )

    return render(
        request,
        'accounts/login.html'
    )


#logout view: logs out the user and redirects to the login page.
def logout_view(request):

    logout(request)

    return redirect('login')

#dashboard view: renders the dashboard page. If the user is not authenticated, it redirects to the login page.
def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('login')

    return render(
        request,
        'accounts/dashboard.html'
    )