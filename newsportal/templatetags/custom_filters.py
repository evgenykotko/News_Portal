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
        string2 = text.lower()

        flag = 0
        for j in stopword:
            if not string2 in j:
                flag += 1
            if string2 == j:
                censored_text += block * len(text)
                flag -= 1
                text = ''

        if flag == ln:
            censored_text += text
            text = ''

    if string2 != '' and string2 not in stopword:
        censored_text += text
    elif string2 != '':
        censored_text += block * len(text)

    return censored_text