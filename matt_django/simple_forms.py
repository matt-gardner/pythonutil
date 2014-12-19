from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django import forms

from collections import namedtuple

def add_url_to_data(data, varname, link):
    Url = namedtuple('Url', ['varname', 'link'])
    data['urls'].append(Url(varname, link))


def default_model_form(cls):
    class ModelForm(forms.ModelForm):
        class Meta:
            model = cls
    return ModelForm


@login_required
def simple_form(request, form_class, next_url, label, header, instance=None,
        initial={}, data=None):
    if request.POST:
        print request.POST
        if instance:
            form = form_class(request.POST, instance=instance)
        else:
            form = form_class(request.POST)
        try:
            form.save()
        except ValueError:
            print vars(form)
            print form.errors
            raise
        return HttpResponseRedirect(next_url)
    if data == None:
        data = base_data()
    data['form'] = form_class(instance=instance, initial=initial)
    data['submit_label'] = label
    data['header'] = header
    return render(request, 'add_form.html', data)


class DateTimeWidget(forms.DateTimeInput):
    def __init__(self, attrs=None):
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {'class': 'datetimepicker'}
        if 'format' not in self.attrs:
            self.attrs['format'] = '%m/%d/%Y %I:%M %p'

    def render(self, name, value, attrs=None):
        if value:
            value = value.strftime(self.attrs['format'])
        return super(forms.DateTimeInput, self).render(name, value, attrs)

DATE_TIME_FORMATS = ['%m/%d/%Y %I:%M %p']


# vim: et sw=4 sts=4
