from django import forms

from mainapp.models import Subscribe


class ContactForm(forms.Form):
    name = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'name', 'label':
        None}), max_length=50, required=True)
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'placeholder': 'email'}),
                             max_length=50, required=True)
    message = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'message'}),
                              required=True)


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['client_email']