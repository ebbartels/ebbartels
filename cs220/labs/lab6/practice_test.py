#!/usr/bin/python
import os, json, math


REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats

PASS = "PASS"

TEXT_FORMAT = "text"  # question type when expected answer is a str, int, float, or bool
TEXT_FORMAT_NAMEDTUPLE = "text namedtuple"  # question type when expected answer is a namedtuple
TEXT_FORMAT_UNORDERED_LIST = "text list_unordered"  # question type when the expected answer is a list where the order does *not* matter
TEXT_FORMAT_ORDERED_LIST = "text list_ordered"  # question type when the expected answer is a list where the order does matter
TEXT_FORMAT_ORDERED_LIST_NAMEDTUPLE = "text list_ordered namedtuple"  # question type when the expected answer is a list of namedtuples where the order does matter
TEXT_FORMAT_SPECIAL_ORDERED_LIST = "text list_special_ordered"  # question type when the expected answer is a list where order does matter, but with possible ties. Elements are ordered according to values in special_ordered_json (with ties allowed)
TEXT_FORMAT_DICT = "text dict"  # question type when the expected answer is a dictionary
TEXT_FORMAT_LIST_DICTS_ORDERED = "text list_dicts_ordered"  # question type when the expected answer is a list of dicts where the order does matter


