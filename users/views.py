from django.contrib.auth.models import User
from django.views import generic


class UsersList(generic.ListView):
    template_name = "users/users_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.all()
