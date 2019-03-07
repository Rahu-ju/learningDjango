from django import forms

from .models import Join


class JoinForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'id': 'validationCustom03'})
        # self.fields['ip_address'].widget.attrs.update({'class': 'form-control', 'id': 'validationCustom04'})

    class Meta:
        fields = ['email',]
        model = Join
