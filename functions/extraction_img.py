from lxml import etree as ET


def extraction_image(doc_final, titre, editeur_scientifique, id_facsimile):
    """
    Creates a TEI file with a list of all illustrations in a book according to
    information in facsimile tag in another TEI file.
    :param doc_final: str
        Path to file where to extract illustrations' information
    :param titre: str
        Title of the book
    :param id_facsimile: str
        Id of the book
    """
    dossier_resultat_transformation = "./" + id_facsimile + "/xml/transformation_TEI/"
    document_final = ET.parse(doc_final)
    racine = document_final.getroot()
    # <grpList>
    root = ET.Element('TEI')
    root.set('id', id_facsimile)
    teiHeader = ET.SubElement(root, "teiHeader")
    fileDesc = ET.SubElement(teiHeader, "fileDesc")
    titleStmt = ET.SubElement(fileDesc, "titleStmt")
    title = ET.SubElement(titleStmt, "title")
    title.text = titre
    publicationStmt = ET.SubElement(fileDesc, "publicationStmt")
    publisher = ET.SubElement(publicationStmt, "publisher")
    publisher.text = editeur_scientifique
    sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
    p = ET.SubElement(sourceDesc, "p")
    p.text = "Gallica"
    facsimile = ET.SubElement(root, "facsimile")
     # on veut récupérer Decoration (BT4) et DropCapital (BT5)
      # parser le fichier dans l'output
      # aller dans TEI/facsimile
      # boucle for : pour chaque surface
    for surfaceGrp in racine[1]:
      # <listGrp>
        surfacegrp = ET.SubElement(facsimile, "surfaceGrp")
        surfacegrp.attrib["{http://www.w3.org/XML/1998/namespace}id"] = surfaceGrp.attrib['{http://www.' \
                                                                                          'w3.org/XML/1998/namespace}id']
        for surface in surfaceGrp:
            print(surface.attrib['corresp'])
       # if surfaceGrp/@type = BT4
            if surface.attrib['corresp'] == "#BT4":
       # <list type="Decoration">
                surfaceimg = ET.SubElement(surfacegrp, "surface")
                surfaceimg.set("type", "Decoration")
         # <item>value-of @source</item>
                figure = ET.SubElement(surfaceimg, "figure")
                figure.text = surface.attrib['source']
       # elif surfaceGrp/@type = BT5
            elif surface.attrib['corresp'] == "#BT5":
       # <list type="DropCapital">
                surfaceimg = ET.SubElement(surfacegrp, "surface")
                surfaceimg.set("type", "DropCapital")
         # <item>value-of @source</item>
                figure = ET.SubElement(surfaceimg, "figure")
                figure.text = surface.attrib['source']
    text = ET.SubElement(root, "text")
    body = ET.SubElement(text, "body")
    ET.SubElement(body, "p")
    with open(dossier_resultat_transformation + 'extration_img.xml', 'wb') as f:
        f.write(ET.tostring(root))
