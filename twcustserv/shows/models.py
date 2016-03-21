from datetime import datetime
from decimal import Decimal
import json
from collections import OrderedDict

from django.conf import settings
from django.core import management
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.db.models.signals import pre_save
from django.utils.translation import ugettext_lazy as _

import requests
import datetime

##from insurance.models import Insurance
from operator import itemgetter
AVAILABILITY_CHOICES = (
    ('SOLDOUT'  , 'SOLDOUT'),
    ('LIMITED'  , 'LIMITED'),
    ('AVAILABLE', 'AVAILABLE'),
    ('SOONTOSOLDOUT', 'SOONTOSOLDOUT'),
    ('CUPO'     , 'CUPO'),
    ('VP'       , 'VP'),
    ('SINGLE'   , 'SINGLE'),
)

EXCLUDE = ['updated_at', 'created_at', 'api_performance']

class AuditedModel(models.Model):

    # Audit
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    display_text = models.CharField(_('display text'), max_length=254, blank=True)
    admin_name = models.CharField(_('Admin unicode'), max_length=254, blank=True, null=True)

    class Meta:
        abstract = True

    def has_changed(self):
        for field in self._meta.fields:
            if field.name not in EXCLUDE:
                if self.field_has_changed(field):
                    return True
        return False

    def field_has_changed(self, field):
        old_value = getattr(self.__class__._default_manager.get(pk=self.pk), field.name)
        try:
            #Intento Castear el nuevo valor al tipo de campo para poder comparar bien
            new = field.get_db_prep_value(getattr(self, field.name), connection=None)
        except:
            new = getattr(self, field.name)
        return not new == old_value



class Show(AuditedModel):

   # content = models.ForeignKey(Content, null=True)
   # mail_content = models.ForeignKey(Content, null=True, blank=True, related_name='mail_show')

    # Basic
    name = models.CharField(_('Name'), max_length=32, unique=True)
    description = models.TextField(_('Description'), null=True, blank=True)
    is_hotshow = models.BooleanField(default=False)
    cms_url = models.CharField('URL redirect CMS', max_length=255, null=True, blank=True)

   # insurance = models.ForeignKey('insurance.Insurance', null=True, related_name = 'insurance')
    is_active = models.BooleanField(_('Is Active?'), default=True)
    is_public = models.BooleanField(_('Is Public?'), default=True)
    in_cms = models.BooleanField(_('Url is redirected?'), default=False)
    is_big = models.BooleanField(_('Is Big?'), default=False)
    #objects = ShowManager()
    extra_tickets = models.BooleanField(_('Seleccionar mas entradas'), default=False)


class Performance(AuditedModel):

    # Relations
    show = models.ForeignKey('Show', related_name='performances')
    venue = models.ForeignKey('Venue', related_name='venues', null=True, blank=True)
    venue_profile = models.ForeignKey('VenueProfile', null=True, blank=True, on_delete=models.SET_NULL)

    shipping_points = models.ManyToManyField('ShippingPoint', related_name='performances', through='shows.ShippingPointDetails')

    is_series = models.BooleanField(_('is this performance a series?'), default=False)
    seat_selection_disabled = models.BooleanField(_('seat selection disabled'), default=False)

    # Basic
    perf_code = models.CharField(_('Code'), max_length=32)
    event_name = models.CharField(_('Event Name'), max_length=32, null=True, blank=True)
    region = models.CharField(_('Region'), max_length=8)
    who = models.CharField(_('Who'), max_length=100, blank=True)
    when = models.CharField(_('When'), max_length=100, blank=True,
                            help_text=_('The content of this field will be'
                                        ' shown as the perf\'s name in the buy box.'))
    date = models.DateTimeField(_('Date'), null=True, blank=True)
    where = models.CharField(_('Where'), max_length=100, blank=True)
    hidden = models.BooleanField(default=False)
    is_active = models.BooleanField(_('Is Active?'), default=True)
    #credit_cards = models.ManyToManyField('purchase.Card', related_name='performances')
    can_print_at_home = models.BooleanField(_('Can print at home?'), default=False)
  #  insurance = models.ForeignKey('insurance.Insurance', null=True, blank=True, related_name = 'perf_insurance')
    use_local_seatmap = models.BooleanField(default=False, help_text='Poner en True para no pedir a softix el seatmap en cada proceso de compra')
    order = models.PositiveIntegerField(_('Orden Para Mostrar'), default=0)
    sales_start = models.DateTimeField(_('Start date of sales'), null=True, blank=True)
    sales_end = models.DateTimeField(_('End date of sales'), null=True, blank=True)
    #Specific
    max_qty = models.IntegerField(default=6)
    la_nacion_quota = models.PositiveIntegerField(_('Cupo para La Nacion'), default=0)
    extra_tickets = models.BooleanField(_('Seleccionar mas entradas'), default=False)
    social_share = models.BooleanField(_('Habilitar la compra social?'), default=False)

    class Meta:
        verbose_name = _('performance')
        verbose_name_plural = _('performances')
        unique_together = (('show', 'perf_code','event_name'),)

    def __unicode__(self):
        try:
            return u'%s/%s' % (self.show, self.perf_code)
        except:
            return u''

