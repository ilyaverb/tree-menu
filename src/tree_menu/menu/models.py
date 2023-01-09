from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    url = models.CharField(max_length=255, unique=True, blank=True,
                           validators=[RegexValidator(regex=r"^/?(([.a-zA-Z0-9-])+(/){,1})*$")])
    named_url = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.url:
            self.url = self.name
        super().save(*args, **kwargs)

    def get_parents_id(self) -> list:
        return [self.parent_id] + self.parent.get_parents_id() if self.parent else []

    def get_url(self):
        return reverse(self.named_url) if self.named_url else self.url
