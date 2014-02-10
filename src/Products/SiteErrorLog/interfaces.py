# -*- coding: utf-8 -*-
from zope.interface import Interface, implements


class IErrorRaisedEvent(Interface):
    """
    An event that contains an error
    """


class ErrorRaisedEvent(dict):
    implements(IErrorRaisedEvent)
