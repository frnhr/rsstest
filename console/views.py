from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from extra_views.formsets import ModelFormSetView
from api.models import Feed
from .forms import FeedActivateForm


# noinspection PyUnresolvedReferences
class UserContextMixin(object):
    """ 
    Add request.user to template context. Because I don't like context processors. Not for CBV, anyways.
    """
    def get_context_data(self, **kwargs):
        context = super(UserContextMixin, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


# noinspection PyUnresolvedReferences
class LoginRequiredMixin(object):
    """
    Ensures that user must be authenticated in order to access view.
    """
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous():
            request.session['login_bold'] = True
            return redirect("home")
        else:
            return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class FrontpageView(TemplateView):
    template_name = 'console/frontpage.html'


class HomeView(UserContextMixin, TemplateView):
    template_name = 'console/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if self.request.session.get('login_bold', False):
            context['login_bold'] = True
            del self.request.session['login_bold']
        return context


class FeedsView(LoginRequiredMixin, ModelFormSetView):
    
    form_class = FeedActivateForm
    model = Feed
    template_name = 'console/feeds.html'
    extra = 1

    def get_success_url(self):
        url = super(FeedsView, self).get_success_url()
        self.request.session['feeds_saved_ok'] = True
        return url

    def get_context_data(self, **kwargs):
        context = super(FeedsView, self).get_context_data(**kwargs)
        if self.request.session.get('feeds_saved_ok', False):
            context['saved_ok'] = True
            del self.request.session['feeds_saved_ok']
        return context


class WordsView(LoginRequiredMixin, TemplateView):
    template_name = 'console/words.html'

    def get_context_data(self, **kwargs):
        context = super(WordsView, self).get_context_data(**kwargs)
        context['feeds'] = Feed.objects.all()
        return context
