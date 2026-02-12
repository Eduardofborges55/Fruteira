from django.db import models

class Fruta(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    validade = models.DateField()

    def __str__(self):
        return self.nome
