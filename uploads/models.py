from django.db import models

CNAB_LINE_LENGHT = 80
TIPO_START = 0
DATA_START = 1
VALOR_START = 9
CPF_START = 19
CARTAO_START = 30
HORA_START = 42
REPR_START = 48
LOJA_START = 62
LOJA_END = 81


class Parser(models.Model):
    text = models.TextField(blank=False, default=None)

    def validate_content(self):
        self.remove_trailling_eol()
        rows = self.text.split('\n')
        if self.validate_rows_length(rows):
            return self.validate_tipo_transacao(rows)

        return False

    def remove_trailling_eol(self):
        if self.text[-1] == '\n':
            self.text = self.text[:-1]

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

    def save_data(self):
        rows = self.text.split('\n')
        for row in rows:
            self.parse_and_save(row)

    def parse_and_save(self, row):
        tipo = row[TIPO_START:DATA_START]
        data = row[DATA_START:VALOR_START]
        valor = row[VALOR_START:CPF_START]
        cpf = row[CPF_START:CARTAO_START]
        cartao = row[CARTAO_START:HORA_START]
        hora = row[HORA_START:REPR_START]
        representante_loja = row[REPR_START:LOJA_START]
        nome_loja = row[LOJA_START:LOJA_END]

        loja = self.get_or_create_loja(cpf, nome_loja, representante_loja)
        self.get_or_create_cartao(cartao, loja)
        self.create_transacao(tipo, data, hora, valor, loja)

    @staticmethod
    def get_or_create_loja(cpf, nome, representante):
        nome = ' '.join(nome.split())
        representante = ' '.join(representante.split())
        try:
            loja = Loja.objects.get(cpf=cpf)
            loja.nome = nome
            loja.representante = representante
        except Loja.DoesNotExist:
            loja = Loja(cpf=cpf, representante=representante, nome=nome)

        loja.save()

        return loja

    @staticmethod
    def get_or_create_cartao(cartao, loja):
        try:
            cartao = loja.cartoes.get(numero=cartao)
        except Cartao.DoesNotExist:
            cartao = Cartao(numero=cartao, loja=loja)

        cartao.save()
    
    @staticmethod
    def create_transacao(tipo, data, hora, valor, loja):
        data = f'{data[0:4]}-{data[4:6]}-{data[6:8]}'
        hora = f'{hora[0:2]}:{hora[2:4]}:{hora[4:6]}'
        valor = valor.lstrip('0')
        valor = float(valor) / 100

        Transacao.objects.create(tipo=int(tipo), data=data, hora=hora,
                                 valor=valor, loja=loja)


class Loja(models.Model):
    cpf = models.CharField(max_length=11, default='', unique=True)
    nome = models.CharField(max_length=19, default='')
    representante = models.CharField(max_length=14, default='')


class Transacao(models.Model):
    tipo = models.IntegerField()
    data = models.DateField()
    hora = models.TimeField()
    valor = models.FloatField()
    loja = models.ForeignKey(Loja, related_name='transacoes',
                             on_delete=models.CASCADE, default=None)

    @classmethod
    def get_balance(cls):
        result = 0
        for transacao in cls.objects.all():
            result += cls.sum_transacao(transacao)

        return result

    @staticmethod
    def sum_transacao(transacao):
        if transacao.tipo in [1, 4, 5, 6, 7, 8]:
            return transacao.valor
        else:
            return -transacao.valor


class Cartao(models.Model):
    numero = models.CharField(max_length=12, default='')
    loja = models.ForeignKey(Loja, related_name='cartoes',
                             on_delete=models.CASCADE, default=None)
