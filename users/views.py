from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import RedirectView
from django.conf import settings

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


class UserAccountView(FormView):
    model = User
    form_class = UserAccountForm
    template_name = 'users/account.html'

    def get(self, request, *args, **kwargs):
        context = {}
        user_id = kwargs.get('user_id')
        try:
            account = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return HttpResponse('Dosvidos')
        if account:
            context['id'] = account.id
            context['username'] = account.username
            context['email'] = account.email
            context['hide_email'] = account.hide_email

            is_self = True
            user = request.user
            if user.is_authenticated and user != account:
                is_self = False
            if not user.is_authenticated:
                is_self = False

            context['is_self'] = is_self
            context['BASE_URL'] = settings.BASE_URL

            return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        pass


class UserDeleteView(FormView):
    template_name = 'users/account.html'
