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
