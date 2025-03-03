from django.urls import path
from .views import root, create_content, get_contents, count_contents, get_content_by_id, update_content, delete_content

urlpatterns = [
    path('', root),
    path('contents/', create_content, name='create_content'),
    path('contents/', get_contents, name='get_contents'),
    path('contents/count', count_contents, name='count_contents'),
    path('contents/<int:content_id>/',
         get_content_by_id, name='get_content_by_id'),
    path('contents/<int:content_id>/', update_content, name='update_content'),
    path('contents/<int:content_id>/', delete_content, name='delete_content'),
]
