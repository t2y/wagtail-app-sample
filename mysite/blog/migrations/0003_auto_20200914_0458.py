# Generated by Django 3.1.1 on 2020-09-14 04:58

from django.db import migrations
import wagtailmarkdown.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpage',
            name='body',
            field=wagtailmarkdown.fields.MarkdownField(),
        ),
    ]
