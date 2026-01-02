from django import forms
from .models import Contact
from .models import JobApplication

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "What's your name"
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': "Your Email"
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': "Tell us about your project",
                'rows': 4
            }),
        }
        
class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['first_name', 'last_name', 'phone', 'email', 'how_hear', 'cv']

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv:
            # Restrict to PDF
            if not cv.name.lower().endswith('.pdf'):
                raise forms.ValidationError("Only PDF files are accepted.")
            # Restrict file size
            if cv.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Maximum file size is 2 MB.")
        return cv