#!/usr/bin/env python

"""
Copyright (c) 2006-2017 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

class BloblastBaseException(Exception):
    pass

class BloblastCompressionException(BloblastBaseException):
    pass

class BloblastConnectionException(BloblastBaseException):
    pass

class BloblastDataException(BloblastBaseException):
    pass

class BloblastFilePathException(BloblastBaseException):
    pass

class BloblastGenericException(BloblastBaseException):
    pass

class BloblastInstallationException(BloblastBaseException):
    pass

class BloblastMissingDependence(BloblastBaseException):
    pass

class BloblastMissingMandatoryOptionException(BloblastBaseException):
    pass

class BloblastMissingPrivileges(BloblastBaseException):
    pass

class BloblastNoneDataException(BloblastBaseException):
    pass

class BloblastNotVulnerableException(BloblastBaseException):
    pass

class BloblastSilentQuitException(BloblastBaseException):
    pass

class BloblastUserQuitException(BloblastBaseException):
    pass

class BloblastShellQuitException(BloblastBaseException):
    pass

class BloblastSkipTargetException(BloblastBaseException):
    pass

class BloblastSyntaxException(BloblastBaseException):
    pass

class BloblastSystemException(BloblastBaseException):
    pass

class BloblastThreadException(BloblastBaseException):
    pass

class BloblastTokenException(BloblastBaseException):
    pass

class BloblastUndefinedMethod(BloblastBaseException):
    pass

class BloblastUnsupportedDBMSException(BloblastBaseException):
    pass

class BloblastUnsupportedFeatureException(BloblastBaseException):
    pass

class BloblastValueException(BloblastBaseException):
    pass
