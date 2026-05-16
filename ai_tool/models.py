from django.db import models
from django.conf import settings
# from django.utils.timezone import now
# from django.contrib.auth import get_user_model


class ChatThread(models.Model):
    """Represents a conversation thread"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name='chat_threads')
    
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return self.title or f"Chat {self.id}"

    def generate_title(self, first_message: str):
        """Auto-generate title from first user message"""
        if not self.title:
            title = first_message[:60]
            if len(first_message) > 60:
                title += "..."
            self.title = title
            self.save()

    def delete_thread(self):
        """Safely delete thread and all its messages"""
        self.delete()


class ChatMessage(models.Model):
    """Individual messages in a thread"""
    
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, related_name='messages')
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    query = models.TextField()           # User message
    response = models.TextField()        # AI response
    
    intent = models.CharField(max_length=50, null=True, blank=True)
    stock_symbol = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.user.email}: {self.query[:40]}..."
    
