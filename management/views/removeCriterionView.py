from django.shortcuts import redirect
from django.views import View

from management.mixins import ManagerRequiredMixin
from management.models.criterion import CriterionCatalog


class RemoveCriterionView(ManagerRequiredMixin, View):
    def get(self, request, criterion_name):
        CriterionCatalog.get_instance().delete_if_exists(criterion_name)
        return redirect('/management/viewCriterion/')
