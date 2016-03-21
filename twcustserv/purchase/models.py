from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
class Purchase(models.Model):
    performance = models.ForeignKey('shows.Performance', null=False)
#    price_categories = models.ManyToManyField('shows.PriceCategory', related_name = 'purchases', null=False)
    items = models.ManyToManyField('shows.PriceCategory', related_name='items', null=False, through='purchase.PurchaseItem')
    user = models.ForeignKey('auth.User', related_name='purchases', null=False)
    date = models.DateTimeField(auto_now_add=True)
    delivery = models.ForeignKey('shows.Delivery', null=False, blank=True)
    payment_method = models.CharField(max_length=32, null=False)
    payment_type = models.CharField(max_length=255, null=True)
    payment_hash = models.CharField(max_length=255, null=True)
    payment_data = models.CharField(max_length=32, null=True)
    shipping_info = models.CharField(max_length=255, null=True)
    shipping = models.BooleanField(_('is shipping?'))
    insured = models.BooleanField(_('is insured?'), default=False)
    insurance = models.IntegerField(default=0)
    br_name = models.CharField(_('Card name'), max_length=255, blank=True, null=True)
    expiry = models.CharField(_('Card expiry'), max_length=10, blank=True, null=True)
    printed_qty = models.IntegerField(default=0)

class PurchaseItem(models.Model):
    purchase = models.ForeignKey('purchase.Purchase')
    price_category = models.ForeignKey('shows.PriceCategory')
    quantity = models.PositiveIntegerField()
    item_data = models.CharField(max_length = 255, null=True)