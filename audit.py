#this script parses an osm xml file, performs audits and prints values
#for visual inspection to help determine problems in the data
#for all the scripts the safety_harbor.osm was copied to map.osm
#this is an attempt to have generic scripts I can apply to any map.osm

import xml.etree.ElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "map.osm"
DEBUG   = False   #street name processing
DEBUG1  = True   #street change results

#matches last word in street type (st, rd...)
street_type_re = re.compile(r'(\b\S+\.?)$', re.IGNORECASE)

#matches 2nd to last word  in street type
street_type_re2 = re.compile(r'(\b\S+\.?) \S+$', re.IGNORECASE)

#matches direction at end of street type name
#directional_re = re.compile(r'((\s[NESW][EW]?)|(\Dth|\Sst))$', re.IGNORECASE)
directional_re = re.compile(r'\s(North|East|South|West)$', re.IGNORECASE)

unexp_street_types = defaultdict(set)
unexp_house_numbers = []
unexp_postcodes = []
cities = set()

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons", "Way",
            "Terrace", "Highway", "Alley", "Crescent", "Circle"]


street_name_mapping = {"av": "Avenue", "av.": "Avenue", "ave": "Avenue",
                       "ave.": "Avenue", "blvd": "Boulevard",
                       "blvd.": "Boulevard", "cir": "Circle",
                       "ct": "Court", "ct.": "Court",
                       "dr": "Drive","dr.": "Drive",
                       "hwy": "Highway", "hwy.": "Highway",
                       "ln": "Lane", "pkwy": "Parkway", "pl": "Place",
                       "rd": "Road", "rd.": "Road",
                       "st": "Street", "st.": "Street",
                       "ter": "Terrace",
                       "wy": "Way"
                       }


directional_mapping = {"N.": "N", "North": "N", "S.": "S", "South": "S",
                       "E.": "E", "East": "E", "W.": "West", "West": "W",
                       "NE.": "NE", "Northeast": "NE", "NW.": "NW",
                       "Northwest": "NW", "SE.": "SE", "Southeast": "SE",
                       "SW.": "SW", "Southwest": "SW"
                      }


def is_street_name(elem):
    #true if tag describes a street
    return elem.attrib['k'] == "addr:street"


def is_house_number(elem):
    #true if tag describes a house_number
    return elem.attrib['k'] == "addr:house_number"


def is_postcode(elem):
    #true if tag describes a postcode
    return elem.attrib['k'] == "addr:postcode"


def is_city(elem):
    #true if tag describes a postcode
    return elem.attrib['k'] == "addr:city"


#check for unexpected street types, add them to a dict
def audit_street_type(unexp_street_types, street_name):
    initial_street = street_name
    last_word = street_name[-1]
    d = directional_re.search(street_name)
    if d:
        m = street_type_re2.search(street_name)
    else:
        m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            if DEBUG:
                print(" -----------")
                print("unexp: ", street_name, "  type:", street_type)
            unexp_street_types[street_type].add(street_name)

    street_name = update_street_name(street_name)
    if DEBUG1:
        print("Initial Street  :", initial_street, " Final:", street_name)


def audit_house_number(unexp_house_number, house_number):
    #check if number contains a house_number.
    if not house_number.isdigit():
        house_number = house_number.upper()
        if house_number not in unexp_house_number:
            unexp_house_number.append(house_number)

    if DEBUG1:
        print("house#:", house_number)


#update the street type, 1st the direction then the type
def update_street_name(name):
    if DEBUG:
        print("Starting street --", name)
    #check last position for direction
    d = street_type_re.search(name)
    if d:
        if DEBUG:
            print("Direction: ", name, " Matching: ", d.group())
        #check for direction
        street_end = None
        street_end = directional_mapping.get(d.group(), "")
        if DEBUG:
            print("Key Value:", street_end)
        #is a direction
        if street_end :
            p = re.compile(d.group())
            name = p.sub(street_end, name)

        #if this had a direction check 2nd to last word for street type
        m = street_type_re2.search(name)
        if m:
            if DEBUG:
                print("Street: ", name, " Matching: ",m.group(1).lower())
            #check for street type
            street_end = None
            street_end = street_name_mapping.get(m.group(1).lower(), "")
            if DEBUG:
                print("Key Value:", street_end)
            #is a street type
            if street_end:
                p = re.compile(m.group(1))
                name = p.sub(street_end, name)

    #check the last word for street type
    m = street_type_re.search(name)
    if m:
        if DEBUG:
            print("Street: ", name, " Matching: ", m.group(1))
        #check for street type
        street_end = None
        street_end = street_name_mapping.get(m.group(1).lower(), "")
        if DEBUG:
            print("Key Value:", street_end)
        #mapping found
        if street_end:
            p = re.compile(m.group(1))
            name = p.sub(street_end, name)
    if DEBUG:
        print("End street -------", name)
    #return updated string
    return name


def update_postcode(unexp_postcode, postcode):
    postcode1 = postcode
    if not postcode.isdigit():
        unexp_postcode.append(postcode)
    if len(postcode) > 5:
        postcode = postcode[:-5]
    if DEBUG1:
        print("Initial postcode: ", postcode1, " Final postcode:", postcode)
    return postcode


def audit(osmfile):
    osm_file = open(osmfile, "r", encoding="utf-8")
    #parse file perform audits on specific tags
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):

                if is_street_name(tag):
                    audit_street_type(unexp_street_types, tag.attrib['v'])

                if is_house_number(tag):
                    #tag.set('v', audit_house_number(tag.attrib['v']))
                    audit_house_number(unexp_house_numbers, tag.attrib['v'])

                if is_postcode(tag):
                    post_code = update_postcode(unexp_postcodes,
                                                tag.attrib['v'])

                if is_city(tag):
                    cities.add(tag.attrib['v'])

    osm_file.close()


def print_dicts():
    print("\n --Cities --")
    print(cities)

    print("\n --unexp Street Types --")
    pprint.pprint(dict(unexp_street_types))

    print("\n --unexp House Numbers --")
    pprint.pprint(dict(unexp_house_numbers))

    print("\n --unexp Postcodes --")
    pprint.pprint(unexp_postcodes)


audit(OSMFILE)
print_dicts()
