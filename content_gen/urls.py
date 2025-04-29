from django.urls import path
from .views import BusinessLogicView


app_name = "content_gen"

urlpatterns = [
    path('protected-endpoint/', BusinessLogicView.as_view(), name='business_logic_endpoint'),
]
