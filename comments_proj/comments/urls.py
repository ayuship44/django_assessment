from django.urls import path
from comments import views


urlpatterns = [
    path('comments_list/', views.comments_list, name='comments'),
    path('comments_detail/<int:pk>', views.comments_detail, name='comments_detail'),
    # url(r'^api/comments/published$', views.comments_published)
]