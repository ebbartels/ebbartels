#!/usr/bin/python
import os, json, math
from collections import namedtuple

MAX_FILE_SIZE = 450 # units - KB
REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats

PASS = "PASS"

TEXT_FORMAT = "text"  # question type when expected answer is a str, int, float, or bool
TEXT_FORMAT_NAMEDTUPLE = "text namedtuple"  # question type when expected answer is a namedtuple
TEXT_FORMAT_UNORDERED_LIST = "text list_unordered"  # question type when the expected answer is a list where the order does *not* matter
TEXT_FORMAT_ORDERED_LIST = "text list_ordered"  # question type when the expected answer is a list where the order does matter
TEXT_FORMAT_SPECIAL_ORDERED_LIST = "text list_special_ordered"  # question type when the expected answer is a list where order does matter, but with possible ties. Elements are ordered according to values in special_ordered_json (with ties allowed)
TEXT_FORMAT_DICT = "text dict"  # question type when the expected answer is a dictionary
PNG_FORMAT_SCATTER = "png scatter" # question type when the expected answer is a scatter plot


def return_expected_json():
    f = open("practice_plots.json", encoding='utf-8')
    plots_data = json.load(f)
    f.close()
    expected_json =    {"1-1": (PNG_FORMAT_SCATTER, plots_data["1-1"]),
                        "1-2": (PNG_FORMAT_SCATTER, plots_data["1-2"]),
                        "2-1": (PNG_FORMAT_SCATTER, plots_data["2-1"]),
                        "2-2": (PNG_FORMAT_SCATTER, plots_data["2-2"]),
                        "3": (TEXT_FORMAT, 47),
                        "4": (TEXT_FORMAT, 9.116809116809117),
                        "5": (PNG_FORMAT_SCATTER, plots_data["5"]),
                        "6": (PNG_FORMAT_SCATTER, plots_data["6"]),
                        "7-1": (PNG_FORMAT_SCATTER, plots_data["7-1"]),
                        "7-2": (PNG_FORMAT_SCATTER, plots_data["7-2"]),
                        "8": (PNG_FORMAT_SCATTER, plots_data["8"]),
                        "9": (PNG_FORMAT_SCATTER, plots_data["9"]),
                        "10": (PNG_FORMAT_SCATTER, plots_data["10"]),
                        "11": (PNG_FORMAT_SCATTER, plots_data["11"]),
                        "12": (PNG_FORMAT_SCATTER, plots_data["12"]),
                        "13": (TEXT_FORMAT_ORDERED_LIST, ['rabbit', 'cat', 'lion', 'chimpanzee']),
                        "14": (TEXT_FORMAT_ORDERED_LIST, ['Adam', 'Bob', 'Chet', 'Bea', 'Treasure', 'Andy', 'Ann']),
                        "15": (TEXT_FORMAT_ORDERED_LIST, ['Adam',
                                                             'Bob',
                                                             'Chet',
                                                             'Cat',
                                                             'Barb',
                                                             'Bert',
                                                             'Alex',
                                                             'Bea',
                                                             'Gold',
                                                             'Andy',
                                                             'Ann']),
                        "16": (TEXT_FORMAT_ORDERED_LIST, ['file_1.json', 'sample_1', 'sample_2']),
                        "17": (TEXT_FORMAT, 1),
                        "18": (TEXT_FORMAT_ORDERED_LIST, [os.path.join("sample_data", "sample_1"),
                                                            os.path.join("sample_data", "sample_2")]),
                        "19": (TEXT_FORMAT, 2),
                        "20": (TEXT_FORMAT_ORDERED_LIST, [os.path.join("sample_data", "file_1.json"),
                                                            os.path.join("sample_data", "sample_1", "file_2.json"),
                                                            os.path.join("sample_data", "sample_1", "file_3.json"),
                                                            os.path.join("sample_data", "sample_2", "file_4.json"),
                                                            os.path.join("sample_data", "sample_2", "sample_3", "file_5.json")])}
    return expected_json

