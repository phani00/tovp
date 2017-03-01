from django.db import models
from django.utils.translation import ugettext_lazy as _
from reversion.views import RevisionMixin

from .utils import revision_set_comment


class RevisionCommentMixin(RevisionMixin):
    def form_valid(self, form):
        revision_set_comment(form)
        return super(RevisionCommentMixin, self).form_valid(form)

    class Meta:
        abstract = True


class SourceMixin(models.Model):
    SOURCE_CHOICES = (
        (u'ahmedabad-1', _('Ahmedabad 1')),
        (u'ahmedabad-2', _('Ahmedabad 2')),
        (u'tovp-f-mayapur', _('TOVP Fundraising Mayapur')),
        (u'tovp-exhibits', _('TOVP Exhibits')),
        (u'baroda', _('Baroda')),
        (u'bcs-vp-2015', _('BCS Vyasa Puja 2015')),
        (u'bhagavata-saptaha-2015', _('Bhagavata Saptaha 2015')),
        (u'bhakti-vriksa-kolkata-2016', _('Bhakti Vriksa Kolkata 2016')),
        (u'braj-mohan-mumbai', _('Braj Mohan (Mumbai)')),
        (u'delhi-vidyanagar-2015', _('Delhi Vidyanagar 2015')),
        (u'gkg-vp-2015', _('GKG Vyasa Puja 2015')),
        (u'gkg-vp-2016', _('GKG Vyasa Puja 2016')),
        (u'ils-2016', _('ILS 2016')),
        (u'iskcon-silicon-valley', _('ISKCON Silicon Valley (ISV)')),
        (u'j-w-marriot', _('J W Marriot')),
        (u'jps-office', _('JPS Office')),
        (u'jps-others', _('JPS Others')),
        (u'kolkata-nityananda-yatra-2017', _('Kolkata Nityananda Yatra 2017')),
        (u'kanjurmarg-mumbai-2015', _('Kanjurmarg Mumbai 2015')),
        (u'lm-reception', _('Life Membership Reception')),
        (u'mayapur-community', _('Mayapur Community')),
        (u'mso', _('MSO')),
        (u'mumbai-yatra-2016', _('Mumbai Yatra 2016')),
        (u'namahatta', _('JPS Namahatta')),
        (u'botswana-2016', _('Botswana 2016')),
        (u'south-afrika-2016', _('South Afrika 2016')),
        (u'neel-vasan-das', _('Neel Vasan Das')),
        (u'nigdi-2016.', _('Nigdi 2016.')),
        (u'nityananda', _('Nityananda Tour')),
        (u'nvs', _('Nava Yogendra Swami')),
        (u'other', _('Other')),
        (u'prabhupada-currency-inr', _('Prabhupada Currency INR')),
        (u'pune-group-mayapur-2015', _('Pune Group Mayapur 2015')),
        (u'pune-yatra-2016', _('Pune Yatra 2016')),
        (u'rns-kartik-yatra', _('RNS Kartik Yatra')),
        (u'rohini-narayani', _('Rohini (Sri Narayani Devi Dasi)')),
        (u'surat-1', _('Surat 1')),
        (u'surat-2', _('Surat 2')),
        (u'vallabha-vidyanagar', _('Vallabha Vidyanagar')),
        (u'vrindavan-booth', _('Vrindavan Booth 2015')),
        (u'vrindavan-booth-2016', _('Vrindavan Booth 2016')),
        (u'vvps-vp-2015', _('Vedavyasapriya Swami Vyasa Puja 2015')),
    )
    source = models.CharField("Source", max_length=30, default='',
                              choices=SOURCE_CHOICES, blank=True)

    class Meta:
        abstract = True


class NextPrevMixin(object):
    def next(self):
        obj = self.__class__.objects.filter(pk__gt=self.pk)[0:1]
        if len(obj):
            return obj[0]
        return ''

    def prev(self):
        obj = self.__class__.objects.filter(pk__lt=self.pk).order_by('-pk')[0:1]
        if len(obj):
            return obj[0]
        return ''
