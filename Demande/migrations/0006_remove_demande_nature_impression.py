# Generated by Django 4.1 on 2023-12-17 12:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Demande", "0005_nature_impression_alter_statut_options_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="demande",
            name="nature_impression",
        ),
    ]
