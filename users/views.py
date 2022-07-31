from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView, DeleteView, UpdateView
from django.views.generic import RedirectView

from users.forms import RegistrationForm, AuthenticationForm, UserAccountForm
from users.models import User


class UsersList(generic.ListView):
    template_name = 'users/list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all()


class UserRegisterView(FormView):
    model = User
    form_class = RegistrationForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('UsersList')

    def get(self, request):
        context = {
            'registration_form': RegistrationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
        context = {
            'registration_form': form
        }
        return render(request, self.template_name, context)


class UserAuthenticationView(FormView):
    model = User
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    success_url = reverse_lazy('UsersList')

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return redirect('home')
        context = {
            'login_form': AuthenticationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
        context = {
            'login_form': form
        }
        return render(request, self.template_name, context)


class UserLogoutView(RedirectView):
    url = reverse_lazy('home')

    def get(self, request):
        logout(request)
        return redirect('home')


class UserAccountView(UpdateView):
    template_name = 'users/account.html'
    model = User
    form_class = UserAccountForm

    def get_success_url(self):
        return reverse('home')


class UserDeleteView(DeleteView):
    template_name = 'users/delete.html'
    model = User
    success_url = reverse_lazy('home')
