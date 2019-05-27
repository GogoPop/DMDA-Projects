# this script has functions that parse an osm xml file,
# performs audits and returns updated values

import re
import pprint

#matches last word in street type (st, rd...)
street_type_re = re.compile(r'(\b\S+\.?)$', re.IGNORECASE)

#matches 2nd to last word  in street type
street_type_re2 = re.compile(r'(\b\S+\.?) \S+$', re.IGNORECASE)

#matches direction at end of street type name
#directional_re = re.compile(r'((\s[NESW][EW]?)|(\Dth|\Sst))$', re.IGNORECASE)
directional_re = re.compile(r'\s(North|East|South|West)$', re.IGNORECASE)

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


#update the street type, 1st the direction then the type
def update_street_name(name):
    #check last position for direction
    d = street_type_re.search(name)
    if d:
        #check for direction
        street_end = None
        street_end = directional_mapping.get(d.group(), "")
        #is a direction
        if street_end :
            p = re.compile(d.group())
            name = p.sub(street_end, name)

        #if this had a direction check 2nd to last word for street type
        m = street_type_re2.search(name)
        if m:
            #check for street type
            street_end = None
            street_end = street_name_mapping.get(m.group(1).lower(), "")
            #is a street type
            if street_end:
                p = re.compile(m.group(1))
                name = p.sub(street_end, name)
    #check the last word for street type
    m = street_type_re.search(name)
    if m:
        #check for street type
        street_end = None
        street_end = street_name_mapping.get(m.group(1).lower(), "")
        #mapping found
        if street_end:
            p = re.compile(m.group(1))
            name = p.sub(street_end, name)
    #return updated string
    return name


def update_postcode(postcode):
    if len(postcode) > 5:
        postcode = postcode[:-5]
    return postcode


def update_house_number(house_number):
    #check if number contains a house_number.
    if not house_number.isdigit():
        house_number = house_number.upper()
    return house_number

def update_city(city):
    if city.lower() == 'palm habror':
        city = 'Palm Harbor'
    return city
