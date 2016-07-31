from django import forms
from accounts.models import Customer
from django.contrib.admin.widgets import AdminDateWidget

class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new account.
    """
    username = forms.CharField(widget=forms.widgets.TextInput,
                               label="Nom d'utilisateur")
    firstname = forms.CharField(widget=forms.widgets.TextInput,
                                label="Prénom")
    lastname = forms.CharField(widget=forms.widgets.TextInput,
                               label="Nom de famille")
    email = forms.EmailField(widget=forms.widgets.TextInput,
                             label='Addresse Email')
    country = forms.CharField(max_length=50, widget=forms.widgets.TextInput,
                              label='Pays de résidence')
    city = forms.CharField(max_length=50, widget=forms.widgets.TextInput,
                           label='Ville')
    password1 = forms.CharField(widget=forms.widgets.PasswordInput,
                                label="Mot de passe")
    password2 = forms.CharField(widget=forms.widgets.PasswordInput,
                                label="Mot de passe(Confirmation)")
    date_of_birth = forms.DateField(label="Date de Naissance",
                                    widget=forms.widgets.SelectDateWidget(
                                        empty_label=("Choose Year", "Choose Month",
                                                     "Choose Day"),
    ))

    class Meta:
        model = Customer
        fields = ['firstname', 'lastname',
                  'username', 'password1',
                  'password2', 'date_of_birth', 'email', 'country', 'city']

    def clean(self):
        """
        This method verifies that the values entered in the form
        are valid.
        For example we check if the password the user entered into
        the field password1 and password1 match.
        NOTE : Errors will  appear in non_field_errors() because
        it applies to more than one field.
        """
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in cleaned_data and 'password2' in cleaned_data:
            if cleaned_data['password1'] != cleaned_data['password2']:
                raise forms.ValidationError("Les mots ne correspondent pas.\
                Veuillez verifier que les deux champs sont identiques.")
        return cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
