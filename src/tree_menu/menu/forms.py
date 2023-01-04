from urllib.parse import urlsplit, urlunsplit

from django.forms import URLField, ModelForm

from tree_menu.menu.models import Menu


class TrailingSlashURLField(URLField):

    def to_python(self, value: str) -> str:
        path: list = list(urlsplit(super().to_python(value)))
        splited_path: list = path[2].split('/')
        if splited_path[-1]:
            splited_path.append('')
            path[2] = '/'.join(splited_path)
        trailing_slash_value = urlunsplit(path)
        return trailing_slash_value


class MenuForm(ModelForm):
    url = TrailingSlashURLField()

    class Meta:
        model = Menu
        fields = ('name', 'parent')
