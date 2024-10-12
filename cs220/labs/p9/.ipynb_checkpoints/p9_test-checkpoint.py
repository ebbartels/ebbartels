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


expected_json = {"1": (TEXT_FORMAT, 7.65),
                 "2": (TEXT_FORMAT_ORDERED_LIST, [{'title': 'Avengers: Endgame',
                                                  'year': 2019,
                                                  'duration': 181,
                                                  'genres': ['Action', 'Adventure', 'Drama'],
                                                  'rating': 8.4,
                                                  'directors': ['Anthony Russo', 'Joe Russo'],
                                                  'cast': ['Robert Downey Jr.',
                                                   'Chris Evans',
                                                   'Mark Ruffalo',
                                                   'Chris Hemsworth']},
                                                 {'title': 'Avengers: Infinity War',
                                                  'year': 2018,
                                                  'duration': 149,
                                                  'genres': ['Action', 'Adventure', 'Sci-Fi'],
                                                  'rating': 8.4,
                                                  'directors': ['Anthony Russo', 'Joe Russo'],
                                                  'cast': ['Robert Downey Jr.',
                                                   'Chris Hemsworth',
                                                   'Mark Ruffalo',
                                                   'Chris Evans']}]),
                 "3": (TEXT_FORMAT_ORDERED_LIST, [{'title': 'Eat Pray Love',
                                                  'year': 2010,
                                                  'duration': 133,
                                                  'genres': ['Biography', 'Drama', 'Romance'],
                                                  'rating': 5.8,
                                                  'directors': ['Ryan Murphy'],
                                                  'cast': ['Julia Roberts',
                                                   'Javier Bardem',
                                                   'Richard Jenkins',
                                                   'Viola Davis']},
                                                 {'title': "Won't Back Down",
                                                  'year': 2012,
                                                  'duration': 121,
                                                  'genres': ['Drama'],
                                                  'rating': 6.4,
                                                  'directors': ['Daniel Barnz'],
                                                  'cast': ['Viola Davis', 'Maggie Gyllenhaal', 'Holly Hunter', 'Oscar Isaac']},
                                                 {'title': 'Get on Up',
                                                  'year': 2014,
                                                  'duration': 139,
                                                  'genres': ['Biography', 'Drama', 'Music'],
                                                  'rating': 6.9,
                                                  'directors': ['Tate Taylor'],
                                                  'cast': ['Chadwick Boseman', 'Nelsan Ellis', 'Dan Aykroyd', 'Viola Davis']},
                                                 {'title': 'The Disappearance of Eleanor Rigby: Them',
                                                  'year': 2014,
                                                  'duration': 123,
                                                  'genres': ['Drama', 'Romance'],
                                                  'rating': 6.3,
                                                  'directors': ['Ned Benson'],
                                                  'cast': ['James McAvoy', 'Jessica Chastain', 'Viola Davis', 'Bill Hader']},
                                                 {'title': 'Suicide Squad',
                                                  'year': 2016,
                                                  'duration': 123,
                                                  'genres': ['Action', 'Adventure', 'Fantasy'],
                                                  'rating': 5.9,
                                                  'directors': ['David Ayer'],
                                                  'cast': ['Will Smith', 'Jared Leto', 'Margot Robbie', 'Viola Davis']},
                                                 {'title': 'Blackhat',
                                                  'year': 2015,
                                                  'duration': 133,
                                                  'genres': ['Action', 'Crime', 'Thriller'],
                                                  'rating': 5.4,
                                                  'directors': ['Michael Mann'],
                                                  'cast': ['Chris Hemsworth', 'Viola Davis', 'Leehom Wang']},
                                                 {'title': 'Widows',
                                                  'year': 2018,
                                                  'duration': 129,
                                                  'genres': ['Crime', 'Drama', 'Thriller'],
                                                  'rating': 6.8,
                                                  'directors': ['Steve McQueen'],
                                                  'cast': ['Viola Davis', 'Michelle Rodriguez', 'Elizabeth Debicki']},
                                                 {'title': 'The Woman King',
                                                  'year': 2022,
                                                  'duration': 135,
                                                  'genres': ['Action', 'Drama', 'History'],
                                                  'rating': 6.8,
                                                  'directors': ['Gina Prince-Bythewood'],
                                                  'cast': ['Viola Davis', 'Thuso Mbedu', 'Sheila Atim']},
                                                 {'title': 'Black Theater Today: 2005',
                                                  'year': 2005,
                                                  'duration': 60,
                                                  'genres': ['Documentary', 'Family'],
                                                  'rating': 6.1,
                                                  'directors': ['Thea Marie Perkins'],
                                                  'cast': ['Virginia Capers', 'Keith David', 'Viola Davis', 'Richard Gant']},
                                                 {'title': "Ma Rainey's Black Bottom",
                                                  'year': 2020,
                                                  'duration': 94,
                                                  'genres': ['Drama', 'Music'],
                                                  'rating': 6.9,
                                                  'directors': ['George C. Wolfe'],
                                                  'cast': ['Viola Davis',
                                                   'Chadwick Boseman',
                                                   'Glynn Turman',
                                                   'Colman Domingo']},
                                                 {'title': 'Troop Zero',
                                                  'year': 2019,
                                                  'duration': 94,
                                                  'genres': ['Comedy', 'Drama', 'Family'],
                                                  'rating': 6.8,
                                                  'directors': ['Bert', 'Bertie'],
                                                  'cast': ['Mckenna Grace', 'Viola Davis', 'Jim Gaffigan', 'Allison Janney']},
                                                 {'title': 'The Architect',
                                                  'year': 2006,
                                                  'duration': 82,
                                                  'genres': ['Crime', 'Drama', 'Romance'],
                                                  'rating': 5.5,
                                                  'directors': ['Matt Tauber'],
                                                  'cast': ['Anthony LaPaglia',
                                                   'Viola Davis',
                                                   'Isabella Rossellini',
                                                   'Hayden Panettiere']},
                                                 {'title': 'Nights in Rodanthe',
                                                  'year': 2008,
                                                  'duration': 97,
                                                  'genres': ['Drama', 'Romance'],
                                                  'rating': 6.0,
                                                  'directors': ['George C. Wolfe'],
                                                  'cast': ['Diane Lane', 'Richard Gere', 'Christopher Meloni', 'Viola Davis']},
                                                 {'title': 'Custody',
                                                  'year': 2016,
                                                  'duration': 104,
                                                  'genres': ['Drama'],
                                                  'rating': 6.5,
                                                  'directors': ['James Lapine'],
                                                  'cast': ['Viola Davis',
                                                   'Hayden Panettiere',
                                                   'Catalina Sandino Moreno',
                                                   'Tony Shalhoub']},
                                                 {'title': 'The Unforgivable',
                                                  'year': 2021,
                                                  'duration': 112,
                                                  'genres': ['Crime', 'Drama'],
                                                  'rating': 7.1,
                                                  'directors': ['Nora Fingscheidt'],
                                                  'cast': ['Sandra Bullock',
                                                   'Viola Davis',
                                                   "Vincent D'Onofrio",
                                                   'Jon Bernthal']},
                                                 {'title': 'Prisoners',
                                                  'year': 2013,
                                                  'duration': 153,
                                                  'genres': ['Crime', 'Drama', 'Mystery'],
                                                  'rating': 8.1,
                                                  'directors': ['Denis Villeneuve'],
                                                  'cast': ['Hugh Jackman', 'Jake Gyllenhaal', 'Viola Davis', 'Melissa Leo']},
                                                 {'title': 'The Help',
                                                  'year': 2011,
                                                  'duration': 146,
                                                  'genres': ['Drama'],
                                                  'rating': 8.1,
                                                  'directors': ['Tate Taylor'],
  'cast': ['Viola Davis',
   'Emma Stone',
   'Octavia Spencer',
   'Bryce Dallas Howard']},
                                                 {'title': 'Beautiful Creatures',
                                                  'year': 2013,
                                                  'duration': 124,
                                                  'genres': ['Drama', 'Fantasy', 'Romance'],
                                                  'rating': 6.1,
                                                  'directors': ['Richard LaGravenese'],
                                                  'cast': ['Alice Englert',
                                                   'Viola Davis',
                                                   'Emma Thompson',
                                                   'Alden Ehrenreich']},
                                                 {'title': 'Lila & Eve',
                                                  'year': 2015,
                                                  'duration': 94,
                                                  'genres': ['Crime', 'Drama', 'Thriller'],
                                                  'rating': 5.8,
                                                  'directors': ['Charles Stone III'],
                                                  'cast': ['Viola Davis', 'Aml Ameen', 'Ron Caldwell', 'Yolonda Ross']},
                                                 {'title': 'The Disappearance of Eleanor Rigby: Her',
                                                  'year': 2013,
                                                  'duration': 100,
                                                  'genres': ['Drama', 'Romance'],
                                                  'rating': 6.9,
                                                  'directors': ['Ned Benson'],
                                                  'cast': ['Jessica Chastain', 'James McAvoy', 'Nina Arianda', 'Viola Davis']},
                                                 {'title': 'The Disappearance of Eleanor Rigby: Him',
                                                  'year': 2013,
                                                  'duration': 89,
                                                  'genres': ['Drama', 'Romance'],
                                                  'rating': 6.8,
                                                  'directors': ['Ned Benson'],
                                                  'cast': ['James McAvoy', 'Jessica Chastain', 'Nina Arianda', 'Viola Davis']},
                                                 {'title': 'Solaris',
                                                  'year': 2002,
                                                  'duration': 99,
                                                  'genres': ['Drama', 'Mystery', 'Romance'],
                                                  'rating': 6.2,
                                                  'directors': ['Steven Soderbergh'],
                                                  'cast': ['George Clooney',
                                                   'Natascha McElhone',
                                                   'Ulrich Tukur',
                                                   'Viola Davis']},
                                                 {'title': 'Beyond Babyland',
                                                  'year': 2010,
                                                  'duration': 56,
                                                  'genres': ['Documentary'],
                                                  'rating': 4.9,
                                                  'directors': ['David Appleby', 'Craig Leake'],
                                                  'cast': ['Viola Davis']},
                                                 {'title': 'Doubt',
                                                  'year': 2008,
                                                  'duration': 104,
                                                  'genres': ['Drama', 'Mystery'],
                                                  'rating': 7.5,
                                                  'directors': ['John Patrick Shanley'],
                                                  'cast': ['Meryl Streep',
                                                   'Philip Seymour Hoffman',
                                                   'Amy Adams',
                                                   'Viola Davis']}]),
                 "4": (TEXT_FORMAT_DICT, {'Drama': 106162,
                                             'Horror': 16606,
                                             'Sport': 2157,
                                             'Family': 8993,
                                             'Comedy': 57265,
                                             'Adventure': 14666,
                                             'Thriller': 20144,
                                             'Crime': 20655,
                                             'Action': 23495,
                                             'Fantasy': 7038,
                                             'History': 5183,
                                             'Romance': 26780,
                                             'Biography': 4946,
                                             'Sci-Fi': 5677,
                                             'Mystery': 9397,
                                             'Documentary': 10038,
                                             'Western': 4595,
                                             'Musical': 5198,
                                             'Animation': 3780,
                                             'Music': 4002,
                                             'War': 4873,
                                             'News': 152,
                                             'Film-Noir': 818,
                                             'Short': 12,
                                             'Reality-TV': 17,
                                             'Game-Show': 1,
                                             'Talk-Show': 1}),
                 "5": (TEXT_FORMAT_DICT, {'Action': 8,
                                             'Drama': 32,
                                             'War': 2,
                                             'Thriller': 4,
                                             'Adventure': 5,
                                             'Fantasy': 1,
                                             'Biography': 1,
                                             'History': 3,
                                             'Crime': 5,
                                             'Mystery': 2,
                                             'Film-Noir': 1,
                                             'Romance': 3}),
                 "6": (TEXT_FORMAT_DICT, {'1991 to 2000': 18496,
                                             '2021 to 2030': 9173,
                                             '1961 to 1970': 14216,
                                             '1951 to 1960': 10981,
                                             '2011 to 2020': 59249,
                                             '2001 to 2010': 33658,
                                             '1941 to 1950': 7807,
                                             '1971 to 1980': 15556,
                                             '1981 to 1990': 17181,
                                             '1921 to 1930': 3014,
                                             '1931 to 1940': 8201,
                                             '1911 to 1920': 1068,
                                             '1901 to 1910': 9,
                                             '1891 to 1900': 1}),
                 "7": (TEXT_FORMAT_DICT, {'Drama': 6.3,
                                                 'Horror': 5.0,
                                                 'Sport': 6.4,
                                                 'Family': 6.2,
                                                 'Comedy': 6.0,
                                                 'Adventure': 6.0,
                                                 'Thriller': 5.6,
                                                 'Crime': 6.1,
                                                 'Action': 5.8,
                                                 'Fantasy': 6.0,
                                                 'History': 6.7,
                                                 'Romance': 6.2,
                                                 'Biography': 6.8,
                                                 'Sci-Fi': 5.4,
                                                 'Mystery': 5.9,
                                                 'Documentary': 7.3,
                                                 'Western': 6.0,
                                                 'Musical': 6.2,
                                                 'Animation': 6.5,
                                                 'Music': 6.5,
                                                 'War': 6.5,
                                                 'News': 7.4,
                                                 'Film-Noir': 6.5,
                                                 'Short': 7.0,
                                                 'Reality-TV': 6.6,
                                                 'Game-Show': 3.3,
                                                 'Talk-Show': 2.8}),
                 "8": (TEXT_FORMAT_SPECIAL_ORDERED_LIST, None),
                 "9": (TEXT_FORMAT_ORDERED_LIST, [{'title': 'Shrek',
                                                  'year': 2001,
                                                  'duration': 90,
                                                  'genres': ['Adventure', 'Animation', 'Comedy'],
                                                  'rating': 7.9,
                                                  'directors': ['Andrew Adamson', 'Vicky Jenson'],
                                                  'cast': ['Mike Myers', 'Eddie Murphy', 'Cameron Diaz', 'John Lithgow']},
                                                 {'title': 'Shrek 2',
                                                  'year': 2004,
                                                  'duration': 93,
                                                  'genres': ['Adventure', 'Animation', 'Comedy'],
                                                  'rating': 7.3,
                                                  'directors': ['Andrew Adamson', 'Kelly Asbury', 'Conrad Vernon'],
                                                  'cast': ['Mike Myers', 'Eddie Murphy', 'Cameron Diaz', 'Julie Andrews']},
                                                 {'title': 'Shrek the Third',
                                                  'year': 2007,
                                                  'duration': 93,
                                                  'genres': ['Adventure', 'Animation', 'Comedy'],
                                                  'rating': 6.1,
                                                  'directors': ['Chris Miller', 'Raman Hui'],
                                                  'cast': ['Mike Myers', 'Cameron Diaz', 'Eddie Murphy', 'Antonio Banderas']},
                                                 {'title': 'Shrek Forever After',
                                                  'year': 2010,
                                                  'duration': 95,
                                                  'genres': ['Adventure', 'Animation', 'Comedy'],
                                                  'rating': 6.3,
                                                  'directors': ['Mike Mitchell'],
                                                  'cast': ['Mike Myers', 'Cameron Diaz', 'Eddie Murphy', 'Antonio Banderas']},
                                                 {'title': 'Shrek 2 Retold',
                                                  'year': 2021,
                                                  'duration': 92,
                                                  'genres': ['Animation'],
                                                  'rating': 8.7,
                                                  'directors': ['Grant Duffrin', 'Conner Japikse'],
                                                  'cast': ['Adam Carbone', 'Bostweek Lewis', 'Nb']}]),
                 "10": (TEXT_FORMAT_SPECIAL_ORDERED_LIST, None)}

