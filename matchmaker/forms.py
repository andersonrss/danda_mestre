from django import forms

# Create your forms here.

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id': 'inputtext', 'placeholder': 'Username'}),
     label="User")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id': 'inputPassword', 'placeholder': 'Password'}),
     label="Password")


class ChangePasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'id': 'inputtext', 'placeholder': 'Username', 'disabled': True}),
     label="User", initial='class')
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id': 'inputOldPassword', 'placeholder': 'Password'}),
     label=" Password")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id': 'inputPassword', 'placeholder': 'New Password'}),
     label=" New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id': 'inputConfirmPassword', 'placeholder': 'Confirm Password'}),
     label="Confirm New Password")

    def set_username(self, username):
        self.username = username
		


class AddMusicianForm(LoginForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control', 'id': 'inputConfirmPassword', 'placeholder': 'Confirm Password'}),
     label="Confirm New Password")