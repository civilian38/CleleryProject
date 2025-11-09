from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import Chat
from .serializers import ChatSerializer
from .tasks import get_gemini_response_and_save


class ChatView(APIView):
    permission_classes = [AllowAny]

    # chat list
    def get(self, request):
        chats = Chat.objects.all()
        serializer = ChatSerializer(chats, many=True)
        return Response(serializer.data)

    def post(self, request):
        # 유저 채팅 저장
        serializer = ChatSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user_message = serializer.validated_data["content"]
        serializer.save(is_by_user=True)

        # llm 응답 저장 (비동기 처리)
        task = get_gemini_response_and_save.delay(user_message)
        return Response({"task_id": task.id}, status=status.HTTP_202_ACCEPTED)