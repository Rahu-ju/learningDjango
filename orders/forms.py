from django import forms
from django.contrib.auth import get_user_model


class GuestCheckoutForm(forms.Form):
    email = forms.EmailField()
    email2 = forms.EmailField(label="Verify email")

    def clean(self):
        email = self.cleaned_data.get('email')
        email2 = self.cleaned_data.get('email2')

        if email == email2:
            user = get_user_model()

            # Checking the mail already exist in the user database or not
            user_exist = user.objects.filter(email=email).count()
            if user_exist != 0:
                raise forms.ValidationError("This user already exist. Please login instead.")
        else:
            raise forms.ValidationError("Please confirm emails are the same.")


class AddressSelectForm(forms.Form):
    billing = forms.CharField(max_length=120)
    shipping = forms.CharField(max_length=120)
