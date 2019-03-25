from django import forms


class UserLoginForm(forms.Form):
    txtusername = forms.CharField(label='Username', widget=forms.TextInput, required=True)
    txtpassword = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)


