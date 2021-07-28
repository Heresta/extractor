from lxml import etree as ET
from copy import deepcopy


def sortchildrenby(dossier_resultat_transformation, fichier_origine):
    """
    Sorts a XML-TEI file by their id with div and surface tags.
    :param dossier_resultat_transformation: str
        Path to the directory where to stock the new file
    :param fichier_origine: str
        Path of the file to sort
    """
    with open(dossier_resultat_transformation + id_facsimile + "_" + ark + ".xml", "wb") as f:
        root = ET.Element("{http://www.tei-c.org/ns/1.0}TEI")
        file = ET.parse(fichier_origine)
        root11 = file.getroot()
        for balise in root11:
            if balise.tag == "teiHeader":
                root.append(deepcopy(balise))
            elif balise.tag == "facsimile":
                balise[:] = sorted(balise, key=lambda child: child.get("{http://www.w3.org/XML/1998/namespace}id"))
                root.append(deepcopy(balise))
            elif balise.tag == "text":
                text = ET.SubElement(root, "text")
                for body in balise:
                    body[:] = sorted(body, key=lambda child: child.get("n"))
                    text.append(deepcopy(body))
        ET.indent(root)
        f.write(ET.tostring(root, encoding="utf-8"))
