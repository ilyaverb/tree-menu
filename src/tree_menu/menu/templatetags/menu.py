from django import template
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from tree_menu.menu.models import Menu

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, name: str) -> dict:
    menu = get_object_or_404(Menu, name=name)
    absolute_uri = context.get('request').build_absolute_uri()
    menu_context = {'menu': menu}
    if absolute_uri:
        try:
            active_menu = Menu.objects.get(url=absolute_uri)
            activated_menu_ids = [active_menu.id] + active_menu.get_parents_id()
        except ObjectDoesNotExist:
            activated_menu_ids = []
        menu_context.update({'active_menu_ids': activated_menu_ids})
    return menu_context
