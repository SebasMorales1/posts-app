from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse

from .models import Post, Comment

def index(request):
  if request.method == "GET":
    posts = Post.objects.all()
    context = {
      "posts": posts
    }
    return render(request, "posts/index.html", context)

def manage(request):  
  if request.method == "GET":
    if request.GET.get("id"):
      id = request.GET.get("id")
      post = get_object_or_404(Post, pk=id)

      return render(request, "posts/manage.html", { "post": post })

    return render(request, "posts/manage.html")
  
  elif request.method == "POST" and request.POST.get("type") == "post":
    title = request.POST.get("title")
    description = request.POST.get("description")

    newPost = Post.objects.create(title=title, description=description)
    newPost.save()

    messages.success(request, "Post Created")
    
    return redirect("posts:manage")
  
  elif request.method == "POST" and request.POST.get("type") == "put":
    id = request.GET.get("id")
    post = get_object_or_404(Post, pk=id)
    newTitle = request.POST.get("title")
    newDescription = request.POST.get("description")

    post.title = newTitle
    post.description = newDescription
    post.save()

    messages.success(request, "Post Edited")

    return redirect("posts:manage")
  
  elif request.method == "POST" and request.POST.get("type") == "delete":
    id = request.GET.get("id")
    post = get_object_or_404(Post, pk=id)
    post.delete()

    messages.success(request, "Post Deleted")

    return redirect("posts:manage")

def detail(request, post_id):
  def text_format(text: str) -> list[str]:
    def add_format(split: str):
      if split == "\r":
        return "*&space*"
      elif split.endswith("\r"):
        return split[:len(split)-1]
      else:
        return split
    return list(map(add_format, text.split("\n")))

  post = get_object_or_404(Post, pk=post_id)

  if request.method == "GET":
    description_formated = []
    comments_formated = []

    if (post.description):
      description_formated = text_format(post.description)
    
    if request.GET.get("comments") == "show":
      comments = post.comment_set.all()
      for comment in comments:
        comments_formated.append({
          "text": text_format(comment.text),
          "published": comment.published
        })

    context = {
      "post": post,
      "description_formarted": description_formated,
      "comments": comments_formated
    }

    return render(request, 'posts/detail.html', context)
  
  elif request.method == "POST":
    textComment = request.POST.get("comment")
    newComment = Comment(text=textComment, post=post)
    url_redirection = reverse("posts:detail", kwargs={ "post_id": post_id }) + "?comments=show"
    newComment.save()

    messages.success(request, "Comment added")
    return redirect(url_redirection)