from django.db import models


class Parser(models.Model):
    text = models.TextField(blank=False, default=None)
