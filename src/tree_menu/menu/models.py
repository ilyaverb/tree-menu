from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name

    def get_parents_id(self) -> list:
        return [self.parent_id] + self.parent.get_parents_id() if self.parent else []
