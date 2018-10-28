from django import forms
from .models import Comment

# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ('title', 'body', 'url', 'icon', 'image')
#         widgets = {
#             'title':forms.TextInput(attrs={'class': 'form-control'}),
#             'body': forms.Textarea(attrs={'class': 'form-control', 'rows':5}),
#             'url': forms.URLInput(attrs={'class': 'form-control'}),
#             'icon': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#             'image': forms.ClearableFileInput(attrs={'class': 'form-control'})
#         }

class CommentForm(forms.Form):
    parent_comment = forms.IntegerField(required=False, widget=forms.HiddenInput())
    receiver = forms.IntegerField(required=False, widget=forms.HiddenInput())
    comment_area = forms.CharField(label="", widget=forms.Textarea(attrs={'class': 'form-control mb-2', 'rows':3}))