def check_cell(qnum, actual):
    expected_json = return_expected_json()
    format, expected = expected_json[qnum[1:]]
    try:
        if format == TEXT_FORMAT:
            return simple_compare(expected, actual)
        elif format == TEXT_FORMAT_UNORDERED_LIST:
            return list_compare_unordered(expected, actual)
        elif format == TEXT_FORMAT_ORDERED_LIST:
            return list_compare_ordered(expected, actual)
        elif format == TEXT_FORMAT_DICT:
            return dict_compare(expected, actual)
        elif format == TEXT_FORMAT_NAMEDTUPLE:
            return namedtuple_compare(expected, actual)
        elif format == PNG_FORMAT_SCATTER:
            return check_png_scatter(expected, actual)
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

namedtuples = ['Star', 'Planet']
star_attributes = ['spectral_type',
                  'stellar_effective_temperature',
                  'stellar_radius',
                  'stellar_mass',
                  'stellar_luminosity',
                  'stellar_surface_gravity',
                  'stellar_age']
# Create a namedtuple type, Star
Star = namedtuple("Star", star_attributes)
planets_attributes = ['planet_name',
                     'host_name',
                     'discovery_method',
                     'discovery_year',
                     'controversial_flag',
                     'orbital_period',
                     'planet_radius',
                     'planet_mass',
                     'semi_major_radius',
                     'eccentricity',
                     'equilibrium_temperature',
                     'insolation_flux']
# Create a namedtuple type, Planet
Planet = namedtuple("Planet", planets_attributes)

def namedtuple_compare(expected, actual):
    msg = PASS
    try:
        actual_fields = actual._fields
    except AttributeError:
        msg = "expected namedtuple but found %s" % (type(actual).__name__)
        return msg
    if type(expected).__name__ != type(actual).__name__:
        msg = "expected namedtuple %s but found namedtuple %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    expected_fields = expected._fields
    msg = list_compare_ordered(list(expected_fields), list(actual_fields), "namedtuple attributes")
    if msg != PASS:
        return msg
    for field in expected_fields:
        val = simple_compare(getattr(expected, field), getattr(actual, field))
        if val != PASS:
            msg = "at attribute %s of namedtuple %s, " % (field, type(expected).__name__) + val
            return msg
    return msg


def list_compare_ordered(expected, actual, obj="list"):
    msg = PASS
    if type(expected) != type(actual):
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    for i in range(len(expected)):
        if i >= len(actual):
            msg = "expected missing %s in %s" % (repr(expected[i]), obj)
            break
        if type(expected[i]) in [int, float, bool, str]:
            val = simple_compare(expected[i], actual[i])
        elif type(expected[i]) in [list, tuple]:
            val = list_compare_ordered(expected[i], actual[i], "sub" + obj)
        elif type(expected[i]) in [dict]:
            val = dict_compare(expected[i], actual[i])
        elif type(expected[i]).__name__ in namedtuples:
            val = namedtuple_compare(expected[i], actual[i])
        if val != PASS:
            msg = "at index %d of the %s, " % (i, obj) + val
            break
    if len(actual) > len(expected) and msg == PASS:
        msg = "found unexpected %s in %s" % (repr(actual[len(expected)]), obj)
    if len(expected) != len(actual):
        msg = msg + " (found %d entries in %s, but expected %d)" % (len(actual), obj, len(expected))

    if len(expected) > 0 and type(expected[0]) in [int, float, bool, str]:
        if msg != PASS and list_compare_unordered(expected, actual, obj) == PASS:
            try:
                msg = msg + " (%s may not be ordered as required)" % (obj)
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
                if type(larger[i]) in [list, tuple]:
                    val = list_compare_ordered(larger[i], smaller[j - 1])
                else:
                    val = simple_compare(larger[i], smaller[j - 1], False)
                break
            if type(larger[i]) in [list, tuple]:
                val = list_compare_ordered(larger[i], smaller[j])
            else:
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
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
        return msg
    try:
        sort_expected = sorted(expected)
        sort_actual = sorted(actual)
    except:
        msg = "unexpected datatype found in %s; expected entries of type %s" % (obj, obj, type(expected[0]).__name__)
        return msg

    if len(actual) == 0 and len(expected) > 0:
        msg = "in the %s, missing" % (obj) + expected[0]
    elif len(actual) > 0 and len(expected) > 0:
        val = simple_compare(sort_expected[0], sort_actual[0])
        if val.startswith("expected to find type"):
            msg = "in the %s, " % (obj) + simple_compare(sort_expected[0], sort_actual[0])
        else:
            if len(expected) > len(actual):
                msg = "in the %s, missing " % (obj) + list_compare_helper(sort_expected, sort_actual)
            elif len(expected) < len(actual):
                msg = "in the %s, found un" % (obj) + list_compare_helper(sort_actual, sort_expected)
            if len(expected) != len(actual):
                msg = msg + " (found %d entries in %s, but expected %d)" % (len(actual), obj, len(expected))
                return msg
            else:
                val = list_compare_helper(sort_expected, sort_actual)
                if val != PASS:
                    msg = "in the %s, missing " % (obj) + val + ", but found un" + list_compare_helper(sort_actual,
                                                                                               sort_expected)
    return msg

