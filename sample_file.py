#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Taken from the project details page and modified for python 3.7
#create a sample file for initial auditing and validation purposes.
#take a systematic sample of elements from the original OSM region.
#changing the value of k resulting in SAMPLE_FILEs of different sizes.
#
import xml.etree.ElementTree as ET

OSM_FILE = 'map.osm'
SAMPLE_FILE = "sample.osm"

k = 20  # Parameter: take every k-th top level element


def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag
    Reference:
    http://stackoverflow.com/questions/3095434/
    inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'w') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % k == 0:
            output.write(ET.tostring(element, encoding="unicode"))

    output.write('\n</osm>')
    print("Done. File ",SAMPLE_FILE ,"  has been created.")
