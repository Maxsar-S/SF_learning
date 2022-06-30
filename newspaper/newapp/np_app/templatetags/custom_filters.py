
from django import template


register = template.Library()


@register.filter()
def censor(value):
    cens_list = ['редиска', 'РЕДИСКА', 'Редиска']
    for word in cens_list:
        if word.find(value):
            value = value.replace(word[1::], "*" * (len(word) - 1))
    return f'{value}'


