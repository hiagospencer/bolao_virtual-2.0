from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, UserProfile

class CadastroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefone = forms.CharField(max_length=20)
    chave_pix = forms.CharField(max_length=100)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Cria o perfil vinculado
            UserProfile.objects.create(
                user=user,
                telefone=self.cleaned_data['telefone'],
                chave_pix=self.cleaned_data['chave_pix'],
            )
        return user
