from django.contrib.auth.models import User
from myblog.models import *
from django.forms import ModelForm
class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
