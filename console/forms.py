from django import forms
from api.models import Feed


class FeedActivateForm(forms.ModelForm):
    delete = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        """
        Make URL a readonly field for saved instances (this is cosmetics only!)
        Show delete checkbox only for saved instances.
        """
        super(FeedActivateForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            del self.fields['url']
        else:
            del self.fields['delete']
            self.fields['url'].widget.attrs['class'] = self.fields['url'].widget.attrs.get('class', '') + " form-control"  

    def clean_url(self):
        """
        Prevent changing URL, in case someone fiddles with Firebug. 
        """
        if self.instance.id:
            self.cleaned_data['url'] = self.instance.url
        return self.cleaned_data['url']

    def save(self, commit=True):
        """
        Deletes instance if "delete" checkbox was marked.
        """
        if commit:
            delete_data = self.cleaned_data.get('delete', None)
            if delete_data and self.instance.id:
                self.Meta.model.objects.filter(id=self.instance.id).delete()
                return
        super(FeedActivateForm, self).save(commit)

    class Meta:
        model = Feed
        fields = ('url', 'is_active', )


