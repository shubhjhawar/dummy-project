from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('', TaskView, basename='task')


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard', Dashboard.as_view(), name='dashboard'),
    path('login/', LoginView.as_view(), name='login'),
    path('api/login/', EmailLoginView.as_view()),
    path('', include(router.urls)),
    path('my_tasks/<str:task_status>/',MyTaskView.as_view()),
    path("add_remark",RemarkView.as_view(), name='remark'),
    path("get_remark/<int:task_id>/", GetRemarkView.as_view()),
    path("createtask", CreateTaskView.as_view(), name='create-task'),
    path("create_user", CreateUserView.as_view(), name='create-user'),
    path("change_status1", ChangeStatusView.as_view(), name='change-status'),
    path("tasks/<str:task_status>/",AllTaskView.as_view(), name='tasks-list'),
    path("user_login", UserLoginView.as_view(), name='user-login'),
    path("user_task/<int:user_id>", UserTaskView.as_view(), name='user-task'),
]