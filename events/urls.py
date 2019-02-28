from django.urls import path
from events import views
#from django.conf import settings
#from django.conf.url import static
from .views import Login, Logout, Signup, home

urlpatterns = [
	path('', home, name='home'),
    path('event/', views.event, name='event'),
    path('add/', views.add_event, name='add_event'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('booked/', views.booked, name='booked'),
    path('<int:event_id>/booking/', views.booking, name='booking'),
    path('<int:event_id>/', views.event_detail, name='event-detail'),
    path('<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('<int:event_id>/update/', views.update_event, name='update_event'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    #path('events_search/', views.events_search, name='events_search'),
]



#if settings.DEBUG:
    #urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)