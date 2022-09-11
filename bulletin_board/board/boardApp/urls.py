from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostDelete, PostUpdate, \
   ReplyCreate, PostReplyList, PersonalReplyList, ReplyDelete, MailingCreate, add_accept


urlpatterns = [
   path('', PostList.as_view()),
   path('<int:pk>', PostDetail.as_view(), name='post'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
   path('create/<int:pk>', PostUpdate.as_view(), name='post_update'),
   path('rcreate/<int:pk>', ReplyCreate.as_view(), name='reply_create'),
   path('reply/<int:pk>', PostReplyList.as_view(), name='reply'),
   path('personal_reply/', PersonalReplyList.as_view(), name='personal_reply'),
   path('reply_delete/<int:pk>', ReplyDelete.as_view(), name='reply_delete'),
   path('accept/<int:pk>', add_accept, name='accept'),
   path('mailing/', MailingCreate.as_view(), name='mailing'),
]