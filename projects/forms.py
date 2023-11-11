from django.forms import ModelForm
from .models import Project, Reviews
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'title',
            'featured_image',
            'description',
            'demo_link',
            'source_link',
        ]
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for fieldKey, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Reviews
        fields = ['value', 'body']

        labels = {
            'value': 'Palce yor voute',
            'body': 'Add a comment with your code'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for fieldKey, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
