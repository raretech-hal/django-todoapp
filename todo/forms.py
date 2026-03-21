from django import forms
from .models import TodoTask, Profile
from django.contrib.auth.models import User

class TodoTaskForm(forms.ModelForm):
    class Meta:
        model = TodoTask
        fields = ['title', 'description', 'completed', 'category', 'duedate']

class ProfileEditForm(forms.ModelForm):
    display_name = forms.CharField(required=False, max_length=100)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name'] # username自体は編集できない仕様
        # fields = ['username', 'email', 'first_name', 'last_name']

    # profileモデルのdisplay_name更新の処理
    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if user:
            profile, created = Profile.objects.get_or_create(user=user)
            self.fields['display_name'].initial = profile.display_name

    def save(self, commit=True):
        user = super().save(commit=commit)

        profile, created = Profile.objects.get_or_create(user=user)
        profile.display_name = self.cleaned_data.get('display_name', '')
        profile.save()

        return user