from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='event_list'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event/add/', views.EventCreateView.as_view(), name='event_add'),
    path('event/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_edit'),
    path('event/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
]
