#!/usr/bin/python

import os, json, math


REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats

PASS = "PASS"

TEXT_FORMAT = "text"  # question type when expected answer is a str, int, float, or bool

expected_json =    {"1": (TEXT_FORMAT, 977),
                    "2": (TEXT_FORMAT, 11230),
                    "3": (TEXT_FORMAT, 26500),
                    "4": (TEXT_FORMAT, 30200),
                    "5": (TEXT_FORMAT, 15090),
                    "6": (TEXT_FORMAT, 4915),
                    "7": (TEXT_FORMAT, 15765.2),
                    "8": (TEXT_FORMAT, 16740.4),
                    "9": (TEXT_FORMAT, 798.0),
                    "10": (TEXT_FORMAT, 82901),
                    "11": (TEXT_FORMAT, 313783),
                    "12": (TEXT_FORMAT, -568.5),
                    "13": (TEXT_FORMAT, -6608.0),
                    "14": (TEXT_FORMAT, 8630.666666666666),
                    "15": (TEXT_FORMAT, 9913.0),
                    "16": (TEXT_FORMAT, 77837.0),
                    "17": (TEXT_FORMAT, 57396.25),
                    "18": (TEXT_FORMAT, -3165.5),
                    "19": (TEXT_FORMAT, -17063.0),
                    "20": (TEXT_FORMAT, 1.37023509439786)}

def check_cell(qnum, actual):
    format, expected = expected_json[qnum[1:]]
    try:
        if format == TEXT_FORMAT:
            return simple_compare(expected, actual)
        else:
            if expected != actual:
                return "expected %s but found %s " % (repr(expected), repr(actual))
    except:
        if expected != actual:
            return "expected %s" % (repr(expected))
    return PASS


def simple_compare(expected, actual, complete_msg=True):
    msg = PASS
    if type(expected) == type:
        if expected != actual:
            if type(actual) == type:
                msg = "expected %s but found %s" % (expected.__name__, actual.__name__)
            else:
                msg = "expected %s but found %s" % (expected.__name__, repr(actual))
    elif type(expected) != type(actual) and not (type(expected) in [float, int] and type(actual) in [float, int]):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=REL_TOL, abs_tol=ABS_TOL):
            msg = "expected %s" % (repr(expected))
            if complete_msg:
                msg = msg + " but found %s" % (repr(actual))
    else:
        if expected != actual:
            msg = "expected %s" % (repr(expected))
            if complete_msg:
                msg = msg + " but found %s" % (repr(actual))
    return msg

def check(qnum, actual):
    msg = check_cell(qnum, actual)
    if msg == PASS:
        return True
    print("<b style='color: red;'>ERROR:</b> " + msg)
