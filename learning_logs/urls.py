from django.urls import path, include
from users import views as auth_view
from rest_framework_nested import routers
from broadcast.views import (
    BTopicRetrieveUpdateDestroyView, BEntryRetrieveUpdateDestroyView,
    BEntryListCreateView, BTopicListCreateView
)
from . import views

app_name = 'learning_logs'

# HTML pages
urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('topic/<uuid:pk>/', views.topic, name='topic'),
    path('entry/<uuid:pk>/', views.entry, name='entry'),

    # User app URLs
    path('login/', auth_view.user_login, name='login'),
    path('signup/', auth_view.user_signup, name='signup'),
    path('logout/', auth_view.log_out, name='logout'),

    # Broadcast API (separate)
    path('api/btopic/', BTopicListCreateView.as_view(), name='btopic-lc'),
    path('api/bentry/', BEntryListCreateView.as_view(), name='bentry-lc'),
    path('api/btopic/<uuid:pk>/', BTopicRetrieveUpdateDestroyView.as_view(), name='btopic-rud'),
    path('api/bentry/<uuid:pk>/', BEntryRetrieveUpdateDestroyView.as_view(), name='bentry-rud'),

    # Misc / Testing
    path('dummy/', views.dummy, name='dummy'),
]

# Routers
router = routers.DefaultRouter()
router.register(r'topics', views.TopicAPIView, basename='topic')
router.register(r'entry', views.EntryAPIView, basename='entry')

topics_router = routers.NestedDefaultRouter(router, r'topics', lookup='topic')
topics_router.register(r'entries', views.EntryAPIView, basename='topic-entries')

# Include routers under /api/
urlpatterns += [
    path('api/', include(router.urls)),
    path('api/', include(topics_router.urls)),
]
