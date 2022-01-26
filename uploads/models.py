from django.db import models

CNAB_LINE_LENGHT = 81


class Parser(models.Model):
    text = models.TextField(blank=False, default=None)

    def validate_content(self):
        rows = self.text.split('\n')
        for row in rows:
            if len(row) != CNAB_LINE_LENGHT:
                return False

        return True
