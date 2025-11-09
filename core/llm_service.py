import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import UserContent, ModelContent
from .models import Chat

def chat_response(user_message):
    load_dotenv()

    prev_chats = Chat.objects.all()
    history = list()
    for chat in prev_chats:
        if chat.is_by_user:
            history.append(UserContent(chat.content))
        else:
            history.append(ModelContent(chat.content))
    history.pop() # 유저의 마지막 채팅은 미포함하기 위함

    api_key = os.getenv("API_KEY")
    client = genai.Client(api_key=api_key)
    chat_generator = client.chats.create(model="gemini-2.5-flash", history=history)
    response_object = chat_generator.send_message(user_message)
    return response_object.text