def list_compare_special_init(expected, special_order):
    real_expected = []
    for i in range(len(expected)):
        if real_expected == [] or special_order[i-1] != special_order[i]:
            real_expected.append([])
        real_expected[-1].append(expected[i])
    return real_expected


def list_compare_special(expected, actual, special_order):
    expected = list_compare_special_init(expected, special_order)
    msg = PASS
    expected_list = []
    for expected_item in expected:
        expected_list.extend(expected_item)
    val = list_compare_unordered(expected_list, actual)
    if val != PASS:
        msg = val
    else:
        i = 0
        for expected_item in expected:
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
        msg = "expected to find type %s but found type %s" % (type(expected).__name__, type(actual).__name__)
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
            elif type(expected[key]).__name__ in namedtuples:
                val = namedtuple_compare(expected[key], actual[key])
            if val != PASS:
                msg = "incorrect val for key %s in %s: " % (repr(key), obj) + val
    return msg

def helper_png_scatter(expected, actual):
    msg = PASS
    expected_length = len(list(expected.values())[0])
    for key in actual:
        if len(actual[key]) != expected_length:
            return "list '%s' has length %d but is expected to have length %d" % (key, len(actual[key]), expected_length)
    expected_plot_points = []
    actual_plot_points = []
    for i in range(expected_length):
        expected_point = []
        actual_point = []
        for key in expected:
            expected_point.append(expected[key][i])
            actual_point.append(actual[key][i])
        expected_plot_points.append(tuple(expected_point))
        actual_plot_points.append(tuple(actual_point))
    sorted_expected_points = sorted(expected_plot_points)
    sorted_actual_points = sorted(actual_plot_points)
    val = list_compare_ordered(sorted_expected_points, sorted_actual_points, "plot")
    if val != PASS:
        val = list_compare_ordered(expected_plot_points, actual_plot_points, "plot")
        bad_idx = int(val.split("index")[1].split()[0])
        msg = "in the plot, at index %d, expected point %s but found %s" % (bad_idx, expected_plot_points[bad_idx], actual_plot_points[bad_idx])
    return msg



def check_png_scatter(expected, actual):
    msg = PASS
    if type(list(expected.values())[0]) == list:
        msg = helper_png_scatter(expected, actual)
    elif type(list(expected.values())[0]) == dict:
        expected_keys = list(list(expected.values())[0].keys())
        for key in actual:
            val = list_compare_unordered(expected_keys, list(actual[key].keys()), "dictionary %s" % key)
            if val != PASS:
                return val
        expected_flipped = {}
        for key_1 in list(expected.values())[0]:
            expected_flipped[key_1] = {}
            for key_2 in expected:
                expected_flipped[key_1][key_2] = expected[key_2][key_1]
        actual_flipped = {}
        for key_1 in list(actual.values())[0]:
            actual_flipped[key_1] = {}
            for key_2 in actual:
                actual_flipped[key_1][key_2] = actual[key_2][key_1]
        for key in expected_flipped:
            val = helper_png_scatter(expected_flipped[key], actual_flipped[key])
            if val != PASS:
                if "length" in val:
                    msg = val.replace("list", "category '%s' of dictionary" % (key))
                else:
                    msg = val.replace("in the plot,", "in the plot, for the category '%s'," % (key))
                return msg
    return msg



def check(qnum, actual):
    msg = check_cell(qnum, actual)
    if msg == PASS:
        return True
    print("<b style='color: red;'>ERROR:</b> " + msg)


def check_file_size(path):
    size = os.path.getsize(path)
    assert size < MAX_FILE_SIZE * 10**3, "Your file is too big to be processed by Gradescope; please delete unnecessary output cells so your file size is < %s KB" % MAX_FILE_SIZE
