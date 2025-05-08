from django.urls import path

from .views import ProcessImageView, ImageResultsView

urlpatterns = [
    path('process/', ProcessImageView.as_view(), name='process-image'),
    path('results/', ImageResultsView.as_view(), name='results-list'),
]
