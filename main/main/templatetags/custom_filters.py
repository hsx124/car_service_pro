from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    获取字典中指定键的值
    用法: {{ my_dict|get_item:key }}
    """
    return dictionary.get(key) 