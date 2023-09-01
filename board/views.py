from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.edit import FormMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .models import Post, Category, Comment
from .forms import PostForm, CommentForm
from .filters import CommentFilter


class UserDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = "board/user_posts.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_posts"] = Post.objects.filter(user=self.request.user).order_by(
            "-id"
        )
        return context


class PostList(ListView):
    model = Post
    template_name = "board/posts.html"
    context_object_name = "posts"
    ordering = "-date"
    paginate_by = 10


class PostDetail(LoginRequiredMixin, FormMixin, DetailView):
    model = Post
    template_name = "board/post.html"
    context_object_name = "post"
    slug_field = "slug"
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_author"] = (
            Post.objects.filter(user=self.request.user)
            .filter(slug=self.kwargs.get("slug"))
            .exists()
        )
        context["comments_post"] = (
            Comment.objects.filter(post=Post.objects.get(slug=self.kwargs.get("slug")))
            .filter(status=None)
            .order_by("-id")
        )
        context["comment_sent"] = (
            Comment.objects.filter(post=Post.objects.get(slug=self.kwargs.get("slug")))
            .filter(user=self.request.user, status=None)
            .exists()
        )
        context["comment_accept"] = (
            Comment.objects.filter(post=Post.objects.get(slug=self.kwargs.get("slug")))
            .filter(user=self.request.user, status=True)
            .exists()
        )
        context["comment_reject"] = (
            Comment.objects.filter(post=Post.objects.get(slug=self.kwargs.get("slug")))
            .filter(user=self.request.user, status=False)
            .exists()
        )
        return context

    def get_success_url(self):
        return reverse("post", kwargs={"slug": self.kwargs.get("slug")})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.get_object()
        comment.user = self.request.user
        comment.save()
        return super().form_valid(form)


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "board/post_form.html"
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return redirect("posts")


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "board/post_form.html"


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "board/post_delete.html"
    success_url = "/"


class PostCategoryList(ListView):
    model = Category
    template_name = "board/categories.html"
    ordering = "-id"


class PostCategoryDetails(DetailView):
    model = Category
    template_name = "board/category.html"
    context_object_name = "category"
    slug_field = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts_in_category"] = Post.objects.filter(
            category__name=Category.objects.get(slug=self.kwargs.get("slug"))
        ).order_by("-id")
        return context


class CommentList(LoginRequiredMixin, ListView):
    model = Comment
    filter_class = CommentFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_new"] = CommentFilter(
            self.request.GET,
            queryset=Comment.objects.filter(post__user=self.request.user)
            .filter(status="")
            .order_by("-id"),
        )
        context["is_accepted"] = CommentFilter(
            self.request.GET,
            queryset=Comment.objects.filter(post__user=self.request.user)
            .filter(status="True")
            .order_by("-id"),
        )
        context["is_rejected"] = CommentFilter(
            self.request.GET,
            queryset=Comment.objects.filter(post__user=self.request.user)
            .filter(status="False")
            .order_by("-id"),
        )
        return context


class CommentStatus(LoginRequiredMixin, UpdateView):
    model = Comment
    choice = None
    fields = []

    def post(self, request, *args, **kwargs):
        choice = self.choice
        comment = Comment.objects.get(pk=self.kwargs.get("pk"))
        if choice == "accept":
            comment.status = True
            comment.save()
        if choice == "reject":
            comment.status = False
            comment.save()
        else:
            return redirect(request.META.get("HTTP_REFERER"))
        return redirect(request.META.get("HTTP_REFERER"))


class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "board/com_delete.html"
    success_url = "/comments/rejected/"