class Series(AuditedModel):

    performance = models.ForeignKey('Performance', related_name='related_series')
    choices = models.ManyToManyField('Performance', related_name='series',
                                     limit_choices_to={'is_series': False})

    is_fixed = models.BooleanField(default=False)

    desc = models.TextField(_('description'))
    onsale = models.DateTimeField(_('starts on'))
    offsale = models.DateTimeField(_('ends on'))
    ticket_limit = models.PositiveIntegerField(_('ticket limit'))

    availability = models.CharField(_('Availability'), max_length=16,
                                    choices= AVAILABILITY_CHOICES,
                                    default = 'AVAILABLE')
    is_active = models.BooleanField(_('Is Active?'), default=True)


    class Meta:
        verbose_name = _('series')
        verbose_name_plural = _('series')


    def __unicode__(self):
        try:
            return u'%s/%s' % (self.desc, self.performance)
        except:
            return u''


class PriceType(AuditedModel):

    # Relations
    performance = models.ForeignKey('Performance', related_name='price_types')
   # content = models.ForeignKey(Content, null=True, blank = True)
   # mail_content = models.ForeignKey(Content, null=True, blank=True, related_name='mail_price_type')
  #  benefit = models.ForeignKey('benefits.Benefit', null=True, blank = True)

    # Basic
    name = models.CharField(_('Name'), max_length=32)
    code = models.CharField(_('Code'), max_length=1)
    dayos_code = models.CharField(_('Dayos Code'), max_length=1, null=True, blank = True)
    has_dayos = models.BooleanField(default=False)
    description = models.CharField(_('Description'), max_length=100)
    admit_cnt = models.IntegerField(_('Admit Cnt'))
    max_qty = models.IntegerField(_('max qty'), default=0)
    generic_type = models.CharField(_('Generic Type'), max_length=1)
    price_plan = models.CharField(_('Price Plan'), max_length=32)
    use_quals = models.IntegerField(_('Use Quals'))
    hidden = models.BooleanField(default=False)
    is_active = models.BooleanField(_('Is Active?'), default=True)

    exclusive = models.BooleanField(_('Is Exclusive?'), default=False)
    #discount = models.BooleanField(_('Has Discount?'), default=False)

    class Meta:
        # Ptypes must be unique on each perf
        unique_together = ('code', 'performance')
        verbose_name = _('price type')
        verbose_name_plural = _('price types')

    def __unicode__(self):
        try:
            return u'%s/%s' % (self.performance, self.code)
        except:
            return u''



