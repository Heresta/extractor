from lxml import etree as ET
import re


def clean_file(fichier: str) -> str:
    """
    Deals with the cleaning of the final document of the pipeline.
    Gets ride of some tags and closes some, adds some attributes and namespaces/link to ODD.
    :param fichier: str
        Path towards the file to modify
    """
    file = ET.parse(fichier)
    root = file.getroot()
    # transform the parsed file into strings that can be modified easily
    strings = ET.tostring(root, encoding='unicode')
    strings = strings.split("\n")
    intern = ""
    for i in strings:
        # search by tag
        if "lb" in i:
            propre = i.replace("</lb>", "")
            propre = propre.replace('<lb break="no" rend="¬"/>', "")
            if i[-6] == "¬":
                propre = re.sub("¬", "", propre)
                propre = re.sub(">", ' break="no" rend = "¬"/>', propre)
                propre = re.sub("^\s*", "", propre)
                intern += propre + "\n"
            else:
                propre = re.sub(">", "/>", propre)
                propre = re.sub("^\s*", "", propre)
                intern += propre + "\n"
        # search by prefix of namespace
        elif "ns0" in i:
            i = re.sub("ns0:", "", i)
            i = re.sub(":ns0", "", i)
            intern += i + "\n"
        else:
            i = re.sub("^\s*", "", i)
            intern += i + "\n"
    # add xml version + link to ODD
    intern = intern.replace("<TEI", '<?xml version="1.0" encoding="UTF-8"?>\n<?xml-model href="./ODD/out/ODD.rng" '
                                    'type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>\n'
                                    '<?xml-model href="./ODD/out/ODD.rng" type="application/xml"\n'
                                    'schematypens="http://purl.oclc.org/dsdl/schematron"?>\n<TEI')
    intern = intern.replace("\n\n", '\n')
    # new cleaned file, which replaces the input one
    with open(fichier, "wb") as f:
        f.write(bytes(intern, encoding="utf-8"))
