from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget= forms.PasswordInput(attrs={'placeholder':'Enter Password',
        'class':'form-controle',
        }))
    conform_password = forms.CharField(widget= forms.PasswordInput(attrs={'placeholder':'Enter Password'}))
    
    class Meta:
        model = Account
        fields = ['first_name', 'last_name','phone_number','password','email']
    
    def __init__(self, *args,**kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['plaseholder']='Enter First name'
        self.fields['last_name'].widget.attrs['plaseholder']='Enter Last name'
        self.fields['phone_number'].widget.attrs['plaseholder']='Enter Phone number'
        self.fields['email'].widget.attrs['plaseholder']='Enter Email Address'
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'