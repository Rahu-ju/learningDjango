import base64

from django.core.files.base import ContentFile, File
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# Create your views here.
class SignUp(CreateView):
    template_name = 'users/signup.html'
    form_class = CustomUserCreationForm
    success_url = '/'

    #authenticate user after successful registration
    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid

class UserInfoChange(LoginRequiredMixin, UpdateView):
    login_url = '/users/login/'
    template_name = 'users/settings.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user


#pic upload view
# @login_required(login_url='/users/login/')
# def user_profile_view(request):
#     '''Handle the image of the user.'''
#     if request.method == 'POST':
#
#         # get the base64 image data
#         image_data = request.POST.get('imagebase64')
#
#         # seperate the image data and format, then decode the image data
#         format, imgstr = image_data.split(';base64,')
#         ext = format.split('/')[-1]
#         decode_image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
#
#         #feed the image to the model instance and save
#         user = UserProfile(user=request.user, image= decode_image)
#         user.save()
#         messages.success(request, 'your pic updated successfully.')
#         return HttpResponseRedirect(reverse(':home'))
#
#     else:
#         # give initial data to the form
#         form = UploadPicForm(initial={'user': request.user})
#     return render(request, 'users/uploadpic.html', {'form': form})
