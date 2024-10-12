#!/usr/bin/python
import os
import json
import math

MAX_FILE_SIZE = 500 # units - KB
REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats

PASS = "PASS"

TEXT_FORMAT = "text"  # question type when expected answer is a str, int, float, or bool
# question type when expected answer is a namedtuple
TEXT_FORMAT_NAMEDTUPLE = "text namedtuple"
# question type when the expected answer is a list where the order does *not* matter
TEXT_FORMAT_UNORDERED_LIST = "text list_unordered"
# question type when the expected answer is a list where the order does matter
TEXT_FORMAT_ORDERED_LIST = "text list_ordered"
# question type when the expected answer is a list of namedtuples where the order does matter
TEXT_FORMAT_ORDERED_LIST_NAMEDTUPLE = "text list_ordered namedtuple"
# question type when the expected answer is a list where order does matter, but with possible ties. Elements are ordered according to values in special_ordered_json (with ties allowed)
TEXT_FORMAT_SPECIAL_ORDERED_LIST = "text list_special_ordered"
# question type when the expected answer is a dictionary
TEXT_FORMAT_DICT = "text dict"


expected_json =    {"1": (TEXT_FORMAT, '1991 to 2000'),
                    "2": (TEXT_FORMAT, '1841 to 1850'),
                    "3": (TEXT_FORMAT_DICT, {'The Trees of the East': '2011 to 2020',
                                                     'Avengers: Infinity War': '2011 to 2020',
                                                     'Zodiac': '2001 to 2010',
                                                     'Top Gun: Maverick': '2021 to 2030',
                                                     'Space Jam: A New Legacy': '2021 to 2030',
                                                     'The Big Short': '2011 to 2020'}),
                    "4": (TEXT_FORMAT, 8.666666666666668),
                    "5": (TEXT_FORMAT_ORDERED_LIST,[('Avengers: Infinity War', 149),
                                         ('Space Jam: A New Legacy', 115),
                                         ('The Big Short', 130),
                                         ('The Trees of the East', 71),
                                         ('Top Gun: Maverick', 130),
                                         ('Zodiac', 157)] ),
                    "6": (TEXT_FORMAT_ORDERED_LIST, [('The Trees of the East', 71),
                                             ('Space Jam: A New Legacy', 115),
                                             ('Top Gun: Maverick', 130),
                                             ('The Big Short', 130),
                                             ('Avengers: Infinity War', 149),
                                             ('Zodiac', 157)]),
                    "7": (TEXT_FORMAT, 'The Trees of the East'),
                    "8": (TEXT_FORMAT_ORDERED_LIST, [{'title': 'Top Gun: Maverick',
                                              'year': 2022,
                                              'duration': 130,
                                              'genres': ['Action', 'Drama'],
                                              'rating': 8.4,
                                              'directors': ['Joseph Kosinski'],
                                              'cast': ['Tom Cruise', 'Jennifer Connelly', 'Miles Teller', 'Val Kilmer']},
                                             {'title': 'Space Jam: A New Legacy',
                                              'year': 2021,
                                              'duration': 115,
                                              'genres': ['Adventure', 'Animation', 'Comedy'],
                                              'rating': 4.5,
                                              'directors': ['Malcolm D. Lee'],
                                              'cast': ['LeBron James', 'Don Cheadle', 'Cedric Joe', 'Khris Davis']},
                                             {'title': 'The Trees of the East',
                                              'year': 2018,
                                              'duration': 71,
                                              'genres': ['Thriller'],
                                              'rating': 9.8,
                                              'directors': ['Mike Ellwood'],
                                              'cast': ['Pattyeffinmayo', 'Parlay Pass', 'Sia Poorak', 'Kandisha']},
                                             {'title': 'Avengers: Infinity War',
                                              'year': 2018,
                                              'duration': 149,
                                              'genres': ['Action', 'Adventure', 'Sci-Fi'],
                                              'rating': 8.4,
                                              'directors': ['Anthony Russo', 'Joe Russo'],
                                              'cast': ['Robert Downey Jr.',
                                               'Chris Hemsworth',
                                               'Mark Ruffalo',
                                               'Chris Evans']},
                                             {'title': 'The Big Short',
                                              'year': 2015,
                                              'duration': 130,
                                              'genres': ['Biography', 'Comedy', 'Drama'],
                                              'rating': 7.8,
                                              'directors': ['Adam McKay'],
                                              'cast': ['Christian Bale', 'Steve Carell', 'Ryan Gosling', 'Brad Pitt']},
                                             {'title': 'Zodiac',
                                              'year': 2007,
                                              'duration': 157,
                                              'genres': ['Crime', 'Drama', 'Mystery'],
                                              'rating': 7.7,
                                              'directors': ['David Fincher'],
                                              'cast': ['Jake Gyllenhaal',
                                               'Robert Downey Jr.',
                                               'Mark Ruffalo',
                                               'Anthony Edwards']}]),
                    "9": (TEXT_FORMAT, 'Space Jam: A New Legacy'),
                    "10": (TEXT_FORMAT, 15),
                    "movies-by-cast": (TEXT_FORMAT_DICT, {'Pattyeffinmayo': [{'title': 'The Trees of the East',
                                                           'year': 2018,
                                                           'duration': 71,
                                                           'genres': ['Thriller'],
                                                           'rating': 9.8,
                                                           'directors': ['Mike Ellwood'],
                                                           'cast': ['Pattyeffinmayo', 'Parlay Pass', 'Sia Poorak', 'Kandisha']}],
                                                         'Parlay Pass': [{'title': 'The Trees of the East',
                                                           'year': 2018,
                                                           'duration': 71,
                                                           'genres': ['Thriller'],
                                                           'rating': 9.8,
                                                           'directors': ['Mike Ellwood'],
                                                           'cast': ['Pattyeffinmayo', 'Parlay Pass', 'Sia Poorak', 'Kandisha']}],
                                                         'Sia Poorak': [{'title': 'The Trees of the East',
                                                           'year': 2018,
                                                           'duration': 71,
                                                           'genres': ['Thriller'],
                                                           'rating': 9.8,
                                                           'directors': ['Mike Ellwood'],
                                                           'cast': ['Pattyeffinmayo', 'Parlay Pass', 'Sia Poorak', 'Kandisha']}],
                                                         'Kandisha': [{'title': 'The Trees of the East',
                                                           'year': 2018,
                                                           'duration': 71,
                                                           'genres': ['Thriller'],
                                                           'rating': 9.8,
                                                           'directors': ['Mike Ellwood'],
                                                           'cast': ['Pattyeffinmayo', 'Parlay Pass', 'Sia Poorak', 'Kandisha']}],
                                                         'Robert Downey Jr.': [{'title': 'Avengers: Infinity War',
                                                           'year': 2018,
                                                           'duration': 149,
                                                           'genres': ['Action', 'Adventure', 'Sci-Fi'],
                                                           'rating': 8.4,
                                                           'directors': ['Anthony Russo', 'Joe Russo'],
                                                           'cast': ['Robert Downey Jr.',
                                                            'Chris Hemsworth',
                                                            'Mark Ruffalo',
                                                            'Chris Evans']},
                                                          {'title': 'Zodiac',
                                                           'year': 2007,
                                                           'duration': 157,
                                                           'genres': ['Crime', 'Drama', 'Mystery'],
                                                           'rating': 7.7,
                                                           'directors': ['David Fincher'],
                                                           'cast': ['Jake Gyllenhaal',
                                                            'Robert Downey Jr.',
                                                            'Mark Ruffalo',
                                                            'Anthony Edwards']}],
                                                         'Chris Hemsworth': [{'title': 'Avengers: Infinity War',
                                                           'year': 2018,
                                                           'duration': 149,
                                                           'genres': ['Action', 'Adventure', 'Sci-Fi'],
                                                           'rating': 8.4,
                                                           'directors': ['Anthony Russo', 'Joe Russo'],
                                                           'cast': ['Robert Downey Jr.',
                                                            'Chris Hemsworth',
                                                            'Mark Ruffalo',
                                                            'Chris Evans']}],
                                                         'Mark Ruffalo': [{'title': 'Avengers: Infinity War',
                                                           'year': 2018,
                                                           'duration': 149,
                                                           'genres': ['Action', 'Adventure', 'Sci-Fi'],
                                                           'rating': 8.4,
                                                           'directors': ['Anthony Russo', 'Joe Russo'],
                                                           'cast': ['Robert Downey Jr.',
                                                            'Chris Hemsworth',
                                                            'Mark Ruffalo',
                                                            'Chris Evans']},
                                                          {'title': 'Zodiac',
                                                           'year': 2007,
                                                           'duration': 157,
                                                           'genres': ['Crime', 'Drama', 'Mystery'],
                                                           'rating': 7.7,
                                                           'directors': ['David Fincher'],
                                                           'cast': ['Jake Gyllenhaal',
                                                            'Robert Downey Jr.',
                                                            'Mark Ruffalo',
                                                            'Anthony Edwards']}],
                                                         'Chris Evans': [{'title': 'Avengers: Infinity War',
                                                           'year': 2018,
                                                           'duration': 149,
                                                           'genres': ['Action', 'Adventure', 'Sci-Fi'],
                                                           'rating': 8.4,
                                                           'directors': ['Anthony Russo', 'Joe Russo'],
                                                           'cast': ['Robert Downey Jr.',
                                                            'Chris Hemsworth',
                                                            'Mark Ruffalo',
                                                            'Chris Evans']}],
                                                         'Jake Gyllenhaal': [{'title': 'Zodiac',
                                                           'year': 2007,
                                                           'duration': 157,
                                                           'genres': ['Crime', 'Drama', 'Mystery'],
                                                           'rating': 7.7,
                                                           'directors': ['David Fincher'],
                                                           'cast': ['Jake Gyllenhaal',
                                                            'Robert Downey Jr.',
                                                            'Mark Ruffalo',
                                                            'Anthony Edwards']}],
                                                         'Anthony Edwards': [{'title': 'Zodiac',
                                                           'year': 2007,
                                                           'duration': 157,
                                                           'genres': ['Crime', 'Drama', 'Mystery'],
                                                           'rating': 7.7,
                                                           'directors': ['David Fincher'],
                                                           'cast': ['Jake Gyllenhaal',
                                                            'Robert Downey Jr.',
                                                            'Mark Ruffalo',
                                                            'Anthony Edwards']}],
                                                         'Tom Cruise': [{'title': 'Top Gun: Maverick',
                                                           'year': 2022,
                                                           'duration': 130,
                                                           'genres': ['Action', 'Drama'],
                                                           'rating': 8.4,
                                                           'directors': ['Joseph Kosinski'],
                                                           'cast': ['Tom Cruise', 'Jennifer Connelly', 'Miles Teller', 'Val Kilmer']}],
                                                         'Jennifer Connelly': [{'title': 'Top Gun: Maverick',
                                                           'year': 2022,
                                                           'duration': 130,
                                                           'genres': ['Action', 'Drama'],
                                                           'rating': 8.4,
                                                           'directors': ['Joseph Kosinski'],
                                                           'cast': ['Tom Cruise', 'Jennifer Connelly', 'Miles Teller', 'Val Kilmer']}],
                                                         'Miles Teller': [{'title': 'Top Gun: Maverick',
                                                           'year': 2022,
                                                           'duration': 130,
                                                           'genres': ['Action', 'Drama'],
                                                           'rating': 8.4,
                                                           'directors': ['Joseph Kosinski'],
                                                           'cast': ['Tom Cruise', 'Jennifer Connelly', 'Miles Teller', 'Val Kilmer']}],
                                                         'Val Kilmer': [{'title': 'Top Gun: Maverick',
                                                           'year': 2022,
                                                           'duration': 130,
                                                           'genres': ['Action', 'Drama'],
                                                           'rating': 8.4,
                                                           'directors': ['Joseph Kosinski'],
                                                           'cast': ['Tom Cruise', 'Jennifer Connelly', 'Miles Teller', 'Val Kilmer']}],
                                                         'LeBron James': [{'title': 'Space Jam: A New Legacy',
                                                           'year': 2021,
                                                           'duration': 115,
                                                           'genres': ['Adventure', 'Animation', 'Comedy'],
                                                           'rating': 4.5,
                                                           'directors': ['Malcolm D. Lee'],
                                                           'cast': ['LeBron James', 'Don Cheadle', 'Cedric Joe', 'Khris Davis']}],
                                                         'Don Cheadle': [{'title': 'Space Jam: A New Legacy',
                                                           'year': 2021,
                                                           'duration': 115,
                                                           'genres': ['Adventure', 'Animation', 'Comedy'],
                                                           'rating': 4.5,
                                                           'directors': ['Malcolm D. Lee'],
                                                           'cast': ['LeBron James', 'Don Cheadle', 'Cedric Joe', 'Khris Davis']}],
                                                         'Cedric Joe': [{'title': 'Space Jam: A New Legacy',
                                                           'year': 2021,
                                                           'duration': 115,
                                                           'genres': ['Adventure', 'Animation', 'Comedy'],
                                                           'rating': 4.5,
                                                           'directors': ['Malcolm D. Lee'],
                                                           'cast': ['LeBron James', 'Don Cheadle', 'Cedric Joe', 'Khris Davis']}],
                                                         'Khris Davis': [{'title': 'Space Jam: A New Legacy',
                                                           'year': 2021,
                                                           'duration': 115,
                                                           'genres': ['Adventure', 'Animation', 'Comedy'],
                                                           'rating': 4.5,
                                                           'directors': ['Malcolm D. Lee'],
                                                           'cast': ['LeBron James', 'Don Cheadle', 'Cedric Joe', 'Khris Davis']}],
                                                         'Christian Bale': [{'title': 'The Big Short',
                                                           'year': 2015,
                                                           'duration': 130,
                                                           'genres': ['Biography', 'Comedy', 'Drama'],
                                                           'rating': 7.8,
                                                           'directors': ['Adam McKay'],
                                                           'cast': ['Christian Bale', 'Steve Carell', 'Ryan Gosling', 'Brad Pitt']}],
                                                         'Steve Carell': [{'title': 'The Big Short',
                                                           'year': 2015,
                                                           'duration': 130,
                                                           'genres': ['Biography', 'Comedy', 'Drama'],
                                                           'rating': 7.8,
                                                           'directors': ['Adam McKay'],
                                                           'cast': ['Christian Bale', 'Steve Carell', 'Ryan Gosling', 'Brad Pitt']}],
                                                         'Ryan Gosling': [{'title': 'The Big Short',
                                                           'year': 2015,
                                                           'duration': 130,
                                                           'genres': ['Biography', 'Comedy', 'Drama'],
                                                           'rating': 7.8,
                                                           'directors': ['Adam McKay'],
                                                           'cast': ['Christian Bale', 'Steve Carell', 'Ryan Gosling', 'Brad Pitt']}],
                                                         'Brad Pitt': [{'title': 'The Big Short',
                                                           'year': 2015,
                                                           'duration': 130,
                                                           'genres': ['Biography', 'Comedy', 'Drama'],
                                                           'rating': 7.8,
                                                           'directors': ['Adam McKay'],
                                                           'cast': ['Christian Bale', 'Steve Carell', 'Ryan Gosling', 'Brad Pitt']}]}),
                    "11": (TEXT_FORMAT, 2),
                    "12": (TEXT_FORMAT, 1),
                    "13": (TEXT_FORMAT, 'Robert Downey Jr.'),
                    "14": (TEXT_FORMAT, 8.1),
                    "15": (TEXT_FORMAT_DICT, {'Pattyeffinmayo': [9.8],
                                                         'Parlay Pass': [9.8],
                                                         'Sia Poorak': [9.8],
                                                         'Kandisha': [9.8],
                                                         'Robert Downey Jr.': [8.4, 7.7],
                                                         'Chris Hemsworth': [8.4],
                                                         'Mark Ruffalo': [8.4, 7.7],
                                                         'Chris Evans': [8.4],
                                                         'Jake Gyllenhaal': [7.7],
                                                         'Anthony Edwards': [7.7],
                                                         'Tom Cruise': [8.4],
                                                         'Jennifer Connelly': [8.4],
                                                         'Miles Teller': [8.4],
                                                         'Val Kilmer': [8.4],
                                                         'LeBron James': [4.5],
                                                         'Don Cheadle': [4.5],
                                                         'Cedric Joe': [4.5],
                                                         'Khris Davis': [4.5],
                                                         'Christian Bale': [7.8],
                                                         'Steve Carell': [7.8],
                                                         'Ryan Gosling': [7.8],
                                                         'Brad Pitt': [7.8]}),
                    "16": (TEXT_FORMAT, 8.05),
                    "17-1": (TEXT_FORMAT_DICT, {'Pattyeffinmayo': 9.8,
                                                         'Parlay Pass': 9.8,
                                                         'Sia Poorak': 9.8,
                                                         'Kandisha': 9.8,
                                                         'Robert Downey Jr.': 8.05,
                                                         'Chris Hemsworth': 8.4,
                                                         'Mark Ruffalo': 8.05,
                                                         'Chris Evans': 8.4,
                                                         'Jake Gyllenhaal': 7.7,
                                                         'Anthony Edwards': 7.7,
                                                         'Tom Cruise': 8.4,
                                                         'Jennifer Connelly': 8.4,
                                                         'Miles Teller': 8.4,
                                                         'Val Kilmer': 8.4,
                                                         'LeBron James': 4.5,
                                                         'Don Cheadle': 4.5,
                                                         'Cedric Joe': 4.5,
                                                         'Khris Davis': 4.5,
                                                         'Christian Bale': 7.8,
                                                         'Steve Carell': 7.8,
                                                         'Ryan Gosling': 7.8,
                                                         'Brad Pitt': 7.8}),
                    "17-2": (TEXT_FORMAT_DICT, {'Pattyeffinmayo': 9.8,
                                                         'Parlay Pass': 9.8,
                                                         'Sia Poorak': 9.8,
                                                         'Kandisha': 9.8,
                                                         'Robert Downey Jr.': 8.05,
                                                         'Chris Hemsworth': 8.4,
                                                         'Mark Ruffalo': 8.05,
                                                         'Chris Evans': 8.4,
                                                         'Jake Gyllenhaal': 7.7,
                                                         'Anthony Edwards': 7.7,
                                                         'Tom Cruise': 8.4,
                                                         'Jennifer Connelly': 8.4,
                                                         'Miles Teller': 8.4,
                                                         'Val Kilmer': 8.4,
                                                         'LeBron James': 4.5,
                                                         'Don Cheadle': 4.5,
                                                         'Cedric Joe': 4.5,
                                                         'Khris Davis': 4.5,
                                                         'Christian Bale': 7.8,
                                                         'Steve Carell': 7.8,
                                                         'Ryan Gosling': 7.8,
                                                         'Brad Pitt': 7.8}),
                    "18-1": (TEXT_FORMAT_DICT, {'Pattyeffinmayo': 9.8,
                                                         'Parlay Pass': 9.8,
                                                         'Sia Poorak': 9.8,
                                                         'Kandisha': 9.8,
                                                         'Robert Downey Jr.': 8.4,
                                                         'Chris Hemsworth': 8.4,
                                                         'Mark Ruffalo': 8.4,
                                                         'Chris Evans': 8.4,
                                                         'Jake Gyllenhaal': 7.7,
                                                         'Anthony Edwards': 7.7,
                                                         'Tom Cruise': 8.4,
                                                         'Jennifer Connelly': 8.4,
                                                         'Miles Teller': 8.4,
                                                         'Val Kilmer': 8.4,
                                                         'LeBron James': 4.5,
                                                         'Don Cheadle': 4.5,
                                                         'Cedric Joe': 4.5,
                                                         'Khris Davis': 4.5,
                                                         'Christian Bale': 7.8,
                                                         'Steve Carell': 7.8,
                                                         'Ryan Gosling': 7.8,
                                                         'Brad Pitt': 7.8}),
                    "18-2": (TEXT_FORMAT, 8.4),
                    "19": (TEXT_FORMAT_DICT, {'Pattyeffinmayo': 9.8,
                                                         'Parlay Pass': 9.8,
                                                         'Sia Poorak': 9.8,
                                                         'Kandisha': 9.8,
                                                         'Robert Downey Jr.': 8.4,
                                                         'Chris Hemsworth': 8.4,
                                                         'Mark Ruffalo': 8.4,
                                                         'Chris Evans': 8.4,
                                                         'Jake Gyllenhaal': 7.7,
                                                         'Anthony Edwards': 7.7,
                                                         'Tom Cruise': 8.4,
                                                         'Jennifer Connelly': 8.4,
                                                         'Miles Teller': 8.4,
                                                         'Val Kilmer': 8.4,
                                                         'LeBron James': 4.5,
                                                         'Don Cheadle': 4.5,
                                                         'Cedric Joe': 4.5,
                                                         'Khris Davis': 4.5,
                                                         'Christian Bale': 7.8,
                                                         'Steve Carell': 7.8,
                                                         'Ryan Gosling': 7.8,
                                                         'Brad Pitt': 7.8}),
                    "20": (TEXT_FORMAT_UNORDERED_LIST, ['LeBron James', 'Don Cheadle', 'Cedric Joe', 'Khris Davis'])}

