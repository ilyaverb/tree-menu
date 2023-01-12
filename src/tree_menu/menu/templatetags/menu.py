from django import template
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from tree_menu.menu.models import Menu

register = template.Library()


def recursive_append_children(items, children):
    def recursive_append(items, child):
        for item in items:
            if item['name'] == child.parent.name:
                child_data = {'name': child.name, 'url': child.url, 'children': []}
                item['children'].append(child_data)
                if child_data in items:
                    items.remove(child_data)
            else:
                recursive_append(item['children'], child)

    for child in children:
        recursive_append(items, child)
    return items


def get_all_children_data(children) -> list:
    return [{'name': child.name, 'url': child.get_url(), 'children': []} for child in children]


def get_activated_menu_ids(children, path):
    for child in children:
        if child.get_url() == path:
            return [child.id] + child.get_parents_id()


@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, name: str) -> dict:
    menu = get_object_or_404(Menu.objects.filter(parent=None), name=name)
    path = context.get('request').path
    children = menu.get_all_children(include_self=False)
    all_children_data = get_all_children_data(children)
    activated_menu_ids = [menu.id] if menu.get_url() == path else []
    if not activated_menu_ids:
        activated_menu_ids = get_activated_menu_ids(children, path)
    children: dict = recursive_append_children(all_children_data, children)
    menu_context = {'menu': menu, 'children': children, 'active_menu_ids': activated_menu_ids}
    return menu_context
