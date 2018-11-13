# -*- coding: utf-8 -*-
"""
Database models for membership.
"""
from __future__ import absolute_import, unicode_literals
import logging
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from six import text_type
from openedx.core.djangoapps.xmodule_django.models import CourseKeyField
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from opaque_keys.edx.keys import CourseKey

log = logging.getLogger(__name__)


class VIPInfo(models.Model):
    """ VIP card information """

    user = models.ForeignKey(User, related_name="vip_user")
    start_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    class Meta(object):
        app_label = 'membership'

    def __unicode__(self):
        return self.user.username


class VIPPackage(models.Model):
    """ VIP package """

    name = models.CharField(max_length=64)
    month = models.IntegerField()
    is_active = models.BooleanField(default=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=30)
    suggested_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=30)
    is_recommended = models.BooleanField(default=False)

    class Meta(object):
        app_label = 'membership'

    def __unicode__(self):
        return self.name


class VIPOrder(models.Model):
    """ VIP order """

    STATUS_WAIT = 1  # Awaiting for payment
    STATUS_SUCCESS = 2    # Paid
    STATUS_FAILED = 3    # Cancelled
    STATUS_REFUND = 4   # Refunded

    STATUS_CHOICES = (
        (STATUS_WAIT, _(u'Awaiting for payment')),
        (STATUS_SUCCESS, _(u'Paid')),
        (STATUS_FAILED, _(u'Cancelled')),
        (STATUS_REFUND, _(u'Refunded'))
    )

    PAY_TYPE_NOT_ONLINE = 0  # Offline
    PAY_TYPE_BY_WECHAT = 1  # WeChat
    PAY_TYPE_BY_ALIPAY = 2  # Alipay
    PAY_TYPE_BY_UNIONPAY = 3  # Union pay
    PAY_TYPE_BY_APPLEPAY = 4   # Apple Pay
    PAY_TYPE_REMAIN_AMOUNT = 5  # Balance

    PAY_TYPE_CHOICES = (
        (PAY_TYPE_REMAIN_AMOUNT, _(u'Balance')),
        (PAY_TYPE_NOT_ONLINE, _(u'Offline')),
        (PAY_TYPE_BY_WECHAT, _(u'WeChat')),
        (PAY_TYPE_BY_ALIPAY, _(u'Alipay ')),
        (PAY_TYPE_BY_UNIONPAY, _(u'Union pay')),
        (PAY_TYPE_BY_APPLEPAY, _(u'Apple Pay'))
    )

    name = models.CharField(max_length=64)
    month = models.IntegerField()
    trans_at = models.DateTimeField(auto_now_add=True)
    start_at = models.DateTimeField()
    expired_at = models.DateTimeField()
    status = models.IntegerField(choices=STATUS_CHOICES)
    price = models.DecimalField(default=0.0, decimal_places=2, max_digits=30)
    suggested_price = models.DecimalField(default=0.0, decimal_places=2, max_digits=30)
    created_by = models.ForeignKey(User, related_name="vip_order")
    description = models.CharField(max_length=255, blank=True, null=True)
    refno = models.CharField(max_length=255, blank=True, null=True)
    openid = models.CharField(max_length=128, blank=True, null=True)
    outtradeno = models.CharField(max_length=120, blank=True, null=True)
    pay_type = models.IntegerField(null=False, choices=PAY_TYPE_CHOICES)
    receipt = models.TextField(blank=True, null=True)
    version = models.CharField(max_length=255, blank=True, null=True)
    os_version = models.CharField(max_length=255, blank=True, null=True)

    class Meta(object):
        app_label = 'membership'

    def __unicode__(self):
        return self.name


class VIPCourseEnrollment(models.Model):
    """ VIP user enrollment courses """

    user = models.ForeignKey(User)
    course_id = CourseKeyField(max_length=255, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta(object):
        app_label = 'membership'

    @classmethod
    def enroll(cls, user, course_key, is_active=True):
        """
        enroll course for vip user
        """
        try:
            course = CourseOverview.get_from_id(course_key)
        except CourseOverview.DoesNotExist:
            pass

        enrollment = cls.get_or_create_enrollment(user, course_key)

        return enrollment

    @classmethod
    def get_or_create_enrollment(cls, user, course_key):
        """
        """
        assert isinstance(course_key, CourseKey)

        if user.id is None:
            user.save()

        enrollment, __ = cls.objects.get_or_create(
            user=user,
            course_id=course_key,
            defaults={
                'is_active': True
            }
        )

        return enrollment


class VIPCoursePrice(models.Model):
    """ VIP course price """

    SUBSCRIBE_NORMAL = 0
    SUBSCRIBE_PAY = 1

    SUBSCRIBE_TYPE_CHOICES = (
        (SUBSCRIBE_NORMAL, u'subscribe normal'),
        (SUBSCRIBE_PAY, u'subscribe pay'),
    )
    course_id = CourseKeyField(max_length=255, db_index=True)
    subscribe = models.IntegerField(default=SUBSCRIBE_NORMAL, choices=SUBSCRIBE_TYPE_CHOICES)

    class Meta(object):
        app_label = 'membership'