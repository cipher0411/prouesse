from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, SetPasswordForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Profile
from django.utils.translation import gettext_lazy as _
from .models import Contact

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Check if profile exists, if not, create one
            if not Profile.objects.filter(user=user).exists():
                Profile.objects.create(user=user)

            # Log the user in after signing up
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')  # Use password1, not password
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                # Add a success message
                messages.success(request, 'You have successfully created an account and logged in!')
                return redirect('core:profile')  # Redirect to the profile page after login
            else:
                messages.error(request, 'Invalid username or password after signup.')
                return redirect('core:signup')  # Redirect back to signup page if login fails
    else:
        form = SignupForm()
    return render(request, 'core/signup.html', {'form': form})




class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'phone', 'service', 'message']
    
    
    


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=254)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No user is associated with this email address.")
        return email


class PasswordResetForm(forms.Form):
    email = forms.EmailField()

class SetPasswordForm(SetPasswordForm):
    pass


COUNTRY_CHOICES = (
    ('', 'Select Country'),
    ('UK', 'United Kingdom'),
    ('AF', 'Afghanistan'),
    ('AL', 'Albania'),
    ('DZ', 'Algeria'),
    ('AD', 'Andorra'),
    ('AO', 'Angola'),
    ('AG', 'Antigua and Barbuda'),
    ('AR', 'Argentina'),
    ('AM', 'Armenia'),
    ('AU', 'Australia'),
    ('AT', 'Austria'),
    ('AZ', 'Azerbaijan'),
    ('BS', 'Bahamas'),
    ('BH', 'Bahrain'),
    ('BD', 'Bangladesh'),
    ('BB', 'Barbados'),
    ('BY', 'Belarus'),
    ('BE', 'Belgium'),
    ('BZ', 'Belize'),
    ('BJ', 'Benin'),
    ('BT', 'Bhutan'),
    ('BO', 'Bolivia'),
    ('BA', 'Bosnia and Herzegovina'),
    ('BW', 'Botswana'),
    ('BR', 'Brazil'),
    ('BN', 'Brunei'),
    ('BG', 'Bulgaria'),
    ('BF', 'Burkina Faso'),
    ('BI', 'Burundi'),
    ('CI', 'Côte d\'Ivoire'),
    ('CV', 'Cabo Verde'),
    ('KH', 'Cambodia'),
    ('CM', 'Cameroon'),
    ('CA', 'Canada'),
    ('CF', 'Central African Republic'),
    ('TD', 'Chad'),
    ('CL', 'Chile'),
    ('CN', 'China'),
    ('CO', 'Colombia'),
    ('KM', 'Comoros'),
    ('CG', 'Congo (Congo-Brazzaville)'),
    ('CR', 'Costa Rica'),
    ('HR', 'Croatia'),
    ('CU', 'Cuba'),
    ('CY', 'Cyprus'),
    ('CZ', 'Czechia'),
    ('CD', 'Democratic Republic of the Congo'),
    ('DK', 'Denmark'),
    ('DJ', 'Djibouti'),
    ('DM', 'Dominica'),
    ('DO', 'Dominican Republic'),
    ('EC', 'Ecuador'),
    ('EG', 'Egypt'),
    ('SV', 'El Salvador'),
    ('GQ', 'Equatorial Guinea'),
    ('ER', 'Eritrea'),
    ('EE', 'Estonia'),
    ('SZ', 'Eswatini'),
    ('ET', 'Ethiopia'),
    ('FJ', 'Fiji'),
    ('FI', 'Finland'),
    ('FR', 'France'),
    ('GA', 'Gabon'),
    ('GM', 'Gambia'),
    ('GE', 'Georgia'),
    ('DE', 'Germany'),
    ('GH', 'Ghana'),
    ('GR', 'Greece'),
    ('GD', 'Grenada'),
    ('GT', 'Guatemala'),
    ('GN', 'Guinea'),
    ('GW', 'Guinea-Bissau'),
    ('GY', 'Guyana'),
    ('HT', 'Haiti'),
    ('VA', 'Holy See'),
    ('HN', 'Honduras'),
    ('HU', 'Hungary'),
    ('IS', 'Iceland'),
    ('IN', 'India'),
    ('ID', 'Indonesia'),
    ('IR', 'Iran'),
    ('IQ', 'Iraq'),
    ('IE', 'Ireland'),
    ('IL', 'Israel'),
    ('IT', 'Italy'),
    ('JM', 'Jamaica'),
    ('JP', 'Japan'),
    ('JO', 'Jordan'),
    ('KZ', 'Kazakhstan'),
    ('KE', 'Kenya'),
    ('KI', 'Kiribati'),
    ('KW', 'Kuwait'),
    ('KG', 'Kyrgyzstan'),
    ('LA', 'Laos'),
    ('LV', 'Latvia'),
    ('LB', 'Lebanon'),
    ('LS', 'Lesotho'),
    ('LR', 'Liberia'),
    ('LY', 'Libya'),
    ('LI', 'Liechtenstein'),
    ('LT', 'Lithuania'),
    ('LU', 'Luxembourg'),
    ('MG', 'Madagascar'),
    ('MW', 'Malawi'),
    ('MY', 'Malaysia'),
    ('MV', 'Maldives'),
    ('ML', 'Mali'),
    ('MT', 'Malta'),
    ('MH', 'Marshall Islands'),
    ('MR', 'Mauritania'),
    ('MU', 'Mauritius'),
    ('MX', 'Mexico'),
    ('FM', 'Micronesia'),
    ('MD', 'Moldova'),
    ('MC', 'Monaco'),
    ('MN', 'Mongolia'),
    ('ME', 'Montenegro'),
    ('MA', 'Morocco'),
    ('MZ', 'Mozambique'),
    ('MM', 'Myanmar'),
    ('NA', 'Namibia'),
    ('NR', 'Nauru'),
    ('NP', 'Nepal'),
    ('NL', 'Netherlands'),
    ('NZ', 'New Zealand'),
    ('NI', 'Nicaragua'),
    ('NE', 'Niger'),
    ('NG', 'Nigeria'),
    ('KP', 'North Korea'),
    ('MK', 'North Macedonia'),
    ('NO', 'Norway'),
    ('OM', 'Oman'),
    ('PK', 'Pakistan'),
    ('PW', 'Palau'),
    ('PA', 'Panama'),
    ('PG', 'Papua New Guinea'),
    ('PY', 'Paraguay'),
    ('PE', 'Peru'),
    ('PH', 'Philippines'),
    ('PL', 'Poland'),
    ('PT', 'Portugal'),
    ('QA', 'Qatar'),
    ('RO', 'Romania'),
    ('RU', 'Russia'),
    ('RW', 'Rwanda'),
    ('KN', 'Saint Kitts and Nevis'),
    ('LC', 'Saint Lucia'),
    ('VC', 'Saint Vincent and the Grenadines'),
    ('WS', 'Samoa'),
    ('SM', 'San Marino'),
    ('ST', 'Sao Tome and Principe'),
    ('SA', 'Saudi Arabia'),
    ('SN', 'Senegal'),
    ('RS', 'Serbia'),
    ('SC', 'Seychelles'),
    ('SL', 'Sierra Leone'),
    ('SG', 'Singapore'),
    ('SK', 'Slovakia'),
    ('SI', 'Slovenia'),
    ('SB', 'Solomon Islands'),
    ('SO', 'Somalia'),
    ('ZA', 'South Africa'),
    ('KR', 'South Korea'),
    ('SS', 'South Sudan'),
    ('ES', 'Spain'),
    ('LK', 'Sri Lanka'),
    ('SD', 'Sudan'),
    ('SR', 'Suriname'),
    ('SE', 'Sweden'),
    ('CH', 'Switzerland'),
    ('SY', 'Syria'),
    ('TJ', 'Tajikistan'),
    ('TZ', 'Tanzania'),
    ('TH', 'Thailand'),
    ('TL', 'Timor-Leste'),
    ('TG', 'Togo'),
    ('TO', 'Tonga'),
    ('TT', 'Trinidad and Tobago'),
    ('TN', 'Tunisia'),
    ('TR', 'Turkey'),
    ('TM', 'Turkmenistan'),
    ('TV', 'Tuvalu'),
    ('UG', 'Uganda'),
    ('UA', 'Ukraine'),
    ('AE', 'United Arab Emirates'),
    ('US', 'United States of America'),
    ('UY', 'Uruguay'),
    ('UZ', 'Uzbekistan'),
    ('VU', 'Vanuatu'),
    ('VE', 'Venezuela'),
    ('VN', 'Vietnam'),
    ('YE', 'Yemen'),
    ('ZM', 'Zambia'),
    ('ZW', 'Zimbabwe'),
)

