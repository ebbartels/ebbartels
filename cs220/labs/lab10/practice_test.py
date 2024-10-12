#!/usr/bin/python
import os, json, math
from collections import namedtuple

MAX_FILE_SIZE = 300 # units - KB
REL_TOL = 6e-04  # relative tolerance for floats
ABS_TOL = 15e-03  # absolute tolerance for floats

PASS = "PASS"

TEXT_FORMAT = "text"  # question type when expected answer is a str, int, float, or bool
TEXT_FORMAT_NAMEDTUPLE = "text namedtuple"  # question type when expected answer is a namedtuple
TEXT_FORMAT_UNORDERED_LIST = "text list_unordered"  # question type when the expected answer is a list where the order does *not* matter
TEXT_FORMAT_ORDERED_LIST = "text list_ordered"  # question type when the expected answer is a list where the order does matter
TEXT_FORMAT_SPECIAL_ORDERED_LIST = "text list_special_ordered"  # question type when the expected answer is a list where order does matter, but with possible ties. Elements are ordered according to values in special_ordered_json (with ties allowed)
TEXT_FORMAT_DICT = "text dict"  # question type when the expected answer is a dictionary

def return_expected_json():
    expected_json =    {"1-1": (TEXT_FORMAT_UNORDERED_LIST, ['.DS_Store',
                                                             '.ipynb_checkpoints',
                                                             'mapping_1.json',
                                                             'mapping_2.json',
                                                             'mapping_3.json',
                                                             'planets_1.csv',
                                                             'planets_2.csv',
                                                             'planets_3.csv',
                                                             'stars_1.csv',
                                                             'stars_2.csv',
                                                             'stars_3.csv']),
                        "1-2": (TEXT_FORMAT_UNORDERED_LIST, ['mapping_1.json',
                                                             'mapping_2.json',
                                                             'mapping_3.json',
                                                             'planets_1.csv',
                                                             'planets_2.csv',
                                                             'planets_3.csv',
                                                             'stars_1.csv',
                                                             'stars_2.csv',
                                                             'stars_3.csv']),
                        "2": (TEXT_FORMAT_ORDERED_LIST, ['mapping_1.json',
                                                             'mapping_2.json',
                                                             'mapping_3.json',
                                                             'planets_1.csv',
                                                             'planets_2.csv',
                                                             'planets_3.csv',
                                                             'stars_1.csv',
                                                             'stars_2.csv',
                                                             'stars_3.csv']),
                        "3-1": (TEXT_FORMAT, os.path.join("small_data", "stars_1.csv")),
                        "3-2": (TEXT_FORMAT_ORDERED_LIST, [os.path.join("small_data", "mapping_1.json"),
                                                            os.path.join("small_data", "mapping_2.json"),
                                                            os.path.join("small_data", "mapping_3.json"),
                                                            os.path.join("small_data", "planets_1.csv"),
                                                            os.path.join("small_data", "planets_2.csv"),
                                                            os.path.join("small_data", "planets_3.csv"),
                                                            os.path.join("small_data", "stars_1.csv"),
                                                            os.path.join("small_data", "stars_2.csv"),
                                                            os.path.join("small_data", "stars_3.csv")]),
                        "4-1": (TEXT_FORMAT_ORDERED_LIST, [os.path.join("small_data", "mapping_1.json"),
                                                            os.path.join("small_data", "mapping_2.json"),
                                                            os.path.join("small_data", "mapping_3.json")]),
                        "4-2": (TEXT_FORMAT_ORDERED_LIST, [os.path.join("small_data", "stars_1.csv"),
                                                            os.path.join("small_data", "stars_2.csv"),
                                                            os.path.join("small_data", "stars_3.csv")]),
                        "star_object": (TEXT_FORMAT_NAMEDTUPLE, Star(spectral_type='G2 V', stellar_effective_temperature=5780.0,
                                                                    stellar_radius=1.0, stellar_mass=1.0, stellar_luminosity=0.0,
                                                                    stellar_surface_gravity=4.44, stellar_age=4.6)),
                        "5": (TEXT_FORMAT_NAMEDTUPLE, Star(spectral_type='G8V', stellar_effective_temperature=5172.0,
                                                            stellar_radius=0.94, stellar_mass=0.91, stellar_luminosity=-0.197,
                                                            stellar_surface_gravity=4.43, stellar_age=10.2)),
                        "6": (TEXT_FORMAT_NAMEDTUPLE, Star(spectral_type='F8 V', stellar_effective_temperature=6196.0,
                                                            stellar_radius=1.26, stellar_mass=1.21, stellar_luminosity=0.32,
                                                            stellar_surface_gravity=4.41, stellar_age=2.01)),
                        "7-1": (TEXT_FORMAT, "F8 V"),
                        "7-2": (TEXT_FORMAT, 10.2),
                        "7": (TEXT_FORMAT, 0.016741496598639403),
                        "8": (TEXT_FORMAT_DICT, {'55 Cnc': Star(spectral_type='G8V', stellar_effective_temperature=5172.0,
                                                                stellar_radius=0.94, stellar_mass=0.91, stellar_luminosity=-0.197,
                                                                stellar_surface_gravity=4.43, stellar_age=10.2),
                                                 'DMPP-1': Star(spectral_type='F8 V', stellar_effective_temperature=6196.0,
                                                                stellar_radius=1.26, stellar_mass=1.21, stellar_luminosity=0.32,
                                                                stellar_surface_gravity=4.41, stellar_age=2.01),
                                                 'GJ 876': Star(spectral_type='M2.5V', stellar_effective_temperature=3271.0,
                                                                stellar_radius=0.3, stellar_mass=0.32, stellar_luminosity=-1.907,
                                                                stellar_surface_gravity=4.87, stellar_age=1.0)}),
                        "9-1": (TEXT_FORMAT_NAMEDTUPLE, Star(spectral_type='M2.5V', stellar_effective_temperature=3271.0,
                                                            stellar_radius=0.3, stellar_mass=0.32, stellar_luminosity=-1.907,
                                                            stellar_surface_gravity=4.87, stellar_age=1.0)),
                        "9-2": (TEXT_FORMAT, -1.907),
                        "10-1": (TEXT_FORMAT, 'G0'),
                        "10-2": (TEXT_FORMAT, None),
                        "10-3": (TEXT_FORMAT, 1.04),
                        "11": (TEXT_FORMAT_DICT, {'HD 158259': Star(spectral_type='G0', stellar_effective_temperature=5801.89,
                                                                    stellar_radius=1.21, stellar_mass=1.08, stellar_luminosity=0.212,
                                                                    stellar_surface_gravity=4.25, stellar_age=None),
                                                 'K2-187': Star(spectral_type=None, stellar_effective_temperature=5438.0,
                                                                stellar_radius=0.83, stellar_mass=0.97, stellar_luminosity=-0.21,
                                                                stellar_surface_gravity=4.6, stellar_age=None),
                                                 'WASP-47': Star(spectral_type=None, stellar_effective_temperature=5552.0,
                                                                stellar_radius=1.14, stellar_mass=1.04, stellar_luminosity=0.032,
                                                                stellar_surface_gravity=4.34, stellar_age=6.5)}),
                        "12-1": (TEXT_FORMAT_DICT, {'K2-133': Star(spectral_type='M1.5 V', stellar_effective_temperature=3655.0,
                                                                    stellar_radius=0.46, stellar_mass=0.46, stellar_luminosity=-1.479,
                                                                    stellar_surface_gravity=4.77, stellar_age=None),
                                                    'K2-138': Star(spectral_type='G8 V', stellar_effective_temperature=5356.3,
                                                                    stellar_radius=0.86, stellar_mass=0.94, stellar_luminosity=-0.287,
                                                                    stellar_surface_gravity=4.54, stellar_age=2.8),
                                                    'GJ 667 C': Star(spectral_type='M1.5 V', stellar_effective_temperature=3350.0,
                                                                    stellar_radius=None, stellar_mass=0.33, stellar_luminosity=-1.863,
                                                                    stellar_surface_gravity=4.69, stellar_age=2.0)}),
                        "12-2": (TEXT_FORMAT_DICT, {'55 Cnc': Star(spectral_type='G8V', stellar_effective_temperature=5172.0,
                                                                    stellar_radius=0.94, stellar_mass=0.91, stellar_luminosity=-0.197,
                                                                    stellar_surface_gravity=4.43, stellar_age=10.2),
                                                    'DMPP-1': Star(spectral_type='F8 V', stellar_effective_temperature=6196.0,
                                                                    stellar_radius=1.26, stellar_mass=1.21, stellar_luminosity=0.32,
                                                                    stellar_surface_gravity=4.41, stellar_age=2.01),
                                                    'GJ 876': Star(spectral_type='M2.5V', stellar_effective_temperature=3271.0,
                                                                    stellar_radius=0.3, stellar_mass=0.32, stellar_luminosity=-1.907,
                                                                    stellar_surface_gravity=4.87, stellar_age=1.0),
                                                    'HD 158259': Star(spectral_type='G0', stellar_effective_temperature=5801.89,
                                                                    stellar_radius=1.21, stellar_mass=1.08, stellar_luminosity=0.212,
                                                                    stellar_surface_gravity=4.25, stellar_age=None),
                                                    'K2-187': Star(spectral_type=None, stellar_effective_temperature=5438.0,
                                                                    stellar_radius=0.83, stellar_mass=0.97, stellar_luminosity=-0.21,
                                                                    stellar_surface_gravity=4.6, stellar_age=None),
                                                    'WASP-47': Star(spectral_type=None, stellar_effective_temperature=5552.0,
                                                                    stellar_radius=1.14, stellar_mass=1.04, stellar_luminosity=0.032,
                                                                    stellar_surface_gravity=4.34, stellar_age=6.5),
                                                    'K2-133': Star(spectral_type='M1.5 V', stellar_effective_temperature=3655.0,
                                                                    stellar_radius=0.46, stellar_mass=0.46, stellar_luminosity=-1.479,
                                                                    stellar_surface_gravity=4.77, stellar_age=None),
                                                    'K2-138': Star(spectral_type='G8 V', stellar_effective_temperature=5356.3,
                                                                    stellar_radius=0.86, stellar_mass=0.94, stellar_luminosity=-0.287,
                                                                    stellar_surface_gravity=4.54, stellar_age=2.8),
                                                    'GJ 667 C': Star(spectral_type='M1.5 V', stellar_effective_temperature=3350.0,
                                                                    stellar_radius=None, stellar_mass=0.33, stellar_luminosity=-1.863,
                                                                    stellar_surface_gravity=4.69, stellar_age=2.0)}),
                        "planet_object": (TEXT_FORMAT_NAMEDTUPLE, Planet(planet_name='Jupiter', host_name='Sun', discovery_method='Imaging',
                                                                    discovery_year=1610, controversial_flag=False, orbital_period=4333.0,
                                                                    planet_radius=11.209, planet_mass=317.828, semi_major_radius=5.2038,
                                                                    eccentricity=0.0489, equilibrium_temperature=110, insolation_flux=0.0345)),
                        "13-1": (TEXT_FORMAT_ORDERED_LIST, [['55 Cnc b',
                                                              'Radial Velocity',
                                                              '1996',
                                                              '0',
                                                              '14.65160000',
                                                              '13.900',
                                                              '263.97850',
                                                              '0.113400',
                                                              '0.000000',
                                                              '700',
                                                              ''],
                                                             ['55 Cnc c',
                                                              'Radial Velocity',
                                                              '2004',
                                                              '0',
                                                              '44.39890000',
                                                              '8.510',
                                                              '54.47380',
                                                              '0.237300',
                                                              '0.030000',
                                                              '',
                                                              ''],
                                                             ['DMPP-1 b',
                                                              'Radial Velocity',
                                                              '2019',
                                                              '0',
                                                              '18.57000000',
                                                              '5.290',
                                                              '24.27000',
                                                              '0.146200',
                                                              '0.083000',
                                                              '877',
                                                              ''],
                                                             ['GJ 876 b',
                                                              'Radial Velocity',
                                                              '1998',
                                                              '0',
                                                              '61.11660000',
                                                              '13.300',
                                                              '723.22350',
                                                              '0.208317',
                                                              '0.032400',
                                                              '',
                                                              ''],
                                                             ['GJ 876 c',
                                                              'Radial Velocity',
                                                              '2000',
                                                              '0',
                                                              '30.08810000',
                                                              '14.000',
                                                              '226.98460',
                                                              '0.129590',
                                                              '0.255910',
                                                              '',
                                                              '']]),
                        "13-2": (TEXT_FORMAT_DICT, {'55 Cnc b': '55 Cnc',
                                                     '55 Cnc c': '55 Cnc',
                                                     'DMPP-1 b': 'DMPP-1',
                                                     'GJ 876 b': 'GJ 876',
                                                     'GJ 876 c': 'GJ 876'}),
                        "14-1": (TEXT_FORMAT, '55 Cnc b'),
                        "14-2": (TEXT_FORMAT, None),
                        "14-3": (TEXT_FORMAT, False),
                        "15": (TEXT_FORMAT_NAMEDTUPLE, Planet(planet_name='55 Cnc b', host_name='55 Cnc', discovery_method='Radial Velocity',
                                                                discovery_year=1996, controversial_flag=False, orbital_period=14.6516,
                                                                planet_radius=13.9, planet_mass=263.9785, semi_major_radius=0.1134,
                                                                eccentricity=0.0, equilibrium_temperature=700.0, insolation_flux=None)),
                        "16": (TEXT_FORMAT_ORDERED_LIST, [Planet(planet_name='55 Cnc b', host_name='55 Cnc', discovery_method='Radial Velocity',
                                                                discovery_year=1996, controversial_flag=False, orbital_period=14.6516,
                                                                planet_radius=13.9, planet_mass=263.9785, semi_major_radius=0.1134,
                                                                eccentricity=0.0, equilibrium_temperature=700.0, insolation_flux=None),
                                                          Planet(planet_name='55 Cnc c', host_name='55 Cnc', discovery_method='Radial Velocity',
                                                                discovery_year=2004, controversial_flag=False, orbital_period=44.3989,
                                                                planet_radius=8.51, planet_mass=54.4738, semi_major_radius=0.2373,
                                                                eccentricity=0.03, equilibrium_temperature=None, insolation_flux=None),
                                                          Planet(planet_name='DMPP-1 b', host_name='DMPP-1', discovery_method='Radial Velocity',
                                                                discovery_year=2019, controversial_flag=False, orbital_period=18.57,
                                                                planet_radius=5.29, planet_mass=24.27, semi_major_radius=0.1462,
                                                                eccentricity=0.083, equilibrium_temperature=877.0, insolation_flux=None),
                                                          Planet(planet_name='GJ 876 b', host_name='GJ 876', discovery_method='Radial Velocity',
                                                                discovery_year=1998, controversial_flag=False, orbital_period=61.1166,
                                                                planet_radius=13.3, planet_mass=723.2235, semi_major_radius=0.208317,
                                                                eccentricity=0.0324, equilibrium_temperature=None, insolation_flux=None),
                                                          Planet(planet_name='GJ 876 c', host_name='GJ 876', discovery_method='Radial Velocity',
                                                                discovery_year=2000, controversial_flag=False, orbital_period=30.0881,
                                                                planet_radius=14.0, planet_mass=226.9846, semi_major_radius=0.12959,
                                                                eccentricity=0.25591, equilibrium_temperature=None, insolation_flux=None)]),
                        "17-1": (TEXT_FORMAT_NAMEDTUPLE, Planet(planet_name='GJ 876 c', host_name='GJ 876', discovery_method='Radial Velocity',
                                                                discovery_year=2000, controversial_flag=False, orbital_period=30.0881,
                                                                planet_radius=14.0, planet_mass=226.9846, semi_major_radius=0.12959,
                                                                eccentricity=0.25591, equilibrium_temperature=None, insolation_flux=None)),
                        "17-2": (TEXT_FORMAT, 'GJ 876 c'),
                        "18": (TEXT_FORMAT_ORDERED_LIST, [Planet(planet_name='HD 158259 b', host_name='HD 158259',
                                                                discovery_method='Radial Velocity', discovery_year=2020,
                                                                controversial_flag=False, orbital_period=2.178, planet_radius=1.292,
                                                                planet_mass=2.22, semi_major_radius=None, eccentricity=None,
                                                                equilibrium_temperature=1478.0, insolation_flux=794.22),
                                                          Planet(planet_name='K2-187 b', host_name='K2-187', discovery_method='Transit',
                                                                discovery_year=2018, controversial_flag=False, orbital_period=0.77401,
                                                                planet_radius=1.2, planet_mass=1.87, semi_major_radius=0.0164,
                                                                eccentricity=None, equilibrium_temperature=1815.0, insolation_flux=None),
                                                          Planet(planet_name='K2-187 c', host_name='K2-187', discovery_method='Transit',
                                                              discovery_year=2018, controversial_flag=False, orbital_period=2.871512,
                                                              planet_radius=1.4, planet_mass=2.54, semi_major_radius=0.0392,
                                                              eccentricity=None, equilibrium_temperature=1173.0, insolation_flux=None)]),
                        "19": (TEXT_FORMAT_DICT, {'55 Cnc b': '55 Cnc',
                                                     '55 Cnc c': '55 Cnc',
                                                     'DMPP-1 b': 'DMPP-1',
                                                     'GJ 876 b': 'GJ 876',
                                                     'GJ 876 c': 'GJ 876',
                                                     'HD 158259 b': 'HD 158259',
                                                     'K2-187 b': 'K2-187',
                                                     'K2-187 c': 'K2-187',
                                                     'K2-187 d': 'K2-187',
                                                     'WASP-47 b': 'WASP-47'}),
                        "20-1": (TEXT_FORMAT, 'K2-187'),
                        "20-2": (TEXT_FORMAT_NAMEDTUPLE, Star(spectral_type=None, stellar_effective_temperature=5438.0,
                                                                stellar_radius=0.83, stellar_mass=0.97, stellar_luminosity=-0.21,
                                                                stellar_surface_gravity=4.6, stellar_age=None)),
                        "20-3": (TEXT_FORMAT, 0.94)}
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
            return namedtuple_compare(expected ,actual)
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
        elif type(expected[i]) in [list]:
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
            elif type(expected[key]).__name__ in namedtuples:
                val = namedtuple_compare(expected[key], actual[key])
            if val != PASS:
                msg = "incorrect val for key %s in %s: " % (repr(key), obj) + val
    return msg

def check(qnum, actual):
    msg = check_cell(qnum, actual)
    if msg == PASS:
        return True
    print("<b style='color: red;'>ERROR:</b> " + msg)


def check_file_size(path):
    size = os.path.getsize(path)
    assert size < MAX_FILE_SIZE * 10**3, "Your file is too big to be processed by Gradescope; please delete unnecessary output cells so your file size is < %s KB" % MAX_FILE_SIZE
