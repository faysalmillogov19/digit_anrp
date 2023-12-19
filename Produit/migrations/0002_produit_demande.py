# Generated by Django 4.1 on 2023-11-24 00:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("Demande", "0001_initial"),
        ("Produit", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Produit_demande",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("dc", models.CharField(max_length=250, null=True)),
                ("dci", models.CharField(max_length=250, null=True)),
                ("forme", models.CharField(max_length=50)),
                ("dosage", models.IntegerField(null=True)),
                ("presentation", models.TextField(null=True)),
                ("quantite", models.IntegerField(null=True)),
                ("cout", models.IntegerField(null=True)),
                ("amm", models.BooleanField(default=False)),
                (
                    "categorie",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Produit.categorie",
                    ),
                ),
                (
                    "demande",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Demande.demande",
                    ),
                ),
            ],
        ),
    ]