from django.urls import path, include

app_name = 'api'

urlpatterns = [
    path('photohub/', include('api.photohub.urls'), name='photohub'),
]
