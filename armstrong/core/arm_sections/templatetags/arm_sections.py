from ..models import Section
from django.utils.safestring import mark_safe as _
from django import template as djtemplate
from django.template.loader import render_to_string

register = djtemplate.Library()

class SectionMenuNode(djtemplate.Node):
    def __init__(self, 
            template='arm_sections/sections_menu.html',
            section_view=None,
            sections=None):
        # this should go away, it's only here temporarily
        # to make testing easier
        if sections is None:
            sections = Section.objects.all().order_by('tree_id')
        self.sections = sections
        self.template = template
        self.section_view = None

    def render(self, context):
        return render_to_string(self.template,
                djtemplate.Context({'sections':self.sections,
                                    'section_view':self.section_view,
                                    }))

@register.tag(name='section_menu')
def do_section_menu(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name = token.split_contents()
    except ValueError:
        raise djtemplate.TemplateSyntaxError("%r tag requires a single argument" % token.contents.split()[0])
    return SectionMenuNode()
