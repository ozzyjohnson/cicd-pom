import xml.etree.ElementTree as ET
from ast import literal_eval
import sys

# Register the pom namespace to avoid 'ns0' ugliness when writing.
xsi = ET.register_namespace('', "http://maven.apache.org/POM/4.0.0")

a_in = sys.argv[1]
a_out = sys.argv[2]
a_contributor = sys.argv[3]

# Parse the contributor dictionary. Handles multiple contributors,
# one dict per line. Should this be JSON or YAML instead?
l_contributors = []
with open(a_contributor, 'r') as f_contributor: 
    for line in f_contributor:
        l_contributors.append(literal_eval(line))
    
# Parse the input xml.
try:
    tree = ET.parse(a_in)
except IOError as err:
    print "Invalid input file:", err

root = tree.getroot()

# Add new elements.
contributors = ET.SubElement(root, 'contributors')

# Populate the contributor recursing for the nested attributes.
# Only handles one level.
def f_add_elements(start, k, v):
    currentElement = ET.SubElement(start, k)
    if isinstance(v, dict):
        val = v.keys()[0]
        return f_add_elements(currentElement, val, v[val])
    else:
        currentElement.text = v

def f_parse_contributors(contribution):
    for k,v in contribution.items():
        f_add_elements(contributor, k, v)

for contribution in l_contributors:
    contributor = ET.SubElement(root.find('contributors'), 'contributor')
    f_parse_contributors(contribution)

# A nice pretty-printing solution borrowed from this
# SO post: http://stackoverflow.com/a/4590052/2591616
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

indent(root)

# Write the outfile using etree's method.
with open(a_out, 'w') as f_out:
    tree.write(f_out)
