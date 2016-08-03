from django import forms


# Maybe I should call this class LoginForm instead
class AuthenticationForm(forms.Form):
    """
    This is the Login Form.
    """
    username = forms.CharField(widget=forms.widgets.TextInput,
                               label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.widgets.PasswordInput,
                               label='Mot de passse')

    class Meta:
        fields = ['username', 'password']