class UserUpdateForm(UserChangeForm):
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your phone number',
        'class': 'form-control'
    }), required=False)
    
    address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your address',
        'class': 'form-control'
    }), required=False)
    
    city = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your city',
        'class': 'form-control'
    }), required=False)

    postcode = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your postcode or ZIP code',
        'class': 'form-control'
    }), required=False)

    country = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your country',
        'class': 'form-control'
    }), required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'phone', 'address', 'city', 'postcode', 'country')

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'form-control'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your first name',
        'class': 'form-control'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your last name',
        'class': 'form-control'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'form-control'
    }))
    password = forms.CharField(label="Password", strip=False, required=False, widget=forms.PasswordInput(attrs={
        'autocomplete': 'new-password',
        'class': 'form-control'
    }))

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password or None


        
        
        
        
        

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('address', 'city', 'postcode', 'country')
        widgets = {
            'address': forms.TextInput(attrs={
                'placeholder': 'Your address',
                'class': 'form-control'
            }),
            'city': forms.TextInput(attrs={
                'placeholder': 'Your city',
                'class': 'form-control'
            }),
            'postcode': forms.TextInput(attrs={
                'placeholder': 'Your postcode',
                'class': 'form-control'
            }),
            'country': forms.Select(choices=COUNTRY_CHOICES, attrs={
                'class': 'form-control'
            }),
        }
        
        
        
        
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'form-control'
    }))

    def clean(self):
        super().clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

            if user and user.check_password(password):
                self.user = user
            else:
                raise forms.ValidationError("Invalid username or password.")

        return self.cleaned_data


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Your first name',
        'class': 'form-control'
    }))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Your last name',
        'class': 'form-control'
    }))
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'form-control'
    }))
    terms_accepted = forms.BooleanField(label='I accept the terms and conditions', required=True, widget=forms.CheckboxInput(attrs={
        'class': 'form-check-input'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'terms_accepted')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Your username',
            'class': 'form-control'
        })
        self.fields['password1'].widget.attrs.update({
            'autocomplete': 'off',
            'class': 'form-control'
        })
        self.fields['password2'].widget.attrs.update({
            'autocomplete': 'off',
            'class': 'form-control'
        })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("This username is already taken. Please choose a different one."))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("This email address is already registered. Please use a different one."))
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create Profile for the user if not exists
            if not Profile.objects.filter(user=user).exists():
                Profile.objects.create(user=user)
        return user
    
    

        
        
        
