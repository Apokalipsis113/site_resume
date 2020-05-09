from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class UserSingupForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()  # dosen't works
        #model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # adding label names for fields
        self.fields['username'].label = 'Display name'
        self.fields['email'].label = 'Email adress'
