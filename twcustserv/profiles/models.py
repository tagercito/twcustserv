# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db.utils import DatabaseError

from accounts.models import Account


DOC_TYPES = [('1', 'DNI'),
             ('2', 'Cedula'),
             ('3', 'Libreta de Enrolamiento'),
             ('4', 'Libreta Civica'),
             ('5', 'Pasaporte/Passport')]

REGISTRATION_SOURCES = {
    'websource': 'websource',
    'legacy': 'legacy',
    'social': 'social'
}

PROVINCIA_CHOICES = (('Buenos Aires', 'Buenos Aires'),
('Buenos Aires-GBA', 'Buenos Aires-GBA'),
('Capital Federal', 'Capital Federal'),
('Catamarca', 'Catamarca'),
('Chaco', 'Chaco'),
('Chubut', 'Chubut'),
('Cordoba', 'Cordoba'),
('Corrientes', 'Corrientes'),
('Entre Rios', 'Entre Rios'),
('Formosa', 'Formosa'),
('Jujuy', 'Jujuy'),
('La Pampa', 'La Pampa'),
('La Rioja', 'La Rioja'),
('Mendoza', 'Mendoza'),
('Misiones', 'Misiones'),
('Neuquen', 'Neuquen'),
('Rio Negro', 'Rio Negro'),
('Salta', 'Salta'),
('San Juan', 'San Juan'),
('San Luis', 'San Luis'),
('Santa Cruz', 'Santa Cruz'),
('Santa Fe', 'Santa Fe'),
('Santiago del Estero', 'Santiago del Estero'),
('Tierra del Fuego', 'Tierra del Fuego'),
('Tucuman', 'Tucuman'))


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    doc_type = models.CharField(_('Document Type'), max_length=10, choices=DOC_TYPES, null=True)
    doc_num = models.CharField(_('Document Number'), max_length=10, null=True)
    phone = models.CharField(_('Phone number'), max_length=32)
    source = models.CharField(_('Registration Source'), max_length=10, choices=REGISTRATION_SOURCES.items())
    newsletter = models.BooleanField(_("Accept newsletter"))
    user_id_legacy = models.CharField(_('ID from Legacy'), max_length=32, null=True)
    user_account_id = models.CharField(_('Accound ID'), max_length=32, null=True)
    legacy_password = models.CharField(_('Legacy Password'), max_length=255, null=True)
    migrated = models.BooleanField(_('Is Migrated'), default=False)

    class Meta:
        verbose_name = _('User profile')
        verbose_name_plural = _('User profiles')

    def __unicode__(self):
        return u"%s (%s - %s)" % (self.user.email, self.doc_type, self.doc_num)