class AccountDeleteForm(forms.Form):
    confirm_email = forms.EmailField(label="Enter your email to confirm", required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    reason_for_deletion = forms.CharField(label="Reason for deletion", required=True, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'rows': 3,
        'placeholder': 'Please specify your reason for deleting your account'
    }))
    confirm_deletion = forms.BooleanField(label="I confirm that I want to delete my account", required=True)
    
    
    
    
class AccountDeletionForm(forms.Form):
    REASON_CHOICES = [
        ('Not satisfied with service', 'Not satisfied with service'),
        ('Found another platform', 'Found another platform'),
        ('Privacy concerns', 'Privacy concerns'),
        ('Other', 'Other'),
    ]

    reason = forms.ChoiceField(choices=REASON_CHOICES, widget=forms.RadioSelect)



class AccountDeletionForm(forms.Form):
    REASON_CHOICES = [
        ('Not satisfied with service', 'Not satisfied with service'),
        ('Found another platform', 'Found another platform'),
        ('Privacy concerns', 'Privacy concerns'),
        ('Other', 'Other'),
    ]
    
    confirm_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}))
    reason_for_deletion = forms.ChoiceField(choices=REASON_CHOICES, widget=forms.RadioSelect)
    confirm_deletion = forms.BooleanField(label="I confirm that I want to delete my account", required=True)