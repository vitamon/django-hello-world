from django import template
from hello.util.utils import admin_page_url

register = template.Library()

class EditLinkNode(template.Node):
    def __init__(self, anything, *args):
        self.anything = template.Variable(anything)

    def render(self, context):
        try:
            item = self.anything.resolve(context)
            return '<a href="%s">Edit %s</a>' % (admin_page_url(item), item)
        except:
            return '---'


@register.tag
def edit_link(parser, token):
    args = token.split_contents()
    return EditLinkNode(*args[1:])

