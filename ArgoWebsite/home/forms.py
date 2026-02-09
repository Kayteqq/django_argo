from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        labels = kwargs.pop('custom_labels', {})
        super().__init__(*args, **kwargs)


        if labels:
            self.fields['name'].label = labels.get('name')
            self.fields['email'].label = labels.get('email')
            self.fields['phone'].label = labels.get('phone')
            self.fields['message'].label = labels.get('message')