from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from authy.models import Profile


def UsuariosProhibidos(value):
    usuarios_prohibidos = ['admin', 'css', 'js', 'authenticate', 'login', 'logout',
                           'root', 'administrator', 'email', 'join', 'sql', 'insert',
                           'db', 'static', 'python', 'delete', 'TABLE', 'insert']

    if value.lower() in usuarios_prohibidos:
        raise ValidationError('Nombre de usuario invalido, el nombre ingresado es una palabra reservada')


def UsuarioInvalido(value):
    if '@' in value or '+' in value or '-' in value:
        raise ValidationError('Nombre de usuario invalido, no usar caracteres como: @, +, -')


def EmailUnico(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError('El mail ingresado ya se encuentra registrado')


def UsuarioUnico(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError('El nombre de usuario ingresado ya se encuentra registrado')


class SignupForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(), max_length=30, required=True)
    email = forms.CharField(widget=forms.EmailInput(), max_length=100, required=True)
    first_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    last_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label='Ingrese la contraseña nuevamente')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].validators.append(UsuariosProhibidos)
        self.fields['username'].validators.append(UsuarioInvalido)
        self.fields['username'].validators.append(UsuarioUnico)
        self.fields['email'].validators.append(EmailUnico)

    def clean(self):
        super(SignupForm, self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            self._errors['password'] = self.error_class(['Las contraseñas no coinciden'])
        return self.cleaned_data


class ChangePasswordForm(forms.ModelForm):
    id = forms.CharField(widget=forms.HiddenInput())
    old_password = forms.CharField(widget=forms.PasswordInput, label="Contraseña vieja", required=True)
    new_password = forms.CharField(widget=forms.PasswordInput, label="Contraseña nueva", required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña nueva", required=True)

    class Meta:
        model = User
        fields = ('id', 'old_password', 'new_password', 'confirm_password')

    def clean(self):
        super(ChangePasswordForm, self).clean()
        id = self.cleaned_data.get('id')
        old_password = self.cleaned_data.get('old_password')
        new_password = self.cleaned_data.get('new_password')
        confirm_password = self.cleaned_data.get('confirm_password')
        user = User.objects.get(pk=id)

        if not user.check_password(old_password):
            self._errors['old_password'] = self.error_class(['La contraseña vieja ingresada es incorrecta'])
        if new_password != confirm_password:
            self._errors['password'] = self.error_class(['Las contraseñas no coinciden'])
        return self.cleaned_data


class EditProfileForm(forms.ModelForm):
    picture = forms.ImageField(required=False)
    first_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    last_name = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    location = forms.CharField(widget=forms.TextInput(), max_length=50, required=False)
    info = forms.CharField(widget=forms.TextInput(), max_length=150, required=False)

    class Meta:
        model = Profile
        fields = ('picture', 'first_name', 'last_name', 'location', 'info')



