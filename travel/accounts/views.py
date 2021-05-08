from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import (
    DetailView, FormView
)

from accounts.forms import UserRegisterForm
from accounts.models import UserProfile

User = get_user_model()


class UserRegisterView(FormView):
    template_name = 'accounts/user_register_form.html'
    form_class = UserRegisterForm
    success_url = '/login'

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create(
            username=username,
            email=email,
            password=password
        )
        new_user.set_password(password)
        new_user.save()
        return super(UserRegisterView, self).form_valid(form)


class UserDetailView(DetailView):
    template_name = "accounts/user_detail.html"
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(
            User, username__iexact=self.kwargs.get("username")
        )

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context["following"] = UserProfile.objects.is_following(
            self.request.user,
            self.get_object()
        )
        context['recommended'] = UserProfile.objects.recommended(
            self.request.user
        )
        return context


class UserFollowView(View):
    def get(self, request, username, *args, **kwargs):
        toggle_user = get_object_or_404(User, username__iexact=username)
        if request.user.is_authenticated:
            is_following = UserProfile.objects.toggle_follow(
                request.user,
                toggle_user)
        return redirect("accounts:detail",
                        username=username)  # HttpResponseRedirect()
