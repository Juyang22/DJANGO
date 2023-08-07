from django import template

register = template.Library()

# sub 함수 위에 @register.filter() 적용하면 템플릿에서 해당 함수를 필터로 사용
@register.filter()
def sub(value, arg):
    """
    value - arg
    """
    return value - arg