expected_json = {"1": (TEXT_FORMAT_ORDERED_LIST, ['room_id',
                                                  'name',
                                                  'host_id',
                                                  'host_name',
                                                  'neighborhood_group',
                                                  'neighborhood',
                                                  'latitude',
                                                  'longitude',
                                                  'room_type',
                                                  'price',
                                                  'minimum_nights',
                                                  'number_of_reviews',
                                                  'last_review',
                                                  'reviews_per_month',
                                                  'calculated_host_listings_count',
                                                  'availability_365']),
                 "2-1": (TEXT_FORMAT, 48895),
                 "2-2": (TEXT_FORMAT_ORDERED_LIST, [['2539',
                                                  'Clean & quiet apt home by the park',
                                                  '2787',
                                                  'John',
                                                  'Brooklyn',
                                                  'Kensington',
                                                  '40.64749000000001',
                                                  '-73.97237',
                                                  'Private room',
                                                  '149',
                                                  '1',
                                                  '9',
                                                  '2018-10-19',
                                                  '0.21',
                                                  '6',
                                                  '365'],
                                                 ['2595',
                                                  'Skylit Midtown Castle',
                                                  '2845',
                                                  'Jennifer',
                                                  'Manhattan',
                                                  'Midtown',
                                                  '40.75362',
                                                  '-73.98376999999998',
                                                  'Entire home/apt',
                                                  '225',
                                                  '1',
                                                  '45',
                                                  '2019-05-21',
                                                  '0.38',
                                                  '2',
                                                  '355'],
                                                 ['3647',
                                                  'THE VILLAGE OF HARLEM....NEW YORK !',
                                                  '4632',
                                                  'Elisabeth',
                                                  'Manhattan',
                                                  'Harlem',
                                                  '40.80902',
                                                  '-73.9419',
                                                  'Private room',
                                                  '150',
                                                  '3',
                                                  '0',
                                                  '',
                                                  '',
                                                  '1',
                                                  '365'],
                                                 ['3831',
                                                  'Cozy Entire Floor of Brownstone',
                                                  '4869',
                                                  'LisaRoxanne',
                                                  'Brooklyn',
                                                  'Clinton Hill',
                                                  '40.68514',
                                                  '-73.95976',
                                                  'Entire home/apt',
                                                  '89',
                                                  '1',
                                                  '270',
                                                  '2019-07-05',
                                                  '4.64',
                                                  '1',
                                                  '194'],
                                                 ['5022',
                                                  'Entire Apt: Spacious Studio/Loft by central park',
                                                  '7192',
                                                  'Laura',
                                                  'Manhattan',
                                                  'East Harlem',
                                                  '40.79851',
                                                  '-73.94399',
                                                  'Entire home/apt',
                                                  '80',
                                                  '10',
                                                  '9',
                                                  '2018-11-19',
                                                  '0.1',
                                                  '1',
                                                  '0'],
                                                 ['5099',
                                                  'Large Cozy 1 BR Apartment In Midtown East',
                                                  '7322',
                                                  'Chris',
                                                  'Manhattan',
                                                  'Murray Hill',
                                                  '40.74767',
                                                  '-73.975',
                                                  'Entire home/apt',
                                                  '200',
                                                  '3',
                                                  '74',
                                                  '2019-06-22',
                                                  '0.59',
                                                  '1',
                                                  '129'],
                                                 ['5121',
                                                  'BlissArtsSpace!',
                                                  '7356',
                                                  'Garon',
                                                  'Brooklyn',
                                                  'Bedford-Stuyvesant',
                                                  '40.68688',
                                                  '-73.95596',
                                                  'Private room',
                                                  '60',
                                                  '45',
                                                  '49',
                                                  '2017-10-05',
                                                  '0.4',
                                                  '1',
                                                  '0'],
                                                 ['5178',
                                                  "Large Furnished Room Near B'way ",
                                                  '8967',
                                                  'Shunichi',
                                                  'Manhattan',
                                                  "Hell's Kitchen",
                                                  '40.76489',
                                                  '-73.98493',
                                                  'Private room',
                                                  '79',
                                                  '2',
                                                  '430',
                                                  '2019-06-24',
                                                  '3.47',
                                                  '1',
                                                  '220'],
                                                 ['5203',
                                                  'Cozy Clean Guest Room - Family Apt',
                                                  '7490',
                                                  'MaryEllen',
                                                  'Manhattan',
                                                  'Upper West Side',
                                                  '40.80178',
                                                  '-73.96723',
                                                  'Private room',
                                                  '79',
                                                  '2',
                                                  '118',
                                                  '2017-07-21',
                                                  '0.99',
                                                  '1',
                                                  '0'],
                                                 ['5238',
                                                  'Cute & Cozy Lower East Side 1 bdrm',
                                                  '7549',
                                                  'Ben',
                                                  'Manhattan',
                                                  'Chinatown',
                                                  '40.71344000000001',
                                                  '-73.99037',
                                                  'Entire home/apt',
                                                  '150',
                                                  '1',
                                                  '160',
                                                  '2019-06-09',
                                                  '1.33',
                                                  '4',
                                                  '188']]),
                 "2-3": (TEXT_FORMAT_ORDERED_LIST, [['36482809',
                                                  'Stunning Bedroom NYC! Walking to Central Park!!',
                                                  '131529729',
                                                  'Kendall',
                                                  'Manhattan',
                                                  'East Harlem',
                                                  '40.79633',
                                                  '-73.93605',
                                                  'Private room',
                                                  '75',
                                                  '2',
                                                  '0',
                                                  '',
                                                  '',
                                                  '2',
                                                  '353'],
                                                 ['36483010',
                                                  'Comfy 1 Bedroom in Midtown East',
                                                  '274311461',
                                                  'Scott',
                                                  'Manhattan',
                                                  'Midtown',
                                                  '40.75561',
                                                  '-73.96723',
                                                  'Entire home/apt',
                                                  '200',
                                                  '6',
                                                  '0',
                                                  '',
                                                  '',
                                                  '1',
                                                  '176'],
                                                 ['36483152',
                                                  'Garden Jewel Apartment in Williamsburg New York',
                                                  '208514239',
                                                  'Melki',
                                                  'Brooklyn',
                                                  'Williamsburg',
                                                  '40.71232',
                                                  '-73.9422',
                                                  'Entire home/apt',
                                                  '170',
                                                  '1',
                                                  '0',
                                                  '',
                                                  '',
                                                  '3',
                                                  '365'],
                                                 ['36484087',
                                                  'Spacious Room w/ Private Rooftop, Central location',
                                                  '274321313',
                                                  'Kat',
                                                  'Manhattan',
                                                  "Hell's Kitchen",
                                                  '40.76392',
                                                  '-73.99183000000002',
                                                  'Private room',
                                                  '125',
                                                  '4',
                                                  '0',
                                                  '',
                                                  '',
                                                  '1',
                                                  '31'],
                                                 ['36484363',
                                                  'QUIT PRIVATE HOUSE',
                                                  '107716952',
                                                  'Michael',
                                                  'Queens',
                                                  'Jamaica',
                                                  '40.69137',
                                                  '-73.80844',
                                                  'Private room',
                                                  '65',
                                                  '1',
                                                  '0',
                                                  '',
                                                  '',
                                                  '2',
                                                  '163'],
                                                 ['36484665',
                                                  'Charming one bedroom - newly renovated rowhouse',
                                                  '8232441',
                                                  'Sabrina',
                                                  'Brooklyn',
                                                  'Bedford-Stuyvesant',
                                                  '40.67853',
                                                  '-73.94995',
                                                  'Private room',
                                                  '70',
                                                  '2',
                                                  '0',
                                                  '',
                                                  '',
                                                  '2',
                                                  '9'],
                                                 ['36485057',
                                                  'Affordable room in Bushwick/East Williamsburg',
                                                  '6570630',
                                                  'Marisol',
                                                  'Brooklyn',
                                                  'Bushwick',
                                                  '40.70184',
                                                  '-73.93316999999998',
                                                  'Private room',
                                                  '40',
                                                  '4',
                                                  '0',
                                                  '',
                                                  '',
                                                  '2',
                                                  '36'],
                                                 ['36485431',
                                                  'Sunny Studio at Historical Neighborhood',
                                                  '23492952',
                                                  'Ilgar & Aysel',
                                                  'Manhattan',
                                                  'Harlem',
                                                  '40.81475',
                                                  '-73.94866999999998',
                                                  'Entire home/apt',
                                                  '115',
                                                  '10',
                                                  '0',
                                                  '',
                                                  '',
                                                  '1',
                                                  '27'],
                                                 ['36485609',
                                                  '43rd St. Time Square-cozy single bed',
                                                  '30985759',
                                                  'Taz',
                                                  'Manhattan',
                                                  "Hell's Kitchen",
                                                  '40.75751',
                                                  '-73.99112',
                                                  'Shared room',
                                                  '55',
                                                  '1',
                                                  '0',
                                                  '',
                                                  '',
                                                  '6',
                                                  '2'],
                                                 ['36487245',
                                                  "Trendy duplex in the very heart of Hell's Kitchen",
                                                  '68119814',
                                                  'Christophe',
                                                  'Manhattan',
                                                  "Hell's Kitchen",
                                                  '40.76404',
                                                  '-73.98933000000002',
                                                  'Private room',
                                                  '90',
                                                  '7',
                                                  '0',
                                                  '',
                                                  '',
                                                  '1',
                                                  '23']]),
                 "3": (TEXT_FORMAT_ORDERED_LIST, ['2539',
                                                  'Clean & quiet apt home by the park',
                                                  '2787',
                                                  'John',
                                                  'Brooklyn',
                                                  'Kensington',
                                                  '40.64749000000001',
                                                  '-73.97237',
                                                  'Private room',
                                                  '149',
                                                  '1',
                                                  '9',
                                                  '2018-10-19',
                                                  '0.21',
                                                  '6',
                                                  '365']),
                 "4": (TEXT_FORMAT, "John"),
                 "5": (TEXT_FORMAT, 4),
                 "6": (TEXT_FORMAT, "Brooklyn"),
                 "7-1": (TEXT_FORMAT, "Kensington"),
                 "7-2": (TEXT_FORMAT, "Skylit Midtown Castle"),
                 "7-3": (TEXT_FORMAT, "150"),
                 "8": (TEXT_FORMAT, 1091),
                 "9": (TEXT_FORMAT_ORDERED_LIST, ['Vanessa',
                                                     'Rossy,  Carmen And Juan',
                                                     'Rossy,  Carmen And Juan',
                                                     'Rossy,  Carmen And Juan',
                                                     'Maris',
                                                     'Brais',
                                                     'Justine',
                                                     'Rossy,  Carmen And Juan',
                                                     'Monica A',
                                                     'Justine',
                                                     'Justine',
                                                     'Pedro',
                                                     'Justine',
                                                     'Mary',
                                                     'Elizabeth',
                                                     'Christophe',
                                                     'Pierpaolo',
                                                     'Oscar',
                                                     'Henry',
                                                     'Mel',
                                                     'Justine']),
                 "10-1": (TEXT_FORMAT_ORDERED_LIST, ['Kensington', 'Midtown', 'Harlem']),
                 "10-2": (TEXT_FORMAT_ORDERED_LIST, ['Harlem', 'Kensington', 'Midtown']),
                 "11-1": (TEXT_FORMAT_ORDERED_LIST, ['Kensington', 'Midtown', 'Harlem']),
                 "11-2": (TEXT_FORMAT_ORDERED_LIST, ['Harlem', 'Kensington', 'Midtown']),
                 "12-1": (TEXT_FORMAT, 3),
                 "12-2": (TEXT_FORMAT, 3.5),
                 "13": (TEXT_FORMAT, 89.0),
                 "14": (TEXT_FORMAT, 80),
                 "15": (TEXT_FORMAT, 7),
                 "16": (TEXT_FORMAT_UNORDERED_LIST, {'Harlem', 'Kensington', 'Midtown'}),
                 "17": (TEXT_FORMAT, True),
                 "18": (TEXT_FORMAT_ORDERED_LIST, ['Frank And Anna',
                                                     'Dave And Shaceline',
                                                     'Chondra',
                                                     'Luis',
                                                     'Edwin',
                                                     'Edwin',
                                                     'Edwin',
                                                     'Edwin',
                                                     'George',
                                                     'Ally',
                                                     'Catherine',
                                                     'Catherine',
                                                     'Denise',
                                                     'Annette',
                                                     'Stephanie',
                                                     'Catherine',
                                                     'Yolanda',
                                                     'Joe',
                                                     'Amaree',
                                                     'Catherine',
                                                     'Catherine',
                                                     'Alfonso',
                                                     'Cecilia',
                                                     'Carsandra']),
                 "19": (TEXT_FORMAT_UNORDERED_LIST, {'Alfonso',
                                                         'Ally',
                                                         'Amaree',
                                                         'Annette',
                                                         'Carsandra',
                                                         'Catherine',
                                                         'Cecilia',
                                                         'Chondra',
                                                         'Dave And Shaceline',
                                                         'Denise',
                                                         'Edwin',
                                                         'Frank And Anna',
                                                         'George',
                                                         'Joe',
                                                         'Luis',
                                                         'Stephanie',
                                                         'Yolanda'}),
                 "20": (TEXT_FORMAT_UNORDERED_LIST, ['Manhattan', 'Midtown', 'Kensington', 'Brooklyn'])}

def check_cell(qnum, actual):
    format, expected = expected_json[qnum[1:]]
    try:
        if format == TEXT_FORMAT:
            return simple_compare(expected, actual)
        elif format == TEXT_FORMAT_UNORDERED_LIST:
            return list_compare_unordered(expected, actual)
        elif format == TEXT_FORMAT_ORDERED_LIST:
            return list_compare_ordered(expected, actual)
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

def namedtuple_compare(expected, actual):
    msg = PASS
    for field in expected._fields:
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
        msg = msg + " (found %d entries in %s, but expected %d)" % (len(actual), obj, len(expected))

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
            if val != PASS:
                msg = "incorrect val for key %s in %s: " % (repr(key), obj) + val
    return msg


def check(qnum, actual):
    msg = check_cell(qnum, actual)
    if msg == PASS:
        return True
    print("<b style='color: red;'>ERROR:</b> " + msg)
