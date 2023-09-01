from django.forms import (
    ModelForm,
    Textarea,
    TextInput,
    CharField,
    ModelChoiceField,
    Select,
)

from .models import Category, Post, Comment


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].label = ""

    category = ModelChoiceField(
        label="",
        empty_label="--- Выберите категорию ---",
        queryset=Category.objects.all(),
        widget=Select(attrs={"class": "form-select shadow-none"}),
    )
    title = CharField(
        label="",
        widget=TextInput(
            attrs={
                "class": "form-control shadow-none",
                "placeholder": "Заголовок",
            }
        ),
    )

    class Meta:
        model = Post
        fields = [
            "category",
            "title",
            "text",
        ]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            "text",
        ]

        widgets = {
            "text": Textarea(
                attrs={
                    "class": "form-control shadow-none",
                    "rows": "3",
                },
            ),
        }
