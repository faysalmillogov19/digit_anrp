# Generated by Django 4.1 on 2023-12-18 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Demande", "0007_signataire"),
        ("ASE", "0002_rename_certicat_bonne_pratique_ase_code_facture_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="ase",
            name="nature_impression",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="Demande.nature_impression",
            ),
        ),
    ]
