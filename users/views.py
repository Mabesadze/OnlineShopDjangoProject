from django.shortcuts import redirect, render

from django.contrib.auth import login, logout, update_session_auth_hash
from django.views.generic import FormView,View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import RegistrationForm, ProfileForm
from .models import UserProfile
from django.contrib.auth.forms import PasswordChangeForm




class logoutUserView(LoginRequiredMixin, FormView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse_lazy('users:login'))
    

class loginUserView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('shop:home')

class RegisterView(FormView):
    template_name = 'users/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
    
class ProfileView(LoginRequiredMixin, View):
    login_url = reverse_lazy('users:login')

    def get(self, request):
        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(instance=user_profile)
        password_form = PasswordChangeForm(user=request.user)

        context = {
            'profile': user_profile,
            'profile_form': profile_form,
            'password_form': password_form,
        }
        
        return render(request, 'users/profile.html', context)
    
    def post(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        profile_form = ProfileForm(request.POST, instance=user_profile)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        if 'profileupdate' in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                return redirect('users:profile')
            
        if 'passwordchange' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect('users:profile')
            
        context = {
            'profile_form': profile_form,
            'password_form': password_form,
        }
        
        return render(request, 'users/profile.html', context)
    