from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect

class OrganizerAndLoginRequiredMixin(AccessMixin):
    """ Verify that the user is authenticated and an organizer."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.is_agent:
            return redirect("leads:lead-list")
        return super().dispatch(request, *args, **kwargs)