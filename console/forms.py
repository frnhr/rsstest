from django import forms
from api.models import Feed


class FeedActivateForm(forms.ModelForm):
    delete = forms.BooleanField(required=False, initial=False)


    def __init__(self, *args, **kwargs):
        super(FeedActivateForm, self).__init__(*args, **kwargs)
        if self.instance.id:
            self.fields['url'].widget.attrs['readonly'] = True
        else:
            del self.fields['delete']

    def clean_url(self):
        """
        Prevent changing URL
        """
        if self.instance.id:
            self.cleaned_data['url'] = self.instance.url
        return self.cleaned_data['url']

    def save(self, commit=True):
        if commit:
            delete_data = self.cleaned_data.get('delete', None)
            if delete_data and self.instance.id:
                self.Meta.model.objects.filter(id=self.instance.id).delete()
                return
        super(FeedActivateForm, self).save(commit)

    class Meta:
        model = Feed
        fields = ('url', 'is_active', )
        #fields = ('is_active', )


