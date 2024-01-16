from django import forms
from movie.models import Review, RATE_OPCIONES


class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textarea'}), required=True)
    rate = forms.ChoiceField(choices=RATE_OPCIONES, widget=forms.Select(), required=True)

    class Meta:
        model = Review
        fields = ('text', 'rate')
