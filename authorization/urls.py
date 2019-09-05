from django.urls import path

from authorization import views

urlpatterns = [
    path('user', views.UserView.as_view()),
    path('authorize', views.__authorize_by_code),
    path('logout', views.logout),
    path('status', views.get_status)
]
