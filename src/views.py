from django.shortcuts import render

from apps.photohub.models import Photo


def index(request):
    results = Photo.objects.all().order_by('uploaded_at')
    context = {
        'results': results,
        'completed_count': results.filter(status='completed').count(),
        'pending_count': results.filter(status__in=['pending', 'processing']).count()
    }
    return render(request, 'index.html', context)
