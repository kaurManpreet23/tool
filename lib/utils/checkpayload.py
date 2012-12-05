#!/usr/bin/env python

"""
Copyright (c) 2006-2012 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""

from re import sub, search

from lib.core.common import readXmlFile, urldecode
from lib.core.data import paths, logger

rules = None

def __adjustGrammar(string):
    string = sub('\ADetects', 'Detected', string)
    string = sub('\Afinds', 'Found', string)
    string = sub('attempts\Z', 'attempt', string)
    string = sub('injections\Z', 'injection', string)
    string = sub('attacks\Z', 'attack', string)

    return string

def checkPayload(payload):
    """
    This method checks if the generated payload is detectable by the
    PHPIDS filter rules
    """

    if not payload:
        return

    global rules

    detected = False
    payload = urldecode(payload, convall=True)

    if not rules:
        xmlrules = readXmlFile(paths.PHPIDS_RULES_XML)
        rules = []

        for xmlrule in xmlrules.getElementsByTagName("filter"):
            rule = "(?i)%s" % xmlrule.getElementsByTagName('rule')[0].childNodes[0].nodeValue
            desc = __adjustGrammar(xmlrule.getElementsByTagName('description')[0].childNodes[0].nodeValue)
            rules.append((rule, desc))

    if payload:
        for rule, desc in rules:
            if search(rule, payload):
                detected = True
                logger.warn("highly probable IDS/IPS detection: '%s: %s'" % (desc, payload))

    if not detected:
        logger.warn("payload '%s' possibly gone undetected" % payload)
