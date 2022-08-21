"""task_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin

from task_manager import views as view
from users import views as user_view
from statuses import views as statuses_view
from tasks import views as tasks_view
from labels import views as labels_view
from django.urls import path


urlpatterns = (
    path('', view.HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('login/', user_view.UserLoginView.as_view(), name='login'),
    path('users/', user_view.UsersList.as_view(), name='users'),
    path('users/logout/', user_view.UserLogoutView.as_view(), name='logout'),
    path('users/create/', user_view.UserCreateView.as_view(), name='create_user'),
    path('users/<int:pk>/update/', user_view.UserUpdateView.as_view(), name='update_user'),
    path('users/<int:pk>/delete/', user_view.UserDeleteView.as_view(), name='delete_user'),
    path('statuses/', statuses_view.StatusesListView.as_view(), name='statuses'),
    path('statuses/create/', statuses_view.StatusCreateView.as_view(), name='create_status'),
    path('statuses/<int:pk>/update/', statuses_view.StatusUpdateView.as_view(), name='update_status'),
    path('statuses/<int:pk>/delete/', statuses_view.StatusDeleteView.as_view(), name='delete_status'),
    path('tasks/', tasks_view.TasksListView.as_view(), name='tasks'),
    path('tasks/create/', tasks_view.TaskCreateView.as_view(), name='create_task'),
    path('tasks/<int:pk>/update/', tasks_view.TaskUpdateView.as_view(), name='update_task'),
    path('tasks/<int:pk>/delete/', tasks_view.TaskDeleteView.as_view(), name='delete_task'),
    path('tasks/<int:pk>/', tasks_view.TaskView.as_view(), name='view_task'),
    path('labels/', labels_view.LabelsListView.as_view(), name='labels'),
    path('labels/create/', labels_view.LabelCreateView.as_view(), name='create_label'),
    path('labels/<int:pk>/update/', labels_view.LabelUpdateView.as_view(), name='update_label'),
    path('labels/<int:pk>/delete/', labels_view.LabelDeleteView.as_view(), name='delete_label')
)
