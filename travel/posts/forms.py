from django import forms

from .models import Post
from .services import get_countries

countries = get_countries()
CHOICES = [tuple([x, x]) for x in countries]


class PostModelForm(forms.ModelForm):
    tags = forms.CharField(label='tag', required=False)
    countries = forms.CharField(widget=forms.Select(choices=CHOICES))
    class Meta:
        model = Post
        fields = [
            # "user",
            "title",
            # "likes"
        ]



    def clean_title(self):
        title = self.cleaned_data.get("title")
        if len(title) <= 3:
            raise forms.ValidationError(
                "Length has to be more than 3 character"
            )
        return title
