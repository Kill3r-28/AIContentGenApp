from django.urls import path
from .views import GptRequestView, PromptView


app_name = "content_gen"

urlpatterns = [
    path('generate/', GptRequestView.as_view(), name='generate_endpoint'),
    path('prompt/', PromptView.as_view(), name='prompt_endpoint'),
]
