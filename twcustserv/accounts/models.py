import datetime

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.forms.models import model_to_dict

gender_choices = [('m', _('Male')),
                  ('f', _('Female'))]


class Account(models.Model):

    user = models.ForeignKey('auth.User', related_name='account_user', null=True)

    season = models.CharField(_('season'), max_length=32, default='INT',
                              editable=False)
    account = models.PositiveIntegerField(_('account'), editable=False,
                                          help_text=_('Set by Softix'))
    atype = models.PositiveSmallIntegerField(_('account type'), null=True, blank=True,
                                             help_text=_('Set by Softix'))

    area_code = models.CharField(_('area code'), max_length=32, blank=True)
    home_phone = models.CharField(_('home phone'), max_length=32)
    other_phone = models.CharField(_('other phone'), max_length=32, blank=True)

    name1 = models.CharField(_('first name'), max_length=32, blank=True)
    name2 = models.CharField(_('middle name'), max_length=32, blank=True)
    name3 = models.CharField(_('last name'), max_length=32)
    name4 = models.CharField(_('other name'), max_length=32, blank=True)
    name5 = models.CharField(_('other name'), max_length=32, blank=True)

    addr1 = models.CharField(_('address line 1'), max_length=34, blank=True)
    addr2 = models.CharField(_('address line 2'), max_length=34, blank=True)
    addr3 = models.CharField(_('address line 3'), max_length=34, blank=True)
    city = models.CharField(_('city'), max_length=30, blank=True)
    zip = models.CharField(_('zip/postal code'), max_length=16, blank=True)
    countrycode = models.CharField(_('country'), blank=True, max_length=250)
    apartment = models.CharField(_('apartment number'), max_length=16, blank=True)
    housenumber = models.CharField(_('house number'), max_length=16, blank=True)

    comment = models.CharField(_('comment'), max_length=255, blank=True)

    email_addr = models.EmailField(_('email address'))

    site_attrib = models.BooleanField(_('arbitrary boolean flag'
                                        ' - for internal usage'))
    do_not_mail = models.BooleanField(_('do not mail'))
    dead_account = models.BooleanField(_('dead account'))
    left_address = models.BooleanField(_('inaccurate address'))

    gender = models.CharField(_('gender'), max_length=1, blank=True, choices=gender_choices)
    member_dob = models.DateField(_('date of birth'), blank=True, null=True)
    member_since = models.DateField(_('member since'), blank=True, null=True,
                                    default=datetime.date.today, editable=False)

    primary_season = models.CharField(_('primary season'), max_length=32, blank=True)
    primary_an = models.PositiveIntegerField(_('primary account'), null=True, blank=True)

    class Meta:
        unique_together = ('season', 'account')
        verbose_name = _('account')
        verbose_name_plural = _('accounts')

    def __unicode__(self):
        return u' - '.join(unicode(p) for p in
                           [self.account, self.full_name, self.season] if p)

    @property
    def full_name(self):
        return u' '.join(n.strip() for n in
                         [self.name1, self.name2, self.name3,
                          self.name4, self.name5]
                         if n.strip())
