from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from core.settings import DEFAULT_FROM_EMAIL
from .models import Post, Comment


@receiver(post_save, sender=Comment)
def new_comment(sender, instance, created, **kwargs):
    if created:
        post_id = instance.post_id
        user_id = Post.objects.get(pk=post_id).user_id
        email = [User.objects.get(pk=user_id).email]

        url = f"http://127.0.0.1:8000{instance.post.get_absolute_url()}"

        content = render_to_string(
            "board/email/comment_new.html",
            {
                "title": instance.post,
                "url": url,
            },
        )

        msg = EmailMultiAlternatives(
            subject=f"На Ваше объявление откликнулись.",
            from_email=DEFAULT_FROM_EMAIL,
            to=email,
        )
        msg.attach_alternative(content, "text/html")
        msg.send()


@receiver(post_save, sender=Comment)
def comment_status(sender, instance, **kwargs):
    user_id = instance.user_id
    email = [User.objects.get(pk=user_id).email]

    if instance.status is not None:
        if instance.status:
            status = "принят"
        else:
            status = "отклонён"

        url = f"http://127.0.0.1:8000{instance.post.get_absolute_url()}"

        content = render_to_string(
            "board/email/comment_status.html",
            {
                "title": instance.post,
                "url": url,
                "status": status,
            },
        )

        msg = EmailMultiAlternatives(
            subject=f"Статус Вашего запроса изменился.",
            from_email=DEFAULT_FROM_EMAIL,
            to=email,
        )
        msg.attach_alternative(content, "text/html")
        msg.send()
