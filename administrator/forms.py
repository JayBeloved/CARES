from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.forms import widgets
from main.models import User, Student, PAYMENT_STATUS, Course, Resource


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


class ResourceUploadForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
                'placeholder': " Course",
            }
        ))
    
    category = forms.ChoiceField(
        choices=Resource.CATEGORY_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
                'placeholder': " Material Category",
            }
        ))
    
    mat_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Name of Resource",
                "class": "shadow form-control form-control-user"
            }
        ))
    
    description = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Short Description of the resource",
                "class": "shadow form-control form-control-user"
            }
        ))

    link = forms.URLField(
        widget=forms.URLInput(
            attrs={
                "class": "form-control form-control-user",
                'placeholder': " Link to File",
            }
        ))
    
    date_added = forms.DateField(
        widget=forms.NumberInput(
            attrs={
                'type': 'date',
                'class': 'form-control form-control-select',
                'placeholder': " Date Added",
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
            }
        ))

    class Meta:
        model = Resource
        fields = ['course', 'category', 'mat_name', 'description', 'link', 'date_added']

class CourseCreationForm(forms.ModelForm):
    course_title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Course Title",
                "class": "shadow form-control form-control-user"
            }
        ))
    
    course_code = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Course Code",
                "class": "shadow form-control form-control-user"
            }
        ))
    
    level = forms.ChoiceField(
        choices=Course.LEVEL_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'form-control form-control-select',
                'style': "border-radius: 10rem;padding: 0.5rem 0.5rem;",
                'placeholder': " Choose Level",
            }
        ))

    class Meta:
        model = Course
        fields = ['course_title', 'course_code', 'level']



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

