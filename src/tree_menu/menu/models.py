from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse


class Menu(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    url = models.CharField(max_length=255, blank=True, null=True, unique=True,
                           validators=[RegexValidator(regex=r"^/?(([.a-zA-Z0-9-])+(/){,1})*$")])
    named_url = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     if not (self.url and self.named_url):
    #         self.url = self.get_full_path()
    #     super().save(*args, **kwargs)

    def get_full_path(self):
        return self.parent.get_url() + self.get_url() if self.parent else '/{}'.format(self.get_url())

    def get_parents_id(self) -> list:
        return [self.parent_id] + self.parent.get_parents_id() if self.parent else []

    def get_url(self) -> str:
        return reverse(self.named_url) if self.named_url else self.url
