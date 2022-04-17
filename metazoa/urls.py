
from django.urls import path,include
from .views import *
urlpatterns = [
    path('',home , name='home'),
    
    path('login/' ,Login , name ="login"),
    path('signup/' ,Signup , name ="signup"),
    path('logout/' ,Logout , name ="logout"),
    path('allblog/' ,Allblog , name ="allblog"),
    path('blog/<str:id>' ,Blog , name ="blog"),
    path('addblog' ,AddBlog , name ="addblog"),
    path('authorblog' ,AuthorBlog , name ="authorblog"),
    path('blog/delete//<str:id>',DeleteBlog,name='deleteblog')
    
    
    
]
