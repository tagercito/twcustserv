import datetime
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Transaction(models.Model):
    date = models.DateField(blank=True)

    fmj_date = models.CharField(_('master journal date'), max_length=6)
    tnum = models.CharField(_('transaction number'), max_length=16)

    title1 = models.CharField(_('title line 1'), max_length=64, blank=True)
    title2 = models.CharField(_('title line 2'), max_length=64, blank=True)
    title3 = models.CharField(_('title line 3'), max_length=64, blank=True)
    title4 = models.CharField(_('title line 4'), max_length=64, blank=True)
    title5 = models.CharField(_('title line 5'), max_length=64, blank=True)
    title6 = models.CharField(_('title line 6'), max_length=64, blank=True)

    scomment = models.CharField(_('seat comment'), max_length=64, blank=True)
    stitle = models.CharField(_('seat title'), max_length=64, blank=True)

    where = models.SmallIntegerField(_('performance location title line number'), blank=True, null=True)
    who = models.SmallIntegerField(_('performer title line number'), blank=True, null=True)
    when = models.SmallIntegerField(_('performance date title line number'), blank=True, null=True)

    location = models.CharField(_('section-specific location'), max_length=64)
    usher1 = models.CharField(_('section usher 1'), max_length=64)
    usher2 = models.CharField(_('section usher 2'), max_length=64)

    account = models.ForeignKey('accounts.Account', blank=True, null=True)

    purchase = models.ForeignKey('purchase.Purchase')


    class Meta:
        verbose_name = _('transaction')
        verbose_name_plural = _('transactions')
        unique_together = (('fmj_date', 'tnum',),)

    def __unicode__(self):
        return u' - '.join([self.fmj_date, str(self.tnum)])


class Ticket(models.Model):
    transaction = models.ForeignKey(Transaction,
                                    verbose_name=_('transaction'),
                                    related_name='tickets')

    paxnum = models.PositiveIntegerField(_('paxnum'), editable=False,
                                         help_text=_('Set by Softix'))
    secname = models.CharField(_('section name'), max_length=64)
    rowname = models.CharField(_('row name'), max_length=64)
    seatname = models.CharField(_('seat name'), max_length=64)
    ptcode = models.CharField(_('price type code'), max_length=8)
    ptname = models.CharField(_('price type name'), max_length=64)
    price = models.CharField(_('price'), max_length=64)
    bfee = models.CharField(_('booking fee'), max_length=64)
    concession = models.PositiveIntegerField(_('concession'))
    tix_price_suppressed = models.BooleanField(_('price is overridden'))
    barcode = models.CharField(_('barcode'), max_length=16, editable=False)
    door = models.CharField(_('door name'), max_length=64)
    aisle = models.CharField(_('aisle name'), max_length=64)
    owner = models.CharField(_('owner'), max_length=255)

    class Meta:
        ordering = ['barcode',]
        verbose_name = _('ticket')
        verbose_name_plural = _('tickets')
