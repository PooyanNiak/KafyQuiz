from django import forms

class QuestionForm(forms.Form):
    a = forms.IntegerField()
    b = forms.IntegerField()
    c = forms.IntegerField()

class SubmitForm(forms.Form):
    value = forms.CharField(max_length=128)