class PriceCategory(AuditedModel):

    # Relations
    price_type = models.ForeignKey('PriceType', related_name='price_categories')
    section = models.ForeignKey('Section', related_name='price_categories')

    price = models.DecimalField(_('Price'), max_digits=8, decimal_places=2)
    bfee = models.DecimalField(_('Booking Fee'), null=True, blank=True,
                                max_digits=8, decimal_places=2, default=0)
    full_price = models.DecimalField(_('Full Price'), max_digits=8, decimal_places=2, default=-1,
                             help_text=_('The price plus the discount. -1 If no discount'))
    max_qty = models.IntegerField(_('max qty'),  null=True, blank=True, default=0)
    hidden = models.BooleanField(default=False)
    is_active = models.BooleanField(_('Is Active?'), default=True)

    class Meta:
        verbose_name = _('price category')
        verbose_name_plural = _('price categories')

    def __unicode__(self):
        try:
            return u'%s/%s' % (self.price_type.__unicode__(), self.section.section)
        except:
            return u''

class SeriesPriceCategory(AuditedModel):
    serie = models.ForeignKey(Series, related_name='serie')
    pcat = models.ForeignKey(PriceCategory, blank=True, null=True)

    class Meta:
        verbose_name = _('Series price category')
        verbose_name_plural = _('Series price categories')

class Section(AuditedModel):

    performance = models.ForeignKey('Performance', related_name='sections')

    section = models.CharField(_('Section'), max_length=16)
    desc = models.CharField(_('Description'), max_length=100)
    pcat = models.IntegerField(_('Price Category Id'))
    is_ga = models.BooleanField(_('General Access'), default=False)
    _seatmap = models.TextField(db_column='seatmap', default='[]')
    corridor_map = models.TextField(default='[]')
    seat_selection_disabled = models.BooleanField(_('seat selection disabled'), default=False)
    availability = models.CharField(_('Availability'), max_length=16,
                                    choices= AVAILABILITY_CHOICES,
                                    default = 'AVAILABLE')
    limited_vision = models.BooleanField(default=False)
    restricted_vision = models.BooleanField(default=False)
    hidden = models.BooleanField(default=False)
    is_active = models.BooleanField(_('Is Active?'), default=True)
    small_section = models.BooleanField(_('Is small Section?'), default=False)
    soon_to_soldout = models.BooleanField(_('Soon to sold out?'), default=False)
    show_seat_description = models.BooleanField(_('Mostrar Fila/Asiento en resumen de'), default=True)

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')

    def __unicode__(self):
        try:
            return u'%s/%s' % (self.performance, self.section)
        except:
            return u''
class DeliveryType(AuditedModel):

  #  content = models.ForeignKey(Content, null=True, blank=True)
    name = models.CharField(_('Name'), max_length=16)

    class Meta:
        verbose_name = _('DeliveryType')
        verbose_name_plural = _('DeliveryTypes')

    def __unicode__(self):
        try:
            return u'%s' % (self.name)
        except:
            pass
class DeliveryTypeMapping(AuditedModel):

    delivery = models.CharField(_('Delivery'), max_length=5)
    type = models.ForeignKey(DeliveryType)

    class Meta:
        verbose_name = _('delivery mapping')
        verbose_name_plural = _('delivery mappings')

    def __unicode__(self):
        try:
            return u'%s' % self.delivery
        except:
            return u''
class ShippingPoint(AuditedModel):
    name = models.CharField(_('Name'), max_length=30)
    address = models.CharField(_('Address'), max_length=100)
    businessTime = models.TextField(_('BussinessTime'), max_length=100)
    type = models.ForeignKey(DeliveryType)
  #  content = models.ForeignKey(Content, null=True)
    default = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('shipping point')
        verbose_name_plural = _('shipping points')

    def __unicode__(self):
        try:
            return u'%s' % self.name
        except:
            return u''
