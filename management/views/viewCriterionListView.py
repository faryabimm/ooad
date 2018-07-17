from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View

from auth.mixins import LoginRequiredMixin
from management.mixins import ManagerRequiredMixin
from management.models.criterion import CriterionCatalog


class ViewCriterionListView(ManagerRequiredMixin, View):
    def get(self, request):
        criterion_names = CriterionCatalog.get_instance().get_names()
        t = get_template('management/viewCriteriaList.html')
        html = t.render({'criterion_names': criterion_names}, request)
        return HttpResponse(html)