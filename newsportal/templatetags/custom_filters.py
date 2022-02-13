from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='multiply')

def multiply(value, arg):
    if isinstance(value, str) and isinstance(arg, int):
        return str(value) * arg
    else:
        raise ValueError(
            f'Нельзя умножить {type(value)} на {type(arg)}')


@register.filter(name='censor')
@stringfilter
def censor(value):
    stopword = ['бес', 'вид', 'ами', 'ние']
    ln = len(stopword)
    censored_text = ''
    text = ''
    block = '*'
    for i in value:
        text += i
        lowtext = text.lower()

        flag = 0
        for j in stopword:
            if not lowtext in j:
                flag += 1
            if lowtext == j:
                censored_text += block * len(text)
                flag -= 1
                text = ''

        if flag == ln:
            censored_text += text
            text = ''

    if lowtext != '' and lowtext not in stopword:
        censored_text += text
    elif lowtext != '':
        censored_text += block * len(text)

    return censored_text