class ShippingPointDetails(AuditedModel):
    performance     = models.ForeignKey('Performance', related_name ='shipping_point_detail')
    shipping_point  = models.ForeignKey('ShippingPoint', related_name ='shipping_point_detail')
 #   content         = models.ForeignKey(Content, null=True, blank = True)

    class Meta:
        verbose_name = _('shipping point details')
        verbose_name_plural = _('shipping points details')
        unique_together = ('performance','shipping_point')

    def __unicode__(self):
        try:
            return u'%s/%s' % (self.performance, self.shipping_point)
        except:
            return u''

class VenueShippingPointDetails(AuditedModel):
    venue     = models.ForeignKey('Venue', related_name ='venue_shipping_point_detail')
    shipping_point  = models.ForeignKey('ShippingPoint', related_name ='venue_shipping_point_detail')
  #  content         = models.ForeignKey(Content, null=True, blank = True)

    class Meta:
        verbose_name = _('venue shipping point details')
        verbose_name_plural = _('venue shipping points details')
        unique_together = ('venue','shipping_point')

    def __unicode__(self):
        try:
            return u'%s/%s' % (self.venue, self.shipping_point)
        except:
            return u''

class Delivery(AuditedModel):

    # Relations
    performance = models.ForeignKey('Performance', related_name='deliveries')
 #   content = models.ForeignKey(Content, null=True, blank=True)
 #   mail_content = models.ForeignKey(Content, null=True, blank=True, related_name='mail_delivery')
    type = models.ForeignKey(DeliveryType)

    # Basic
    code = models.CharField(_('Code'), max_length=1)
    name = models.CharField(_('Name'), max_length=16)
    description = models.CharField(_('Description'), max_length=100)
    ship = models.BooleanField(_('Ship'))
    fee = models.DecimalField(_('Fee'), max_digits=8, decimal_places=2)
    is_active = models.BooleanField(_('Is Active?'), default=True)

    class Meta:
        verbose_name = _('delivery')
        verbose_name_plural = _('deliveries')

    def __unicode__(self):
        try:
            return u'%s/%s' % (self.performance, self.code)
        except:
            return u''
    def set_admin_name(self):
        admin_name = '/'.join([self.performance.admin_name, self.code])
        self.admin_name = admin_name

class Location(AuditedModel):
    desc = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
  #  address = map_fields.AddressField(max_length=255, null=True, blank=True)
   # geolocation = map_fields.GeoLocationField(max_length=255, null=True, blank=True)

class Venue(Location):
    zoom = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    title = models.CharField(max_length=255, null=True, blank=True)
    web = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    thumb = models.CharField(max_length=255, null=True, blank=True)
    header = models.CharField(max_length=255, null=True, blank=True)
    shipping_points = models.ManyToManyField('ShippingPoint', related_name='venue_shipping_points', through='shows.VenueShippingPointDetails')

    def get_venue_info(self):
        return dict(title=self.display_text or self.title,
                    address = self.address,
                    city = self.city,
                    state = self.state)


    def __unicode__(self):
        try:
            return u'%s - %s' % (self.code, self.display_text)
        except:
            return u''
class VenueProfile(AuditedModel):
    venue = models.ForeignKey('Venue')
    html_map = models.TextField(null=True, blank=True)
  #  background = models.ImageField(upload_to='venueprofile', null=True, blank=True)
    default = models.BooleanField(default=False)
    small_section = models.BooleanField(default=False)
    show_seat_description = models.BooleanField(_('Mostrar Fila/Asiento en resumen de'), default=True)

    class Meta:
        ordering = ['venue__code']

    def load_html_map(self):
        #Cambio background no requerido
        if self.html_map and self.background:
            html = self.html_map
            html = html.replace('{{ MAP_IMAGE }}', self.background.url)
            return html

    def get_section_group_name(self, color):
        try:
            vp_colorgroup = VenueProfileColorGroup.objects.get(venue_profile=self, color=color)
            return vp_colorgroup.name
        except VenueProfileColorGroup.DoesNotExist:
            return 'SECTORES'

    def __unicode__(self):
        try:
            return u'%s-%s profile' % (self.venue, self.display_text)
        except:
            return u''
