from django.urls import path
from WmVoice.views import api

app_name = 'WmVoice'

urlpatterns = [
    path('api/receive-transcript',
         api.ReceiveTranscriptView.as_view(), name='receiveTranscript'),
]
