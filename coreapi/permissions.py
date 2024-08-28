from rest_framework.permissions import BasePermission
class IsTutor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.type == 'Tutor')

class IsLearner(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.type == 'Learner')    