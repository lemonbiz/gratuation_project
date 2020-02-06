from django import template

register = template.Library()

'''这些是模板过滤器，他们的⼯作⽅式是这样的：
⾸先，我们将它加载到模板中，就像我们使⽤ widget_tweaks 或static 模板
标签⼀样。请注意，在创建这个⽂件后，你将不得不⼿动停⽌开发服务器并
重启它，以便Django可以识别新的模板标签。'''


@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__


@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'is-invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'is-valid'
    return 'form-control {}'.format(css_class)
