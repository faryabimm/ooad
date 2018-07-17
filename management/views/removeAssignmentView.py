import json

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import get_template
from django.views import View

from management.mixins import ManagerRequiredMixin
from management.models.assignment import AssignmentCatalog
from management.models.jobs import EmployeeCatalog


class RemoveAssignmentView(ManagerRequiredMixin, View):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template = get_template('management/removeAssignment.html')

    def post(self, request):
        json_data = json.loads(request.body)
        evaluatee_username = json_data['evaluatee_username']
        evaluator_username = json_data['evaluator_username']
        AssignmentCatalog.get_instance().remove_assignment(evaluatee_username, evaluator_username)
        return redirect('/management/assignEvaluatorToEmployee/')