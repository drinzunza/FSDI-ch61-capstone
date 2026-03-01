from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required

"""
Class-based views:

View        = Generic View
ListView    = Get a list of records
DetailView  = Get a single(detail) record
CreateView  = Create a new record
UpdateView  = Modify an existing record
LoginView   = LogIn
"""

class PostList(ListView):
    model = Post
    template_name = "blog/list.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm() # Create new form and send it to html
        return context


# model, form_class, template_name, success_url
class PostCreate(CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/create.html"
    success_url = reverse_lazy("post_list")


class PostDetail(DetailView):
    model = Post
    template_name = "blog/details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.select_related("author").order_by("-created_on")

        # liked by me
        user = self.request.user
        if user.is_authenticated:
            context["linked_by_me"] = self.object.liked_by.filter(id=user.id)
        else:
            context["linked_by_me"] = False

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user if request.user.is_authenticated else None
            comment.save()
            return redirect("post_details", pk=self.object.pk)

        context = self.get_context_data()
        context["comment_form"] = form
        return self.render_to_response(context)



@login_required
def toggle_like(request):
    post_id = int(request.POST.get("post_id"))
    user = request.user

    # get the post
    post = Post.objects.get(id=post_id)
    if post.liked_by.filter(id=user.id).exists():
        # remove the like
        post.liked_by.remove(user)
    else:
        # add the like
        post.liked_by.add(user)

    return redirect("post_details", post_id)
    