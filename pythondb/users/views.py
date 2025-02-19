from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from data import CATEGORIES
from knowledge_base.models import Category, Post

from .forms import CreationForm, ResetPasswordForm


class SignUp(CreateView):
    form_class = CreationForm

    success_url = reverse_lazy("knowledge_base:main")
    template_name = "users/signup.html"


class ResetPassword(CreateView):
    form_class = ResetPasswordForm

    success_url = reverse_lazy("knowledge_base:main")
    template_name = "users/password_reset.html"


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("knowledge_base:main")
        else:
            error_message = "Неверный логин или пароль"
            return render(
                request, "users/login.html", {"error_message": error_message}
            )
    return render(request, "users/login.html")


@login_required
def profile_view(request, user_id):
    user_profile = get_object_or_404(User, id=user_id)
    categories = Category.objects.all()
    posts = Post.objects.filter(author=user_profile).order_by("-created_at")
    return render(
        request,
        "users/profile.html",
        {
            "user_profile": user_profile,
            "posts": posts,
            CATEGORIES: categories,
        },
    )
