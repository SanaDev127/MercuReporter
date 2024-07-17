from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, LoginForm, UserRegistrationForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])

            if user is not None:
                login(request, user)
                if user.groups.filter(name='Supervisors').exists():  # Depending on the group the user belongs to, send them to a specific home dashboards
                    return render(request, 'dashboards/supervisor_dashboard.html', {'user': user})
                elif user.groups.filter(name='Owners').exists():
                    return render(request, 'dashboards/owner_dashboard.html', {'user': user})
                elif user.groups.filter(name='Drivers').exists():
                    return render(request, 'dashboards/driver_dashboard.html', {'user': user})
                else:
                    return render(request, 'home.html', {'user': user})

            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                user_form.cleaned_data['password']
            )
            group = Group.objects.get(name=user_form.cleaned_data['group'])
            new_user.save()
            new_user.groups.add(group)
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'account/register.html',
                  {'user_form': user_form})



class SignupPageView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"




