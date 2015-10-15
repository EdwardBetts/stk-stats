# coding=utf-8

import json

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape

register = template.Library()


@register.filter
def mod(value, arg):
    return value % arg


@register.filter
@stringfilter
def has_token(value, token):
    "Returns whether a space-separated list of tokens contains a given token"
    return token in value.split(' ')


@register.filter
@stringfilter
def wrap_at_underscores(value):
    return value.replace('_', '&#x200b;_')


wrap_at_underscores.is_safe = True


@register.filter
@stringfilter
def prettify_json(value):
    try:
        data = json.loads(value)
        return json.dumps(data, indent=2, sort_keys=True)
    except:
        return value


@register.filter
@stringfilter
def glext_spec_link(value):
    c = value.split('_', 2)
    if len(c) < 2:
        return ''
    return 'http://www.opengl.org/registry/specs/%s/%s.txt' % (c[1], c[2])


@register.filter
@stringfilter
def prettify_gl_title(value):
    if value[-4:] in ('_ARB', '_EXT'):
        value = value[:-4]
    if value.startswith('GL_FRAGMENT_PROGRAM_ARB.'):
        value = value[24:] + ' (fragment)'
    if value.startswith('GL_VERTEX_PROGRAM_ARB.'):
        value = value[22:] + ' (vertex)'
    return value


@register.filter
def dictget(value, key):
    return value.get(key, '')


@register.filter
def sorteditems(value):
    # return sorted(value.items(), key = lambda (k, v): k)
    return value.items()


@register.filter
def sorteddeviceitems(value):
    # return sorted(value.items(), key = lambda (k, v): (k['vendor'], k['renderer'], k['os'], v))
    return value.items()


@register.filter
def sortedcpuitems(value):
    # return sorted(value.items(), key = lambda (k, v): (k['x86_vendor'], k['x86_model'], k['x86_family'], k['cpu_identifier']))
    return value.items()


@register.filter
def cpufreqformat(value):
    return mark_safe("%.2f&nbsp;GHz" % (int(value) / 1000000000.0))


@register.filter
def sort(value):
    return sorted(value)


@register.filter
def sortreversed(value):
    return reversed(sorted(value))


@register.filter
def reverse(value):
    return reversed(value)


@register.filter
def format_profile(table):
    cols = table['cols']

    out = []
    for c in cols:
        out.append('<th>%s' % conditional_escape(c))

    def handle(indents, indent, t):
        items = sorted(t.items())

        item_id = 0
        for name, row in items:
            if item_id == len(items) - 1:
                last = True
            else:
                last = False
            item_id += 1

            out.append('<tr>')
            out.append('<td><span class=treemarker>%s%s─%s╴</span>%s' % (
            indent, ('└' if last else '├'), ('┬' if row[0] is not None else '─'), conditional_escape(name)))
            outrow = []
            for c in range(1, len(cols)):
                outrow.append('<td>%s%s' % ('  ' * indents, conditional_escape(row[c])))
            out.append('%s</td>' % ''.join(outrow))
            if row[0] is not None:
                handle(indents + 1, indent + ('  ' if last else '│ '), row[0])

    handle(0, '', table['data'])

    return mark_safe('\n'.join(out))
