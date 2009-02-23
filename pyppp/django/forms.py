from django import forms
from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.contrib.auth import authenticate, REDIRECT_FIELD_NAME
from django.contrib.formtools.wizard import FormWizard

from pyppp.django import login
from pyppp.django.models import UserPPP

class UserFormBase(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(UserFormBase, self).__init__(*args, **kwargs)
    
    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None
    
    def get_user(self):
        return self.user_cache

class AuthenticationForm(UserFormBase):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            
            if self.user_cache is None:
                raise forms.ValidationError('Please enter a correct username and password. Note that both fields are case-sensitive.')
            elif not self.user_cache.is_active:
                raise forms.ValidationError('This account is inactive')
        
        return self.cleaned_data

class PasscodeForm(UserFormBase):
    username = forms.CharField(max_length=30)
    passcode = forms.CharField(max_length=4)
    card = forms.CharField(max_length=8)
    code = forms.CharField(max_length=8)
    
    def __init__(self, *args, **kwargs):
        super(PasscodeForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['card'].widget.attrs['readonly'] = True
        self.fields['code'].widget.attrs['readonly'] = True
    
    def clean(self):
        if self.user_cache is not None:
            return self.cleaned_data
        
        username = self.cleaned_data.get('username')
        passcode = self.cleaned_data.get('passcode')
        
        if username and passcode:
            self.user_cache = authenticate(username=username, passcode=passcode)
            if self.user_cache is None:
                raise forms.ValidationError('Incorrect passcode.')
        
        return self.cleaned_data

class LoginWizard(FormWizard):
    def parse_params(self, request, *args, **kwargs):
        current_step = self.determine_step(request, *args, **kwargs)
        if request.method == 'POST' and current_step == 0:
            request.session.set_test_cookie()
            form = self.get_form(current_step, request.POST)
            if form.is_valid():
                ppp, created = UserPPP.objects.get_or_create(user=form.user_cache)
                passcode_info = ppp.get_current_sequence_info()
                self.initial[(current_step + 1)] = {
                    'username': form.cleaned_data.get('username'),
                    'card': passcode_info['card'],
                    'code': '%s%s' % (passcode_info['row'], passcode_info['column'])
                }
    
    def get_template(self, step):
        return 'pyppp/form.html'
    
    def done(self, request, form_list):
        if not request.session.test_cookie_worked():
            print "Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."
        
        redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
        if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        
        login(request, form_list[1].get_user())
        
        return HttpResponseRedirect(redirect_to)
