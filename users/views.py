from django.contrib.auth.models import User
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy


class UsersList(generic.ListView):
    template_name = 'registration/users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return User.objects.all()


class UserRegisterView(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')
