from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("estoque", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RegraFruta",
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
                ("nome_fruta", models.CharField(max_length=100, unique=True)),
                ("dias_para_promocao", models.PositiveSmallIntegerField(default=4)),
                ("dias_para_apodrecer", models.PositiveSmallIntegerField(default=4)),
                (
                    "dias_ate_descarte_apos_apodrecer",
                    models.PositiveSmallIntegerField(default=3),
                ),
            ],
            options={
                "ordering": ["nome_fruta"],
                "verbose_name": "Regra de fruta",
                "verbose_name_plural": "Regras de frutas",
            },
        ),
        migrations.AddField(
            model_name="fruta",
            name="data_chegada",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="fruta",
            name="data_descarte",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="fruta",
            name="data_inicio_apodrecimento",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="fruta",
            name="data_promocao",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="fruta",
            name="preco_atual",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="fruta",
            name="preco_normal",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="fruta",
            name="preco_promocional",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name="fruta",
            name="status_ciclo",
            field=models.CharField(
                choices=[
                    ("disponivel", "Disponivel"),
                    ("promocao", "Promocao"),
                    ("apodrecendo", "Apodrecendo"),
                    ("descartada", "Descartada"),
                ],
                default="disponivel",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="fruta",
            name="validade",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterModelOptions(
            name="fruta",
            options={
                "ordering": ["nome", "data_chegada"],
                "verbose_name": "Fruta",
                "verbose_name_plural": "Frutas",
            },
        ),
    ]
