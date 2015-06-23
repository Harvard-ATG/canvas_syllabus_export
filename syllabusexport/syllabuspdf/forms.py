from django import forms

class SettingsForm(forms.Form):
	syllabus = forms.BooleanField(label="Syllabus", initial=True, required=False)
	dated_events = forms.BooleanField(label="Dated Events", initial=True, required=False)
	undated_events = forms.BooleanField(label="Undated Events", initial=False, required=False)
	descriptions = forms.BooleanField(label="Event Descriptions", initial=False, required=False)
	times = forms.BooleanField(label="Event Times", initial=True, required=False)
	weights = forms.BooleanField(label="Assignment Weights", initial=True, required=False)
	hidden_field = forms.CharField(widget=forms.HiddenInput(), initial='field', required=False)

	