from django import forms

class SettingsForm(forms.Form):
	syllabus = forms.BooleanField(label="Syllabus", initial=True, required=False)
	events = forms.BooleanField(label="Events", initial=True, required=False)
	descriptions = forms.BooleanField(label="Event Descriptions", initial=True, required=False)
	times = forms.BooleanField(label="Event Times", initial=True, required=False)
	weights = forms.BooleanField(label="Weights", initial=True, required=False)

	