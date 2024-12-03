from django.urls import path
from .views import HomeView, RoomView

urlpatterns = [
    path("login/", HomeView.as_view(), name="login"),
path("<int:room_id>/<int:user_id>/", RoomView.as_view(), name="room"),
    
]
