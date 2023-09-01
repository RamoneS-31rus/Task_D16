from django_filters import FilterSet, filters
from django.forms import TextInput
from .models import Comment


class CommentFilter(FilterSet):
    post = filters.CharFilter(
        label="",
        field_name="post__title",
        lookup_expr="icontains",
        widget=TextInput(
            attrs={"class": "form-control shadow-none", "placeholder": "Поиск"}
        ),
    )

    class Meta:
        model = Comment
        fields = ["post"]
