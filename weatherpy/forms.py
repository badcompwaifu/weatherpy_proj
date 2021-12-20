from django import forms
from .models import MessagesDb


class WeatherForm(forms.Form):
    testinput = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Digite uma localidade',
            'class': 'formclass',
        }),
        label=False,
    )


class UserMessage(forms.ModelForm):
    class Meta:
        model = MessagesDb
        fields = ['name', 'contact_email', 'message']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Name', 'class': 'contactname'}),
            'contact_email': forms.EmailInput(attrs={'placeholder': 'E-mail', 'class': 'contactemail'}),
            'message': forms.Textarea(attrs={'placeholder': 'Message', 'class': 'contactmessage'}),

        }
