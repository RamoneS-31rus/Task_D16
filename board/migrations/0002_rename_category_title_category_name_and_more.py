# Generated by Django 4.2.4 on 2023-08-28 07:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("board", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="category",
            old_name="category_title",
            new_name="name",
        ),
        migrations.RenameField(
            model_name="comment",
            old_name="comment_time",
            new_name="date",
        ),
        migrations.RenameField(
            model_name="comment",
            old_name="comment_post",
            new_name="post",
        ),
        migrations.RenameField(
            model_name="comment",
            old_name="comment_status",
            new_name="status",
        ),
        migrations.RenameField(
            model_name="comment",
            old_name="comment_text",
            new_name="text",
        ),
        migrations.RenameField(
            model_name="comment",
            old_name="comment_user",
            new_name="user",
        ),
        migrations.RenameField(
            model_name="post",
            old_name="post_category",
            new_name="category",
        ),
        migrations.RenameField(
            model_name="post",
            old_name="post_time",
            new_name="date",
        ),
        migrations.RenameField(
            model_name="post",
            old_name="post_text",
            new_name="text",
        ),
        migrations.RenameField(
            model_name="post",
            old_name="post_title",
            new_name="title",
        ),
        migrations.RenameField(
            model_name="post",
            old_name="post_user",
            new_name="user",
        ),
        migrations.AlterField(
            model_name="category",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="comment",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="post",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
