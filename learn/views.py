from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Video, LearningCategory, UserVideoProgress


def learning_home(request):
    """Main Learning Page"""
    categories = LearningCategory.objects.all()
    featured_videos = Video.objects.filter(is_featured=True)[:6]
    all_videos = Video.objects.select_related('category').all()

    context = {
        'categories': categories,
        'featured_videos': featured_videos,
        'all_videos': all_videos,
        # 'watched_count': UserVideoProgress.objects.filter(user=request.user, watched=True).count() if request.user.is_authenticated else 0,
    }
    return render(request, 'learning/learning_home.html', context)


def video_detail(request, slug):
    """Single Video Page"""
    video = get_object_or_404(Video, slug=slug)
    
    # Track progress if user is logged in
    if request.user.is_authenticated:
        UserVideoProgress.objects.get_or_create(user=request.user, video=video)

    related_videos = Video.objects.filter(category=video.category).exclude(id=video.id)[:4]

    context = {
        'video': video,
        'related_videos': related_videos,
    }
    return render(request, 'learning/video_detail.html', context)


@login_required
def mark_video_watched(request, video_id):
    """AJAX endpoint to mark video as watched"""
    video = get_object_or_404(Video, id=video_id)
    progress, _ = UserVideoProgress.objects.get_or_create(user=request.user, video=video)
    progress.watched = True
    progress.save()
    return JsonResponse({'status': 'success'})

