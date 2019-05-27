#this script parses an osm xml file, performs audits and prints values
#of data that is expected to change during the xml to csv conversion
# problems in the data

import xml.etree.cElementTree as ET
import re


OSMFILE = "map.osm"
DEBUG   = True

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
    in_str = name
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
    #if in_str != name:
        #print("Returning: ", in_str, " --> ", name)
    #return updated string
    return name


def update_postcode(postcode):
    in_str = postcode
    if len(postcode) > 5:
        postcode = postcode[:-5]
    #if in_str != postcode:
        #print("Returning: ", in_str, " --> ", postcode)
    return postcode


def update_house_number(house_number):
    in_str = house_number
    #check if number contains a house_number.
    if not house_number.isdigit():
        house_number = house_number.upper()
    #if in_str != house_number:
        #print("Returning: ", in_str, " --> ", house_number)
    return house_number

def update_city(city):
    in_str = city
    #print("checking:", in_str)
    if city.lower() == 'palm habror':
        city = 'Palm Harbor'
    #if in_str != city:
        #print("Returning: ", in_str, " --> ", city)
    return city


def audit(osmfile):
    osm_file = open(osmfile, "r", encoding="utf-8")
    #parse file perform audits on specific tags
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):

                k = tag.attrib['k']
                v = tag.attrib['v']
                #set initial value
                in_val = v
                if k == 'addr:street':
                    v = update_street_name(v)
                    #set value returned and print if it is different
                    #then initial
                    out_val = v
                    if out_val != in_val:
                        print("street: ", v)

                elif k == 'addr:housenumber':
                    v = update_house_number(v)
                    #set value returned and print if it is different
                    #then initial
                    out_val = v
                    if out_val != in_val:
                        print(" elem:", elem.tag, " housenumber: ", v)

                elif k == 'addr:city':
                    v = update_city(v)
                    #set value returned and print if it is different
                    #then initial
                    out_val = v
                    if out_val != in_val:
                        print(" elem:", elem.tag, " city: ", v)

                elif k == 'addr:postcode':
                    v = update_postcode(v)
                    #set value returned and print if it is different
                    #then initial
                    out_val = v
                    if out_val != in_val:
                        print(" elem:", elem.tag, " postcode: ", v)

    osm_file.close()

audit(OSMFILE)
