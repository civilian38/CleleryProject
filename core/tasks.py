from celery import shared_task
from .serializers import ChatSerializer
from .llm_service import chat_response

@shared_task(bind=True)
def get_gemini_response_and_save(self, user_message):
    gemini_response_text = chat_response(user_message)
    response_data = {
        "content": gemini_response_text,
    }
    serializer = ChatSerializer(data=response_data)
    if not serializer.is_valid():
        self.update_status(state='FAILURE', meta={'error': serializer.errors})
        return f"Validation Error: {serializer.errors}"
    serializer.save(is_by_user=False)

    return "SUCCESS"