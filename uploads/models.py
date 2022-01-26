from django.db import models

CNAB_LINE_LENGHT = 80


class Parser(models.Model):
    text = models.TextField(blank=False, default=None)

    def validate_content(self):
        rows = self.text.split('\n')
        if self.validate_rows_length(rows):
            return self.validate_tipo_transacao(rows)

        return False

    @staticmethod
    def validate_rows_length(rows):
        for row in rows:
            if len(row) != CNAB_LINE_LENGHT:
                return False

        return True

    @staticmethod
    def validate_tipo_transacao(rows):
        for row in rows:
            if row[0] == '0':
                return False

        return True


class Loja(models.Model):
    cpf = models.CharField(max_length=11, default='')
    nome = models.CharField(max_length=19, default='')
    representante = models.CharField(max_length=14, default='')


class Transacao(models.Model):
    tipo = models.IntegerField()
    data = models.DateField()
    hora = models.TimeField()
    valor = models.FloatField()
    loja = models.ForeignKey(Loja, related_name='transacoes',
                             on_delete=models.CASCADE, default=None)


class Cartao(models.Model):
    numero = models.CharField(max_length=12, default='')
    loja = models.ForeignKey(Loja, related_name='cartoes',
                             on_delete=models.CASCADE, default=None)