def update_default(sender, instance, created, **kwargs):
    if instance.default:
        q = VenueProfile.objects.filter(default=True, venue=instance.venue).exclude(id=instance.id)
        q.update(default=False)

post_save.connect(update_default, sender = VenueProfile)

class Area(models.Model):
    venue_profile_section = models.ForeignKey('VenueProfileSection', related_name='areas')
    code = models.CharField(max_length=255)

class VenueProfileSection(AuditedModel):
    venue_profile = models.ForeignKey('VenueProfile')
    section = models.CharField(max_length=255)
 #   color = RGBColorField()
   # thumbnail_image = models.ImageField(upload_to='venueprofile', null=True, blank=True)
    thumbnail = models.URLField()
    #ticket_info_image = models.ImageField(upload_to='venue_ticketinfo', null=True, blank=True)
    ticket_info_description = models.TextField()

    def __unicode__(self):
        try:
            return u'%s : %s' % (self.venue_profile, self.section)
        except:
            return u''


class VenueProfileSectionInfo(AuditedModel):
    section = models.ForeignKey(VenueProfileSection, related_name="venue_profile_section_info")
    icon = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __unicode__(self):
        return u'%s-%s' % (self.title, self.description)


class VenueProfileColorGroup(AuditedModel):
    venue_profile = models.ForeignKey('VenueProfile')
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=32)

    def __unicode__(self):
        try:
            return u'%s-%s' % (self.name, self.venue_profile)
        except:
            return u''
class PointOfSale(Location):
    title = models.CharField(max_length=255)
    business_hours = models.CharField(max_length=255)

    def __unicode__(self):
        try:
            return u'%s' % self.title
        except:
            return u''
class ShowComponentsFilter(models.Model):
    show = models.ForeignKey('Show')
    performance = models.ManyToManyField('Performance')
    price_type = models.ManyToManyField('PriceType')
    price_category = models.ManyToManyField('PriceCategory')

    class Meta:
        abstract = True

    def getAdminData(self):
        show_id = self.show.id
        performances = {}
        price_types = {}
        price_categories = {}

        selected_performances = self.performance.all().values_list('id', flat=True)
        for perf in self.show.performances.all().values('id', 'admin_name'):
            perf['selected'] =  perf['id'] in selected_performances
            performances[perf['id']] = perf

        selected_price_types = self.price_type.all().values_list('id', flat=True)
        for ptype in PriceType.objects.filter(performance__show__id = show_id).values('id', 'performance', 'admin_name'):
            ptype['selected'] = ptype['id'] in selected_price_types
            price_types[ptype['id']] = ptype

        selected_price_categories = self.price_category.all().values_list('id', flat=True)
        for pcat in PriceCategory.objects.filter(price_type__performance__show__id = show_id).values('id', 'price_type', 'admin_name'):
            pcat['selected'] =  pcat['id'] in selected_price_categories
            price_categories[pcat['id']] = pcat

        data = {
            'performances':performances,
            'price_types':price_types,
            'price_categories':price_categories,
        }
        return data

class ShippingPointDetailsCreator(models.Model):
    shipping_point = models.ManyToManyField('ShippingPoint')
    show = models.ForeignKey('Show')
    performance = models.ManyToManyField('Performance')
   # content = models.ForeignKey(Content, null=True, blank = True)

    def create_shipping_point_details(self):
        for perf in self.performance.all():
            for shipping_point in self.shipping_point.all():
                try:
                    ShippingPointDetails.objects.create(shipping_point=shipping_point, performance=perf, content=self.content)
                except:
                    pass

    def __unicode__(self):
        return u'%s' % self.show.name

class ImportShowLog(models.Model):
    show = models.ForeignKey('shows.Show')
    date = models.DateTimeField(_('Created at'), auto_now_add=True)
  #  content = models.TextField(_('Log content'))

    def __unicode__(self):
        try:
            return u'%s-%s' % (self.show, self.date)
        except:
            return u''