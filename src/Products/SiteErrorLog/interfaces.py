from zope.interface import Interface
from zope.interface import implementer


class IErrorRaisedEvent(Interface):
    """
    An event that contains an error
    """


@implementer(IErrorRaisedEvent)
class ErrorRaisedEvent(dict):
    pass
