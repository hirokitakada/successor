from django.shortcuts import render, redirect
from django.views.generic import TemplateView, FormView, UpdateView
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, 
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate

from .models import User, Image
from .forms import ImageForm

from .forms import (
    UserInfoChangeForm,
    CustomAuthenticationForm, CustomPasswordChangeForm,
    CustomPasswordResetForm, CustomSetPasswordForm,
    CustomUserChangeForm, CustomUserCreationForm, EmailChangeForm,
    EmailAuthenticationForm
)
from django.contrib.auth.forms import (
    UserChangeForm,
    )

class AccountsView(TemplateView):
    template_name = "registration/account.html"

# class UserProfileView(LoginRequiredMixin, TemplateView):
#     template_name = 'registration/introduce.html'
#     def get_queryset(self):
#         return User.objects.get(id=self.request.user.id)

class UserProfileView(TemplateView):
    template_name = 'registration/introduce.html'
    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)

class EmailChangeView(LoginRequiredMixin, FormView):
    template_name = 'registration/change.html'
    form_class = EmailChangeForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'email' : self.request.user.email,
        })
        return kwargs



"""
class UserCreateView(FormView):
    # form_class = UserCreationForm
    form_class = CustomUserCreationForm
    template_name = 'registration/create.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):

        domains = ['east.ntt.co.jp', 'west.ntt.co.jp']

        print(self.request.POST['next'])
        if self.request.POST['next'] == 'back':
            print(form)
            return render(self.request, 'registration/create.html', {'form': form})
        elif self.request.POST['next'] == 'confirm':
            return render(self.request, 'registration/create_confirm.html', {'form': form})
        elif self.request.POST['next'] == 'regist':
            print(form.cleaned_data['text'])
            form.save()
            # 認証
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
            )
            # ログイン
            login(self.request, user)
            return super().form_valid(form)

        elif self.request.POST['next'] == 'introduce':
            print(form)
            address = str(form.cleaned_data['email'])
            #print(address)
            _, domain = address.split('@')
            #print(domain)

            if domain in domains:
                return render(self.request, 'registration/create_introduce.html', {'form': form})
            else:
                print("error")
                return render(self.request, 'registration/create.html', {'form': form})

        elif self.request.POST['next'] == 'details':
            print(form)
            return render(self.request, 'registration/create_details.html', {'form': form})

        else:
            # 通常このルートは通らない
            return redirect(reverse_lazy('base:top'))
"""

class UserCreateView(FormView):
    # form_class = UserCreationForm
    form_class = CustomUserCreationForm
    template_name = 'registration/create.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):

        domains = ['east.ntt.co.jp', 'west.ntt.co.jp']

        print(self.request.POST['next'])

        if self.request.POST['next'] == 'back':
            return render(self.request, 'registration/create.html', {'form': form})
        elif self.request.POST['next'] == 'confirm':
            print(form)
            address = str(form.cleaned_data['email'])
            # print(address)
            _, domain = address.split('@')

            if domain in domains:
                # print(domain)
                context = {'form': form}
                return render(self.request, 'registration/create_confirm.html', {'form': form})
            else:
                print("error")
                return render(self.request, 'registration/create.html', {'form': form})

        elif self.request.POST['next'] == 'regist':
            form.save()
            # 認証
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
            )
            # ログイン
            login(self.request, user)
            return super().form_valid(form)

        else:
            # 通常このルートは通らない
            return redirect(reverse_lazy('base:top'))




class CustomLoginView(LoginView):
    # form_class = CustomAuthenticationForm
    form_class = EmailAuthenticationForm
    template_name = 'registration/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'
    next_page = '/'

class UserChangeView(LoginRequiredMixin, FormView):
    template_name = 'registration/change.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            'email' : self.request.user.email,
            'first_name' : self.request.user.first_name,
            'last_name' : self.request.user.last_name,
        })
        return kwargs

class CustomLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'
    next_page = '/'

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'registration/password_change_form.html'
    success_url = reverse_lazy('accounts:password_change_done')

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'registration/password_change_done.html'

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    form_class = CustomPasswordResetForm
    from_email = 'info@example.com'
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    template_name = 'registration/password_reset_form.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'



def upload(request):
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts/showall')
    else:
        form = ImageForm()

    context = {'form':form}
    return render(request, 'album/upload.html', context)


def showall(request):
    images = Image.objects.all()
    context = {'images':images}
    return render(request, 'album/showall.html', context)
