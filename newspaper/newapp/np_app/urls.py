from django.urls import path
from .views import PostList, PostDetail, Search, PostCreate, PostUpdate, PostDelete, UserUpdateView,\
    CategoryList, add_subscribe


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search', Search.as_view()),
    path('add/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('user/', UserUpdateView.as_view(), name='user_update'),
    path('category/', CategoryList.as_view(), name='category'),
    path('subscribe/<int:pk>', add_subscribe, name='subscribe')
    #path('app/', IndexView.as_view())
]