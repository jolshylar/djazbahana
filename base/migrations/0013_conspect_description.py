# Generated by Django 4.0.4 on 2022-06-15 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0012_user_balance"),
    ]

    operations = [
        migrations.AddField(
            model_name="conspect",
            name="description",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]