special_json = {"8": [['News'],
                     ['Documentary'],
                     ['Short'],
                     ['Biography'],
                     ['History'],
                     ['Reality-TV'],
                     ['Animation', 'Music', 'War', 'Film-Noir'],
                     ['Sport'],
                     ['Drama'],
                     ['Family', 'Romance', 'Musical'],
                     ['Crime'],
                     ['Comedy', 'Adventure', 'Fantasy', 'Western'],
                     ['Mystery'],
                     ['Action'],
                     ['Thriller'],
                     ['Sci-Fi'],
                     ['Horror'],
                     ['Game-Show'],
                     ['Talk-Show']],
                "10": [['Tony Scott'],
                     ['Antoine Fuqua'],
                     ['Edward Zwick'],
                     ['Carl Franklin', 'Jonathan Demme', 'Spike Lee'],
                     ['Penny Marshall',
                      'Ridley Scott',
                      'Mira Nair',
                      'Albert Hughes',
                      'Allen Hughes',
                      'John Scheinfeld',
                      'Gregory Hoblit',
                      'Norman Jewison',
                      'Carl Schenkel',
                      'Baltasar Kormákur',
                      'Robert Zemeckis',
                      'Joel Coen',
                      'Boaz Yakin',
                      'Phillip Noyce',
                      'Nick Cassavetes',
                      'Martin Stellman',
                      'Daniel Espinosa',
                      'Brett Leonard',
                      'Russell Mulcahy',
                      'James D. Parriott',
                      'Richard Attenborough',
                      'John Lee Hancock',
                      'Alan J. Pakula']]}


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
