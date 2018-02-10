# -*- coding: utf-8 -*-
from mingtak.ECBase import _
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from zope import schema
from plone.z3cform import layout
from z3c.form import form
from plone.directives import form as Form


class ICustom(Form.Schema):

    dbString = schema.TextLine(
        title=_(u'DataBase connect setting string.'),
        description=_(u'String format referenced to Sqlalchemy'),
        required=True,
    )

    citySorted = schema.Text(
        title=_(u"Taiwan's Sorted City List."),
        required=False,
    )

    distList = schema.Text(
        title=_(u"Taiwan's District and ZIP Code List"),
        required=False,
    )

    # reCAPTCHA
    siteKey = schema.TextLine(
        title=_(u"Google reCAPTCHA's Site Key"),
        required=False,
    )

    secretKey = schema.TextLine(
        title=_(u"Google reCAPTCHA's Secret Key"),
        required=False,
    )


class CustomControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = ICustom

CustomControlPanelView = layout.wrap_form(CustomControlPanelForm, ControlPanelFormWrapper)
CustomControlPanelView.label = _(u"Custom Related Setting")
