from django import template
from accounts.models import CustomUser

register = template.Library()


@register.inclusion_tag('members/head_info.html')
def get_head_info():
    head_info = CustomUser.objects.filter(user_role='head').first()
    return {'head_info': head_info}


@register.inclusion_tag('members/current_info.html')
def get_current_info():
    current_info = CustomUser.objects.filter(status='current', student_level='Master')
    return {'current_info': current_info}


@register.inclusion_tag('members/current_phd_info.html')
def get_current_phd_info():
    current_info = CustomUser.objects.filter(status='current', student_level='PHD')
    return {'current_info': current_info}


@register.inclusion_tag('members/alumni_info.html')
def get_alumni_info():
    alumni_info = CustomUser.objects.filter(status='Alumni', student_level='Master')
    return {'alumni_info': alumni_info}


@register.inclusion_tag('members/alumni_phd_info.html')
def get_alumni_phd_info():
    alumni_info = CustomUser.objects.filter(status='Alumni', student_level='PHD')
    return {'alumni_info': alumni_info}
