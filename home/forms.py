from django import forms

DOOR_SIDE_CHOICES = (
    ("left", "left"),
    ("right", "right"),
    ("both", "both"),
)

SIDE_LIMIT_CHOICES = (
    ("left", "left"),
    ("right", "right"),
    ("both", "both"),
    ("", ""),
)

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

class ContactFormConfig(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False)
    message = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        labels = kwargs.pop('custom_labels', {})
        super().__init__(*args, **kwargs)


        if labels:
            self.fields['name'].label = labels.get('name')
            self.fields['email'].label = labels.get('email')
            self.fields['phone'].label = labels.get('phone')
            self.fields['message'].label = labels.get('message')



class ConfigForm(forms.Form):

    # --- krótkie stringi (<50 znaków)
    styleLine = forms.CharField(max_length=50)
    usecase = forms.CharField(max_length=50)
    type = forms.CharField(max_length=50)
    additivies = forms.CharField(max_length=50)
    color1 = forms.CharField(max_length=50)
    color2 = forms.CharField(max_length=50)
    smart = forms.CharField(max_length=255)

    # --- konfiguracja drzwi
    sideLimitation = forms.ChoiceField(
        choices=SIDE_LIMIT_CHOICES,
        required=False
    )

    doorSide = forms.ChoiceField(
        choices=DOOR_SIDE_CHOICES
    )

    # --- checkboxy
    leftWindowEnabled = forms.BooleanField(required=False)
    rightWindowEnabled = forms.BooleanField(required=False)
    topWindowEnabled = forms.BooleanField(required=False)

    # --- zakresy z Alpine (range input)
    productWidth = forms.IntegerField(min_value=2, max_value=10)
    productHeight = forms.IntegerField(min_value=4, max_value=20)
    doorWidth = forms.IntegerField(min_value=2, max_value=10)
    rightWidth = forms.IntegerField(min_value=1, max_value=10)
    leftWidth = forms.IntegerField(min_value=1, max_value=10)

    # --- WALIDACJA LOGIKI BIZNESOWEJ
    def clean(self):
        cleaned = super().clean()

        total_width = cleaned.get("productWidth")
        door_width = cleaned.get("doorWidth")
        right_width = cleaned.get("rightWidth", 0)
        left_width = cleaned.get("leftWidth", 0)

        right_enabled = cleaned.get("rightWindowEnabled")
        left_enabled = cleaned.get("leftWindowEnabled")
        top_enabled = cleaned.get("topWindowEnabled")

        # okna wyłączone = szerokość 0
        if not right_enabled:
            cleaned["rightWidth"] = 0

        if not left_enabled:
            cleaned["leftWidth"] = 0

        # walidacja geometrii
        if total_width and door_width:
            calculated = door_width + cleaned.get("rightWidth", 0) + cleaned.get("leftWidth", 0)

            if calculated > total_width:
                raise forms.ValidationError(
                    "Suma szerokości przekracza szerokość produktu."
                )

        return cleaned