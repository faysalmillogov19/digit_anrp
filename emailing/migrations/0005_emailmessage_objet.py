# Generated by Django 4.1 on 2023-12-08 16:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("emailing", "0004_alter_emailmessage_type_demande"),
    ]

    operations = [
        migrations.AddField(
            model_name="emailmessage",
            name="objet",
            field=models.TextField(null=True),
        ),
    ]
