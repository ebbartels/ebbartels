#!/usr/bin/python

import os, json, math


REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats

PASS = "PASS"

TEXT_FORMAT = "text"  # question type when expected answer is a str, int, float, or bool

expected_json =    {"1": (TEXT_FORMAT, 850),
                    "2": (TEXT_FORMAT, 426),
                    "3": (TEXT_FORMAT, 3664),
                    "4": (TEXT_FORMAT, 154840),
                    "5": (TEXT_FORMAT, 154840),
                    "6": (TEXT_FORMAT, 1574),
                    "7": (TEXT_FORMAT, 18019),
                    "8": (TEXT_FORMAT, 220),
                    "9": (TEXT_FORMAT, 200),
                    "10": (TEXT_FORMAT, 400),
                    "11": (TEXT_FORMAT, 19.0),
                    "12": (TEXT_FORMAT, 42.5),
                    "13": (TEXT_FORMAT, 50),
                    "14": (TEXT_FORMAT, 30),
                    "15": (TEXT_FORMAT, -8.0),
                    "16": (TEXT_FORMAT, 1.0),
                    "17": (TEXT_FORMAT, -0.2857142857142857),
                    "18": (TEXT_FORMAT, -1.25),
                    "19": (TEXT_FORMAT, -0.1111111111111111),
                    "20": (TEXT_FORMAT, -0.6666666666666666)}

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
