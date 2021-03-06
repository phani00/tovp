from django import forms
from django.utils.safestring import mark_safe
from django.forms import TextInput

from datetimewidget.widgets import DateWidget

from .models import Pledge, FollowUp, Contribution, BulkPayment

from contacts.models import Person


class PledgeForm(forms.ModelForm):
    person = forms.ModelChoiceField(queryset=Person.objects.all(),
                                    widget=forms.HiddenInput())

    class Meta:
        model = Pledge
        exclude = ('status_changed',)
        widgets = {
            'amount': TextInput(attrs={'type': 'text'}),
            'payments_start_date': DateWidget(
                attrs={},
                options={'startView': 2, 'format': 'yyyy-mm-dd'},
                bootstrap_version=3
            ),
        }


class FollowUpForm(forms.ModelForm):
    pledge = forms.ModelChoiceField(queryset=Pledge.objects.all(),
                                    widget=forms.HiddenInput())

    next_payment_date = forms.DateField(
        required=False,
        widget=DateWidget(
            attrs={},
            options={'startView': 2, 'format': 'yyyy-mm-dd'},
            bootstrap_version=3
        ),
        label='Next expected payment date',
    )

    def save(self, commit=True):
        instance = super(FollowUpForm, self).save()

        # if we defined new date of next payment we will save it to the pledge
        if self.cleaned_data['next_payment_date']:
            instance.pledge.payments_start_date = self.cleaned_data['next_payment_date']
            instance.pledge.save()
        return instance

    def __init__(self, next_payment_date, *args, **kwargs):
        super(FollowUpForm, self).__init__(*args, **kwargs)
        self.fields['next_payment_date'].initial = next_payment_date

    class Meta:
        model = FollowUp
        exclude = []


class NoInput(forms.Widget):
    def render(self, name, value, attrs=None):
        return mark_safe(value)


class StaticField(forms.Field):
    widget = NoInput

    def clean(self, value):
        return


class ContributionForm(forms.ModelForm):
    def __init__(self, person, request=None, user=None, *args, **kwargs):
        super(ContributionForm, self).__init__(*args, **kwargs)

        if request and request.user.default_usa_receipt:
            self.fields['receipt_type'].initial = 'usa-receipt'

        self.fields['pledge'].queryset = Pledge.objects.filter(
            person=person)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk and instance.serial_number \
                and instance.payment_method in ['cashl', 'cashf'] \
                and not user.has_perm('contributions.can_edit_completed'):
            self.fields['amount'] = StaticField()
            self.fields['currency'] = StaticField()
            self.fields['receipt_date'] = StaticField()
            self.fields['is_external'] = StaticField()
            if instance.status == 'completed':
                self.fields['status'] = StaticField()
                self.fields['cleared_on'] = StaticField()
                self.fields['payment_method'] = StaticField()

        if not self.is_bound:
            if None not in (self.instance, self.instance.bulk_payment):
                self.fields['bulk_payment'].queryset = BulkPayment.objects. \
                    filter(pk=self.instance.bulk_payment.pk)
            else:
                self.fields['bulk_payment'].queryset = BulkPayment.objects. \
                    none()

            if None not in (self.instance, self.instance.collector):
                self.fields['collector'].queryset = Person.objects.filter(
                    pk=self.instance.collector.pk)
                print(self.fields['collector'].queryset)

            else:
                self.fields['collector'].queryset = Person.objects.none()

    def clean(self):
        for name, field in self.fields.items():
            if isinstance(field, StaticField):
                self.cleaned_data.update({name: self.initial[name]})

        return self.cleaned_data

    class Meta:
        model = Contribution
        exclude = ('status_changed', 'deposited_status',
                   'deposited_status_changed')
        widgets = {
            'collector': forms.Select(attrs={'class': 'autocomplete'}),
            'amount': TextInput(attrs={'type': 'text'}),
            'foreign_amount': TextInput(attrs={'type': 'text'}),
            'dated': DateWidget(
                attrs={},
                options={
                    'startView': 2,
                    'format': 'yyyy-mm-dd',
                },
                bootstrap_version=3
            ),
            'receipt_date': DateWidget(
                attrs={},
                options={
                    'startView': 2,
                    'format': 'yyyy-mm-dd',
                },
                bootstrap_version=3
            ),
            'cleared_on': DateWidget(
                attrs={},
                options={
                    'startView': 2,
                    'format': 'yyyy-mm-dd',
                },
                bootstrap_version=3
            ),
        }


class BulkPaymentForm(forms.ModelForm):
    person = forms.ModelChoiceField(queryset=Person.objects.all(),
                                    widget=forms.HiddenInput())

    def __init__(self, person, *args, **kwargs):
        super(BulkPaymentForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk and instance.serial_number:
            self.fields['amount'] = StaticField()
            self.fields['currency'] = StaticField()
            self.fields['receipt_date'] = StaticField()
            if instance.status == 'completed':
                self.fields['status'] = StaticField()
                self.fields['cleared_on'] = StaticField()
                self.fields['payment_method'] = StaticField()

    def clean(self):
        for name, field in self.fields.items():
            if isinstance(field, StaticField):
                self.cleaned_data.update({name: self.initial[name]})

        return self.cleaned_data

    class Meta:
        model = BulkPayment
        exclude = ('status_changed',)
        widgets = {
            'amount': TextInput(attrs={'type': 'text'}),
            'dated': DateWidget(
                attrs={},
                options={
                    'startView': 2,
                    'format': 'yyyy-mm-dd',
                },
                bootstrap_version=3
            ),
            'receipt_date': DateWidget(
                attrs={},
                options={
                    'startView': 2,
                    'format': 'yyyy-mm-dd',
                },
                bootstrap_version=3
            ),
            'cleared_on': DateWidget(
                attrs={},
                options={
                    'startView': 2,
                    'format': 'yyyy-mm-dd',
                },
                bootstrap_version=3
            ),
        }
