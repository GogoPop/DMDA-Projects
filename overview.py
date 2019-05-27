#!/usr/bin/python
# -*- coding: utf-8 -*-

#gets various counts from osm file

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re


OSMFILE = 'map.osm'
SAMPLE_FILE = 'sample.osm'
filelist = [OSMFILE]

#regular expressions
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#get first word before '.'
street_type_re = re.compile(r'^\S+\.?',  re.IGNORECASE)
street_types = defaultdict(int)  #create dictionary with default int

# Count key and value
def key_counts(filename):
    key_cnt = defaultdict(int)
    for event, elem in ET.iterparse(filename):
        if elem.tag == "tag":
            key_cnt[elem.attrib['k']] += 1
    return key_cnt


# Count all tags in the dataset
def tag_counts(filename):
    tag_cnt = defaultdict(int)
    for event, elem in ET.iterparse(filename):
        tag_cnt[elem.tag] += 1
    return tag_cnt


# Count all ways in the dataset
def way_count(filename):
    way_cnt = 0
    for _, element in ET.iterparse(filename):
        if element.tag == "way":
            way_cnt += 1
    return way_cnt


#count of key types
def key_type(element, keys):
    if element.tag == "tag":
        if lower.search(element.attrib['k']):
            keys['lower'] += 1
        elif lower_colon.search(element.attrib['k']):
            keys['lower_colon'] += 1
        elif problemchars.search(element.attrib['k']):
            keys['problemchars'] += 1
            print ("problemchars: " + element.attrib['k'] )
        else:
            keys['other'] += 1
    return keys


def key_style_counts(filename):
    key_chars = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, key_chars)
    return key_chars


# users who contributed to the map's data
def top_contributors(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if 'user' in element.attrib:
            users.update([element.attrib['user']])
    return (sorted(users)[-5:])


def get_user(element):
    if element.get('uid'):
        uid = element.attrib["uid"]
        return uid
    else:
        return None


# count unique users who contributed to the map's data
def user_count(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        if get_user(element):
            users.add(get_user(element))
    return len(users)


def is_amenity(elem):
    return elem.attrib['k'] == "amenity"


# get count of amenities
def amenity_type_count(amenity_type, amenity):
    amenity_type[amenity] += 1


def amenity_counts(filename):
    amenity_type = defaultdict(int)
    for event, elem in ET.iterparse(filename, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_amenity(tag):
                    amenity_type_count(amenity_type, tag.attrib['v'])
    return amenity_type


#count street names
def street_count(filename):
    st_count = 0
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == 'node' or elem.tag == 'way':
            for tag in elem.iter('tag'):
                if tag.attrib['k'] == "addr:street":
                    st_count += 1
    return st_count


#count street types
def street_type_count(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        street_types[street_type] += 1


#sort dictionary by street names
def print_sorted_dict(d):
    keys = d.keys()
    keys = sorted(keys, key=lambda s: s.lower())
    for k in keys:
        v = d[k]
        print("%s: %d" % (k, v))


def street_counts(filename):
    for event, elem in ET.iterparse(filename):
        if (elem.tag == "tag") and (elem.attrib['k'] == "addr:street"):
            street_type_count(street_types, elem.attrib['v'])
    print_sorted_dict(street_types)


# users who contributed to the map's data
def city_list(filename):
    cities = set()
    for event, elem in ET.iterparse(filename):
        if (elem.tag == "tag") and (elem.attrib['k'] == "addr:city"):
            cities.add(elem.attrib['v'])
    return sorted(cities)


# key elements
def key_list(filename):
    keyset = defaultdict(set)
    for event, elem in ET.iterparse(filename):
        if elem.tag == "tag":
            keyset[elem.attrib['k']] = elem.attrib['v']
    return sorted(keyset)


if __name__ == '__main__':
    for file in filelist:
        print('\n_________________________________')
        print("Counts for osm file:" ,file )
        print('_________________________________')
        print("Contributors:", user_count(file))

        print("\nTop Contributors")
        print(top_contributors(file))

        print("\nTag Counts ")
        all_tags = tag_counts(file)
        pprint.pprint(tag_counts(file))

        print("\nKey Counts ")
        pprint.pprint(key_counts(file))

        print("\nKey Style Counts")
        keys = key_style_counts(file)
        pprint.pprint(key_style_counts(file))

        print("\nAmenity Counts")
        stuff = amenity_counts(file)
        pprint.pprint(amenity_counts(file))

        print("\nWay Count:", way_count(file))

        print("\nStreet Count: ", street_count(file))

        print("\nStreet Type Counts")
        print(street_counts(file))

        print("\nCities")
        print(city_list(file))

