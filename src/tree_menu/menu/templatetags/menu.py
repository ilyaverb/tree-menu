from django import template
from django.shortcuts import get_object_or_404

from tree_menu.menu.models import Menu

register = template.Library()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, name):
    menu = get_object_or_404(Menu, name=name)
    absolute_uri = context.get('request').build_absolute_uri()
    if absolute_uri:
        active_menu = Menu.objects.get(url=absolute_uri)
        activated_menu_ids = [active_menu]
        return {'active_menu_ids': activated_menu_ids.append(active_menu.get_parents_id()), 'menu': menu}
    return {'menu': menu}