def check_cell(qnum, actual):
    format, expected = expected_json[qnum[1:]]

    try:
        if format == TEXT_FORMAT:
            return simple_compare(expected, actual)
        elif format == TEXT_FORMAT_UNORDERED_LIST:
            return list_compare_unordered(expected, actual)
        elif format == TEXT_FORMAT_ORDERED_LIST:
            return list_compare_ordered(expected, actual)
        elif format == TEXT_FORMAT_SPECIAL_ORDERED_LIST:
            special_expected = special_json[qnum[1:]]
            return list_compare_special(special_expected, actual)
        elif format == TEXT_FORMAT_DICT:
            return dict_compare(expected, actual)
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
                msg = "expected %s but found %s" % (
                    expected.__name__, actual.__name__)
            else:
                msg = "expected %s but found %s" % (
                    expected.__name__, repr(actual))
    elif type(expected) != type(actual) and not (type(expected) in [float, int] and type(actual) in [float, int]):
        msg = "expected to find type %s but found type %s" % (
            type(expected).__name__, type(actual).__name__)
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


def namedtuple_compare(expected, actual):
    msg = PASS
    for field in expected._fields:
        val = simple_compare(getattr(expected, field), getattr(actual, field))
        if val != PASS:
            msg = "at attribute %s of namedtuple %s, " % (
                field, type(expected).__name__) + val
            return msg
    return msg


