from django import template

register = template.Library()

@register.filter(name='user_in_groups')
def user_in_groups(user, groups):
    return any(group in groups for group in user.groups.values_list('name', flat=True))