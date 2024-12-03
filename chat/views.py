from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework import status
from .serializers import MessageSerializer
from .models import Room, Message
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


# Create your views here.


class HomeView(APIView):
    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties= {
    'username': openapi.Schema(type=openapi.TYPE_STRING, description="Имя пользователя для регистрации"),
    'chat': openapi.Schema(type=openapi.TYPE_STRING, format='chat', description="Чат"),
},
        required=['username',  'chat']
    ),
    responses={
        status.HTTP_201_CREATED: openapi.Response(
            description="Operator registered successfully!",
            examples={
                'application/json': {'message': 'Operator registered successfully!'}
            }
        ),
        status.HTTP_400_BAD_REQUEST: openapi.Response(
            description="Invalid data"
        ),
    }
)
    def post(self, request):
        username = request.data.get("username")
        room = request.data.get("room")



        if username and room:
            try:
                existing_room = Room.objects.get(room_name__icontains=room)
            except Room.DoesNotExist:
                existing_room = Room.objects.create(room_name=room)

            # Перенаправление на комнату
            return redirect("room", room_name=room, username=username)
        
        return render(request, "home.html")

# Представление для комнаты
class RoomView(APIView):
    def get(self, request, room_id, user_id):
        try:
            existing_room = Room.objects.get(id=room_id)  # Используем id для поиска комнаты
            get_messages = Message.objects.filter(room=existing_room)
            serializer = MessageSerializer(get_messages, many=True)  # Сериализация данных
            context = {
                "messages": serializer.data,
                "user": user_id,  # Здесь предполагается, что user_id — это идентификатор пользователя
                "room_name": existing_room.room_name,
            }
            return Response(context, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({"error": "Room not found."}, status=status.HTTP_404_NOT_FOUND)