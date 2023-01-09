from django.core.validators import RegexValidator
from django.forms import CharField, ModelForm

from tree_menu.menu.models import Menu


class TrailingSlashURLField(CharField):
    default_validators = [RegexValidator(regex=r"^/?(([.a-zA-Z0-9-])+(/){,1})*$")]

    def to_python(self, value: str) -> str:
        splited_path: list = super().to_python(value).split('/')
        if splited_path[-1]:
            splited_path.append('')
        return '/'.join(splited_path)


class MenuForm(ModelForm):
    url = TrailingSlashURLField(required=False)

    class Meta:
        model = Menu
        fields = ('name', 'parent', 'named_url', 'url')
