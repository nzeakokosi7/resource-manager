from django.contrib.auth.views import LoginView
from django.urls import path
from . import views

verification_renderer = views.ResourceFetchView.as_view()

resource_log_view = views.ResourceLogViewset.as_view({
    'get': 'list',
})

urlpatterns = [
   path('', views.resource_upload,
        name='upload'),
   path('confirmation', views.upload_success, name='resource_confirmation'),
   path('access', views.access_granted, name='access_granted'),
   path('retrieve/<int:pk>/', verification_renderer),
   path('logs', resource_log_view, name="logs")
]