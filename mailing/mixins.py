from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        if not request.user.is_superuser and self.get_object().owner != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
