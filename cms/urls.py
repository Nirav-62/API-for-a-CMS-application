from django.urls import include,path
from cms import views
urlpatterns = [
    path('user_create',views.create_user,name='create_user'),
    path('user_update/<int:user_id>',views.update_user,name='update_user'),
    path('user_delete/<int:user_id>',views.delete_user,name='delete_user'),
    path('user/<int:user_id>',views.get_user,name='get user'),

    path('posts/<int:user_id>',views.see_posts,name='posts'),             #   retrieve all the post based on whether it is private or not
    path('post/<int:id>/<int:user_id>',views.get_post,name="get_post"),                 #   retrieve single post using post id  based on whether it is private or not             
    path('create_post',views.create_post,name='create_post'),
    path('delete_post/<int:post_id>/<int:user_id>',views.delete_post,name="delete_post"),        # url for delete the post based on the ownership of the post
    path('update_post/<int:post_id>/<int:user_id>',views.update_post,name="update_post"),            # url for update the post based on the ownership of the post

    path('create_like',views.create_like,name="create_like"),
    path('update_like',views.update_like,name="update_like"),  # delete functionality is also implemented in update
    path('get_like/<int:like_id>',views.get_like,name="get_like"),

]
