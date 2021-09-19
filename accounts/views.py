from django.conf import settings
from django.shortcuts import render
from .forms import SignupForm
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

# from django.contrib.auth import User # global settings 오버라이딩을 통해서 인증 User 모델을 다른 모델로 변경할 수 있음 # 확인 필요

# Create your views here.

User = get_user_model()

signup = CreateView.as_view(
    model=User,  # 안써줘도 되긴 함
    form_class=SignupForm,
    success_url=settings.LOGIN_URL,
    template_name="accounts/signup.html",
)


@login_required
def profile(request):
    return render(request, "accounts/profile.html")
