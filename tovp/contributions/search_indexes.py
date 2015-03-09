from haystack import indexes

from ananta.search_indexes import ContentSearchIndexMixin
from contacts.search_indexes import PersonSearchIndexMixin

from .models import Pledge, Contribution


class PledgeIndex(ContentSearchIndexMixin, PersonSearchIndexMixin,
                  indexes.SearchIndex, indexes.Indexable):
    content_name = 'Pledge'
    text = indexes.CharField(document=True, use_template=True)
    amount = indexes.IntegerField(model_attr='amount')
    amount_paid = indexes.IntegerField(model_attr='amount_paid')
    currency = indexes.CharField(model_attr='currency', faceted=True)
    payments_start_date = indexes.DateTimeField(
        model_attr='payments_start_date')
    info = indexes.CharField(model_attr='info')
    interval = indexes.CharField(model_attr='get_interval_display',
                                 faceted=True)
    status = indexes.CharField(model_attr='get_status_display', faceted=True)

    # next_payment_date =

    def get_model(self):
        return Pledge


class ContributionIndex(ContentSearchIndexMixin, PersonSearchIndexMixin,
                        indexes.SearchIndex, indexes.Indexable):
    content_name = 'Contribution'
    text = indexes.CharField(document=True, use_template=True)
    amount = indexes.IntegerField(model_attr='amount')
    currency = indexes.CharField(model_attr='currency', faceted=True)
    payment_method = indexes.CharField(model_attr='get_payment_method_display',
                                       faceted=True)
    transaction_id = indexes.CharField(model_attr='transaction_id')
    bank = indexes.CharField(model_attr='bank', faceted=True)
    dated = indexes.DateTimeField()
    cleared_on = indexes.DateTimeField()
    status = indexes.CharField(model_attr='get_status_display', faceted=True)
    book_number = indexes.CharField(model_attr='book_number')
    slip_number = indexes.CharField(model_attr='slip_number')
    overwrite_name = indexes.CharField(model_attr='overwrite_name')
    overwrite_address = indexes.CharField(model_attr='overwrite_address')

    def get_model(self):
        return Contribution

    def prepare_dated(self, obj):
        if obj.dated:
            return obj.dated

    def prepare_cleared_on(self, obj):
        if obj.cleared_on:
            return obj.cleared_on