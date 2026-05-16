from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from .services.orchestrator import Orchestrator
from .models import ChatThread, ChatMessage


# ============== CHAT PAGE ================
@login_required
def chat_page(request):
    """Main chat interface"""
    # Get user's recent threads
    recent_threads = ChatThread.objects.filter(user=request.user)[:10]
    
    context = {
        'recent_threads': recent_threads,
        'chat_history': []  # Will be loaded via JS for the active thread
    }
    return render(request, 'ai/chrysalis.html', context)
    # return render(request, 'ai/lis-ai.html', context)
    

# ====================== CHAT API (Main) ======================
@login_required
def chat_api(request):
    """Process message with Orchestrator"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_query = data.get('message', '').strip()
            thread_id = data.get('thread_id')

            if not user_query:
                return JsonResponse({'error': 'Message is required'}, status=400)

            # Get or create thread
            if thread_id:
                thread = ChatThread.objects.get(id=thread_id, user=request.user)
            else:
                thread = ChatThread.objects.create(user=request.user)
            
            # Process with AI Orchestrator
            orchestrator = Orchestrator()
            result = orchestrator.process(user=request.user, query=user_query)
            
            ai_response = result.get('message', '')

            # Save message
            ChatMessage.objects.create(
                thread=thread,
                user=request.user,
                query=user_query,
                response=ai_response,
                intent=result.get('intent'),
                stock_symbol=result.get('stock_symbol')
            )

            # Auto-generate thread title from first message
            if thread.messages.count() == 1:
                thread.generate_title(user_query)

            return JsonResponse({
                'response': ai_response,
                'intent': result.get('intent'),
                'stock_symbol': result.get('stock_symbol'),
                'thread_id': thread.id
            })

        except ChatThread.DoesNotExist:
            return JsonResponse({'error': 'Chat thread not found'}, status=404)
        except Exception as e:
            print("Chat API Error:", str(e))
            return JsonResponse({'error': 'Internal server error'}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


# ====================== CHAT HISTORY API ======================
@login_required
def chat_history_api(request):
    """Return list of recent chats for sidebar"""
    threads = ChatThread.objects.filter(user=request.user)[:15]
    
    history = []
    for thread in threads:
        last_message = thread.messages.last()
        last_text = last_message.query[:80] if last_message else "New Chat"
        
        history.append({
            'id': thread.id,
            'title': thread.title or "New Conversation",
            'last_message': last_text + "..." if len(last_text) > 77 else last_text,
            'time': thread.updated_at.strftime("%b %d, %I:%M %p"),
            'message_count': thread.messages.count()
        })
    
    return JsonResponse(history, safe=False)


# THREAD DETAILS                                 
@login_required
def chat_thread_detail(request, thread_id):
    """Return messages for a specific chat thread"""
    try:
        thread = ChatThread.objects.get(id=thread_id, user=request.user)
        
        messages = thread.messages.all()
        
        messages_data = []
        for msg in messages:
            messages_data.append({
                'query': msg.query,
                'response': msg.response,
                'intent': msg.intent,
                'stock_symbol': msg.stock_symbol,
                'created_at': msg.created_at.strftime("%I:%M %p")
            })
        
        return JsonResponse({
            'thread_id': thread.id,
            'title': thread.title,
            'messages': messages_data
        })
        
    except ChatThread.DoesNotExist:
        return JsonResponse({'error': 'Chat thread not found'}, status=404)
    except Exception as e:
        print("Thread Detail Error:", str(e))
        return JsonResponse({'error': 'Something went wrong'}, status=500)
    

# DELETE CHAT .............
@login_required
def delete_chat_thread(request, thread_id):
    """Delete a chat thread"""
    if request.method == 'POST':
        try:
            thread = ChatThread.objects.get(id=thread_id, user=request.user)
            thread.delete()
            return JsonResponse({'status': 'success', 'message': 'Chat deleted successfully'})
        except ChatThread.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Chat not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Failed to delete chat'}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=405)
