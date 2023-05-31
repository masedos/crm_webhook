from django.db import models

# Create your models here.

class Aluno(models.Model):
    NumeroInscricao = models.CharField(blank =True, max_length=10)
    Oferta = models.CharField(blank =True, max_length=50)
    TurnoOfertado = models.CharField(blank =True, max_length=10)
    NomeCompleto = models.CharField(blank =True, max_length=200)

    def __str__(self):
        return self.NumeroInscricao
   