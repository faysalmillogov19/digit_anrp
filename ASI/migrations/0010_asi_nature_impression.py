# Generated by Django 4.1 on 2023-12-17 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Demande", "0006_remove_demande_nature_impression"),
        ("ASI", "0009_alter_asi_certicat_bonne_pratique_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="asi",
            name="nature_impression",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Demande.nature_impression",
            ),
        ),
    ]
