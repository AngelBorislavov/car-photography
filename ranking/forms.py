from django import forms


class RatingForm(forms.Form):
    score = forms.TypedChoiceField(
        choices=[(score, str(score)) for score in range(1, 6)],
        coerce=int,
        widget=forms.Select,
        label="Rate",
    )