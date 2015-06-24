from django import forms

class SettingsForm(forms.Form):
	syllabus = forms.BooleanField(label="Syllabus Description", initial=True, required=False, label_suffix='')
	dated_events = forms.BooleanField(label="Dated", initial=True, required=False, label_suffix='')
	undated_events = forms.BooleanField(label="Undated", initial=False, required=False, label_suffix='')
	descriptions = forms.BooleanField(label="Descriptions", initial=False, required=False, label_suffix='')
	times = forms.BooleanField(label="Times", initial=True, required=False, label_suffix='')
	weights = forms.BooleanField(label="Assignment Group Weights", initial=True, required=False, label_suffix='')
	hidden_field = forms.CharField(widget=forms.HiddenInput(), initial="viewed", required=False, label_suffix='')

	