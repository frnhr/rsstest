from django.shortcuts import render
from django.views.generic.base import TemplateView

# noinspection PyUnresolvedReferences
class UserContextMixin(object):
    """ 
    Add request.user to template context. Because I don't like context processors. Not for CBV, anyways.
    """
    def get_context_data(self, **kwargs):
        context = super(UserContextMixin, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class HomeView(UserContextMixin, TemplateView):
    template_name = 'console/home.html'


class FeedsView(UserContextMixin, TemplateView):
    template_name = 'console/feeds.html'

