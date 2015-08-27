from mezzanine import template
from mezzanine.utils.sites import current_site_id

from my_cms.models import Employee, WorkOrder

register = template.Library()


@register.as_tag
def get_sitewide_content():
    """
    Adds the `SitewideContent` to the context
    """
    args = {}
    #args['contact']= Contact.objects.get_or_create(site_id=current_site_id())[0]
    #args['works'] = Work.objects.all()
    employees = Employee.objects.all()

    #args['worksimages'] = WorkImage.objects.all()
    args['employees'] = employees
    
    #employees2 = Employee.objects.prefetch_related('workorder')
    
    #works = employee.WorkOrder_set.all()
    args['work_orders'] = WorkOrder.objects.all().order_by('-time_date')
    #args['emp'] = employees2
    return args
  
