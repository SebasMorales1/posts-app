from django.urls import path
from .views import index, manage, detail

app_name = "posts"
urlpatterns = [
  path('', index, name="index"),
  path('manage', manage, name="manage"),
  path('post/<int:post_id>', detail, name="detail")
]