from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from users.forms import RegistrationForm


User = get_user_model()


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
