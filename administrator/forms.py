from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.forms import widgets
from main.models import User, Student, PAYMENT_STATUS


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter Username...",
                "class": "shadow form-control form-control-user"
            }
        ))

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "shadow form-control form-control-user"
            }
        ))


class StudentVerificationForm(forms.ModelForm):
    Paid = forms.ChoiceField(
        choices=PAYMENT_STATUS,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
                'placeholder': " Payment Status",
            }
        ))
    
    Amount = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control form-control-user",
                'placeholder': " Amount Paid",
            }
        ))
    Date = forms.DateField(
        widget=forms.NumberInput(
            attrs={
                'type': 'date',
                'class': 'form-control form-control-select',
                'placeholder': " Select Payment Date",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    class Meta:
        model = Student
        fields = ('Paid', 'Amount', 'Date')


# class ProfileInfoUpdateForm(forms.ModelForm):
#     username = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "class": "form-control form-control-user",
#             }
#         ))
#     first_name = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "class": "form-control form-control-user",
#             }
#         ))
#     last_name = forms.CharField(
#         widget=forms.TextInput(
#             attrs={
#                 "class": "form-control form-control-user",
#             }
#         ))
#     email = forms.EmailField(
#         widget=forms.EmailInput(
#             attrs={
#                 "class": "form-control form-control-user",
#             }
#         ))

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'first_name', 'last_name')

