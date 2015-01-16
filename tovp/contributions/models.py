from django.db import models
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _
from django.core import exceptions

from model_utils.fields import MonitorField
from model_utils.models import TimeStampedModel
# from dateutil import relativedelta

from contacts.models import Person


class Pledge(TimeStampedModel):
    person = models.ForeignKey(Person, verbose_name="Person", blank=True,
                               related_name='pledges')
    amount = models.DecimalField(_('Amount'), max_digits=20, decimal_places=2)
    amount_paid = models.DecimalField(_('Amount Paid'), max_digits=20,
                                      default=0, decimal_places=2,
                                      null=True, blank=True)
    CURRENCY_CHOICES = (
        ('INR', _('₹')),
        ('USD', _('$')),
        ('EUR', _('€')),
    )
    currency = models.CharField(
        "Currency", max_length=6, choices=CURRENCY_CHOICES, default="INR")
    payments_start_date = models.DateField(
        _("Payments Start"), null=True, blank=True,
        help_text=_('Date of first expected payment for this pledge.'),
    )
    INTERVAL_CHOICES = (
        (u'1', _('1 month')),
        (u'2', _('2 months')),
        (u'3', _('3 months')),
        (u'4', _('4 months')),
        (u'6', _('6 months')),
    )
    interval = models.CharField(
        _("Payments Interval"), max_length=30, choices=INTERVAL_CHOICES,
        help_text=_("Enter planned interval of payments (e.g. 1 month)"),
    )
    STATUS_CHOICES = (
        (u'pending', _('Pending')),
        (u'partial', _('Partially Paid')),
        (u'completed', _('Completed')),
        (u'failed', _('Shadow')),
    )
    status = models.CharField("Status", max_length=30, default='pending',
                              choices=STATUS_CHOICES, blank=True)

    status_changed = MonitorField(monitor='status')

    next_payment_date = models.DateField(
        _("Next Payment Date"), null=True, blank=True,
        help_text=_('Date of next expected payment.'),
    )

    @property
    def progress(self):
        if self.amount_paid and self.amount:
            return self.amount_paid / self.amount * 100
        return 0

    @permalink
    def get_absolute_url(self):
        return ('contributions:pledge:detail', None, {
            'person_id': self.person.pk,
            'pk': self.pk})

    def info(self):
        return 'Pledged {amount}{currency} - {progress}% completed'. \
            format(amount=self.amount, currency=self.get_currency_display(),
                   progress=self.progress, status=self.get_status_display())

    # def update_next_payment_due(self):
    #     self.next_payment_date = last_contribution_date + \
    #                              relativedelta(months = self.interval)

    def __str__(self):
        field_values = (
            self.person.full_name,
            self.amount,
        )
        return ' - '.join(filter(bool, field_values))


class Contribution(TimeStampedModel):
    person = models.ForeignKey(Person, verbose_name="Person", blank=True,
                               related_name='contributions')
    amount = models.DecimalField(_('Amount'), max_digits=20, decimal_places=2)
    CURRENCY_CHOICES = (
        (u'INR', _('₹')),
        (u'USD', _('$')),
        (u'EUR', _('€')),
    )
    currency = models.CharField(
        "Currency", max_length=6, choices=CURRENCY_CHOICES)
    PAYMENT_METHOD_CHOICES = (
        (u'cash', _('Cash')),
        (u'ccdc', _('Credit/Debit Card')),
        (u'neft', _('NEFT')),
        (u'cheque', _('Cheque')),
    )
    payment_method = models.CharField(
        "Payment Method", max_length=6, choices=PAYMENT_METHOD_CHOICES)

    transaction_id = models.CharField(
        _('Transaction ID or Cheque No'), max_length=100, blank=True,
        help_text=_('Transaction ID of this contribution or cheque number.'))

    dated = models.DateField(
        _("Dated"), null=True, blank=True,
        help_text=_('Enter date of the transaction (e.g. date on the cheque, '
                    'date when credit card was charged)')
    )
    STATUS_CHOICES = (
        (u'pending', _('Pending')),
        (u'completed', _('Completed')),
        (u'failed', _('Failed')),
    )
    status = models.CharField("Status", max_length=30, choices=STATUS_CHOICES)

    status_changed = MonitorField(monitor='status')

    def clean(self):
        errors = {}

        # Strip all whitespace
        for field in ['transaction_id']:
            if self.__dict__[field]:
                self.__dict__[field] = self.__dict__[field].strip()

        if self.status == 'completed' and not self.dated:
            msg = _("There must be date for completed transaction")
            errors['dated'] = [msg]

        # transaction id is required for cheque or credit/debit cards payments
        if not self.transaction_id:
            if self.payment_method in ['cheque', 'ccdc']:
                if self.payment_method == 'ccdc':
                    msg = _("You have to fill Transaction ID for Credit/Debit "
                            "card payment.")
                    errors['transaction_id'] = [msg]
                if self.payment_method == 'cheque':
                    msg = _("You have to fill Cheque Number")
                    errors['transaction_id'] = [msg]
        if errors:
            raise exceptions.ValidationError(errors)

    @property
    def currency_words(self):
        CURRENCY_CHOICES = {
            'INR': 'rupees',
            'USD': 'american dollars',
            'EUR': 'euro',
        }
        return CURRENCY_CHOICES[self.currency]

    @permalink
    def get_absolute_url(self):
        return ('contributions:contribution:detail', None, {
            'person_id': self.person.pk,
            'pk': self.pk})

    def info(self, show_name=None):
        field_values = [
            '#' + str(self.pk),
        ]
        if show_name:
            field_values.append(self.person.full_name)
        field_values.append(str(self.dated))
        field_values.append(str(self.amount))
        field_values.append(self.currency)
        field_values.append('(%s)' % self.get_payment_method_display())
        field_values.append(self.get_status_display())
        return ' - '.join(filter(bool, field_values))

    def __str__(self):
        field_values = (
            self.person.full_name,
            self.amount,
            '(%s)' % self.get_payment_method_display()
        )
        return ' - '.join(filter(bool, field_values))