def list_compare_ordered(expected, actual, obj="list"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (
            type(expected).__name__, type(actual).__name__)
        return msg
    for i in range(len(expected)):
        if i >= len(actual):
            msg = "expected missing %s in %s" % (repr(expected[i]), obj)
            break
        if type(expected[i]) in [int, float, bool, str]:
            val = simple_compare(expected[i], actual[i])
        elif type(expected[i]) in [list]:
            val = list_compare_ordered(expected[i], actual[i], "sub" + obj)
        elif type(expected[i]) in [dict]:
            val = dict_compare(expected[i], actual[i])
        elif type(expected[i]).__name__ == obfuscate1():
            val = simple_compare(expected[i], actual[i])
        if val != PASS:
            msg = "at index %d of the %s, " % (i, obj) + val
            break
    if len(actual) > len(expected) and msg == PASS:
        msg = "found unexpected %s in %s" % (repr(actual[len(expected)]), obj)
    if len(expected) != len(actual):
        msg = msg + \
            " (found %d entries in %s, but expected %d)" % (
                len(actual), obj, len(expected))

    if len(expected) > 0 and type(expected[0]) in [int, float, bool, str]:
        if msg != PASS and list_compare_unordered(expected, actual, obj) == PASS:
            try:
                msg = msg + " (list may not be ordered as required)"
            except:
                pass
    return msg


def list_compare_helper(larger, smaller):
    msg = PASS
    j = 0
    for i in range(len(larger)):
        if i == len(smaller):
            msg = "expected %s" % (repr(larger[i]))
            break
        found = False
        while not found:
            if j == len(smaller):
                val = simple_compare(larger[i], smaller[j - 1], False)
                break
            val = simple_compare(larger[i], smaller[j], False)
            j += 1
            if val == PASS:
                found = True
                break
        if not found:
            msg = val
            break
    return msg


def list_compare_unordered(expected, actual, obj="list"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (
            type(expected).__name__, type(actual).__name__)
        return msg
    try:
        sort_expected = sorted(expected)
        sort_actual = sorted(actual)
    except:
        msg = "unexpected datatype found in %s; expected entries of type %s" % (
            obj, obj, type(expected[0]).__name__)
        return msg

    if len(actual) == 0 and len(expected) > 0:
        msg = "in the %s, missing" % (obj) + expected[0]
    elif len(actual) > 0 and len(expected) > 0:
        val = simple_compare(sort_expected[0], sort_actual[0])
        if val.startswith("expected to find type"):
            msg = "in the %s, " % (
                obj) + simple_compare(sort_expected[0], sort_actual[0])
        else:
            if len(expected) > len(actual):
                msg = "in the %s, missing " % (
                    obj) + list_compare_helper(sort_expected, sort_actual)
            elif len(expected) < len(actual):
                msg = "in the %s, found un" % (
                    obj) + list_compare_helper(sort_actual, sort_expected)
            if len(expected) != len(actual):
                msg = msg + \
                    " (found %d entries in %s, but expected %d)" % (
                        len(actual), obj, len(expected))
                return msg
            else:
                val = list_compare_helper(sort_expected, sort_actual)
                if val != PASS:
                    msg = "in the %s, missing " % (obj) + val + ", but found un" + list_compare_helper(sort_actual,
                                                                                                       sort_expected)
    return msg


def list_compare_special(special_expected, actual):
    msg = PASS
    expected_list = []
    for expected_item in special_expected:
        expected_list.extend(expected_item)
    val = list_compare_unordered(expected_list, actual)
    if val != PASS:
        msg = val
    else:
        i = 0
        for expected_item in special_expected:
            j = len(expected_item)
            actual_item = actual[i: i + j]
            val = list_compare_unordered(expected_item, actual_item)
            if val != PASS:
                if j == 1:
                    msg = "at index %d " % (i) + val
                else:
                    msg = "between indices %d and %d " % (i, i + j - 1) + val
                msg = msg + " (list may not be ordered as required)"
                break
            i += j

    return msg

def dict_compare(expected, actual, obj="dict"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (
            type(expected).__name__, type(actual).__name__)
        return msg
    try:
        expected_keys = sorted(list(expected.keys()))
        actual_keys = sorted(list(actual.keys()))
    except:
        msg = "unexpected datatype found in keys of dict; expect a dict with keys of type %s" % (
            type(expected_keys[0]).__name__)
        return msg
    val = list_compare_unordered(expected_keys, actual_keys, "dict")
    if val != PASS:
        msg = "bad keys in %s: " % (obj) + val
    if msg == PASS:
        for key in expected:
            if expected[key] == None or type(expected[key]) in [int, float, bool, str]:
                val = simple_compare(expected[key], actual[key])
            elif type(expected[key]) in [list]:
                val = list_compare_ordered(expected[key], actual[key], "value")
            elif type(expected[key]) in [dict]:
                val = dict_compare(expected[key], actual[key], "sub" + obj)
            if val != PASS:
                msg = "incorrect val for key %s in %s: " % (
                    repr(key), obj) + val
    return msg


def check(qnum, actual):
    msg = check_cell(qnum, actual)
    if msg == PASS:
        return True
    print("<b style='color: red;'>ERROR:</b> " + msg)

def check_file_size(path):
    size = os.path.getsize(path)
    assert size < MAX_FILE_SIZE * 10**3, "Your file is too big to be processed by Gradescope; please delete unnecessary output cells so your file size is < %s KB" % MAX_FILE_SIZE
