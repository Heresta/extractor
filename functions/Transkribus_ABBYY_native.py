from lxml import etree as ET
from functions.sorted import sortchildrenby
from functions.count_words import count_words
import errno
import os
import shutil
import json
import datetime


def tes(chemin, chemin_img, editeur_ORCID, edition, url_edition, availability, isni_auteur, editeur_historique,
        ville_edition, titre, annee, auteur, auteur_nom, id_facsimile, notice_cat, ark, url_images):
    """
    Cette fonction a pour but de traiter la transformation des documents xml en ALTO4 sortant d'eScriptorium
    après être passés par Transkribus et ABBYY. Cette transformation permet de standardiser le document pour pouvoir
    utiliser une seule feuille de transformation générale pour passer en TEI par la suite.

    :param chemin: str
        Chemin qui va chercher les fichiers ALTO4 en sortie d'eScriptorium
    :param chemin_img: str
        Chemin qui va chercher les images en sortie d'eScriptorium
    :param editeur_ORCID: str
        Récupération du nom de l'éditeur et de son ORCID
    :param edition: str
        Récupération du nom de l'édition
    :param url_edition: str
        Récupération de l'URL de l'édition
    :param availability: str
        Récupération de l'information sur la licence
    :param isni_auteur: str
        Récupération de l'information sur l'isni de l'auteur
    :param editeur_historique: str
        Récupération de l'information sur l'éditeur historique
    :param ville_edition: str
        Récupération de l'information sur la ville d'édition
    :param titre: str
        Récupération du titre de l'édition
    :param annee: str
        Récupération de l'année d'édition
    :param auteur: str
        Récupération du nom et du prénom de l'auteur de l'édition
    :param auteur_nom: str
        Récupération du nom de l'auteur de l'édition
    :param id_facsimile: str
        Récupération de l'id du facsimile étudié
    :param notice_cat: str
        Récupération de l'URL de la notice de catalogue du facsimile
    :param ark: str
        Récupération du numéro d'ark
    :param url_images: str
        Récupération de l'url des images IIIF

    :return:
    Des fichiers ALTO4 selon le dossier donné en entrée, transformés selon les fichiers xsl lié à cette fonction.
    """

    intermediaire = "./intermediaire/"
    intermediaire_copie_xml = "./intermediaire/copie_fichier_xml/"
    intermediaire_post_copie = "./intermediaire/post_copie_fichier_xml/"
    intermediaire_copie_img = "./intermediaire/copie_fichier_img/"

    # récupérer le dossier des fichiers xml à renommer et à transformer et le dossier résultat
    dossier_resultat_standardisation = "./" + id_facsimile + "/xml/ALTOS/"
    dossier_resultat_transformation = "./" + id_facsimile + "/xml/TEI/"

    # récupérer le dossier des images à renommer
    dossier_resultat_img = "./" + id_facsimile + "/img/"

    # si le dossier resultat n'existe pas pour les fichiers xml, on le crée, sinon, on ne fait rien
    if not os.path.exists(os.path.dirname(dossier_resultat_standardisation)):
        try:
            os.makedirs(os.path.dirname(dossier_resultat_standardisation))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # si le dossier resultat n'existe pas pour les fichiers xml, on le crée, sinon, on ne fait rien
    if not os.path.exists(os.path.dirname(dossier_resultat_transformation)):
        try:
            os.makedirs(os.path.dirname(dossier_resultat_transformation))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # si le dossier resultat n'existe pas pour les img, on le crée, sinon, on ne fait rien
    if not os.path.exists(os.path.dirname(dossier_resultat_img)):
        try:
            os.makedirs(os.path.dirname(dossier_resultat_img))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # Récupération d'informations auprès du user
    editeur = editeur_ORCID.split("_")
    editeur_identite = ""
    for item in editeur:
        if item != editeur[-1]:
            editeur_identite += item + " "
    if '0' in editeur[-1]:
        editeur_ORCID = "orcid:" + editeur[-1]
    else:
        editeur_ORCID = ""
    commentaire = "Transformation of ALTO4 files from eScriptorium into XML-TEI"
    with open("functions/licences.json") as f:
        licence = json.load(f)
        status_availability = licence["licenses"][availability]["status"]
        target_licence = licence["licenses"][availability]["url"]
    isni_author = "isni:" + str(isni_auteur)
    geonames = str(None)
    with open('functions/geonames.json') as f:
        file = json.load(f)
        for ville in file["geonames"]:
            if ville_edition == str(ville["label"]):
                geonames = ville["code"]
    isni_editeur_historique = input("Indiquez l'isni de l'éditeur historique, s'il en possède un : ")

    liste_fichier = []
    for file in os.listdir(chemin):
        liste_fichier.append(file)
    n_image = str(len(liste_fichier))

    # Renommage des images

    liste_fichier_img = []
    for fichier in os.listdir(chemin_img):
        liste_fichier_img.append(fichier)
        shutil.copyfile(chemin_img + fichier, intermediaire_copie_img + fichier)

    for fichier in os.listdir(intermediaire_copie_img):
        for nom in liste_fichier_img:
            if nom == fichier:
                if "_" in nom[:2]:
                    propre = str(int(nom[:1]) + 1)
                    extension = nom[-4:]
                else:
                    propre = str(int(nom[:2]) + 1)
                    extension = nom[-4:]
                os.rename(intermediaire_copie_img + fichier,
                          dossier_resultat_img + "gallica_" + ark + "_" + auteur_nom
                          + "_" + titre.replace("/", '') + "_" + annee + "_" + propre + extension)

    # Première étape de la transformation des fichiers xml

    liste_fichier_xml = []
    for file in os.listdir(chemin):
        liste_fichier_xml.append(file)

    for fichier in os.listdir(chemin):
        shutil.copyfile(chemin+fichier, intermediaire_copie_xml+fichier)

    for fichier in os.listdir(intermediaire_copie_xml):
        for nom in liste_fichier_xml:
            if nom == fichier:
                if "_" in nom[:2]:
                    propre = str(int(nom[:1]) + 1)
                else:
                    propre = str(int(nom[:2])+1)
                os.rename(intermediaire_copie_xml+fichier, intermediaire_post_copie+"gallica_"+ark+"_"+auteur_nom
                          + "_" + titre.replace("/", '') + "_" + annee + "_" + propre + ".xml")

    for fichier in os.listdir(intermediaire_post_copie):
        tag_label = {"textblock": [["BT1", "Title", "block type Title"],
                                   ["BT2", "Main", "block type Main"],
                                   ["BT3", "Damage", "block type Damage"],
                                   ["BT4", "Decoration", "block type Decoration"],
                                   ["BT5", "DropCapital", "block type DropCapital"],
                                   ["BT6", "Figure", "block type Figure"],
                                   ["BT7", "Margin", "block type Margin"],
                                   ["BT8", "Numbering", "block type Numbering"],
                                   ["BT9", "MusicNotation", "block type MusicNotation"],
                                   ["BT10", "RunningTitle", "block type RunningTitle"],
                                   ["BT11", "Seal", "block type Seal"],
                                   ["BT12", "Signatures", "block type Signatures"],
                                   ["BT13", "Stamp", "block type Stamp"],
                                   ["BT14", "Table", "block type Table"]],
                     "textline": [["LT1", "Default", "block type Default"],
                                  ["LT2", "DropCapitalLine", "block type DropCapitalLine"],
                                  ["LT3", "Interlinear", "block type Interlinear"],
                                  ["LT4", "MusicLine", "block type MusicLine"],
                                  ["LT5", "Rubric", "block type Rubric"]]}
        find_text = ET.XPath("//text()")
        file = ET.parse(intermediaire_post_copie + fichier)
        root = file.getroot()
        text = find_text(root)
        texte = []
        for t in text:
            if t.startswith("\n") is False:
                texte.append(t)
        racine = ET.Element("alto")
        Description = ET.SubElement(racine, "Description")
        MeasurementUnit = ET.SubElement(Description, "MeasurementUnit")
        MeasurementUnit.text = texte[0]
        sourceImageInformation = ET.SubElement(Description, "sourceImageInformation")
        fileName = ET.SubElement(sourceImageInformation, "fileName")
        fileName.text = texte[1]
        fileIdentifier = ET.SubElement(sourceImageInformation, "fileIdentifier")
        fileIdentifier.text = fichier[:-3] + "jpg"
        Tags = ET.SubElement(racine, "Tags")
        for tag in tag_label["textblock"]:
            OtherTag = ET.SubElement(Tags, "OtherTag")
            OtherTag.set("ID", tag[0])
            OtherTag.set("LABEL", tag[1])
            OtherTag.set("DESCRIPTION", tag[2])
        for tag in tag_label["textline"]:
            OtherTag = ET.SubElement(Tags, "OtherTag")
            OtherTag.set("ID", tag[0])
            OtherTag.set("LABEL", tag[1])
            OtherTag.set("DESCRIPTION", tag[2])
        Layout = ET.SubElement(racine, "Layout")
        Page = ET.SubElement(Layout, "Page")
        for page in root[2]:
            Page.set("WIDTH", page.get("WIDTH"))
            Page.set("HEIGHT", page.get("HEIGHT"))
            Page.set("PHYSICAL_IMG_NR", page.get("PHYSICAL_IMG_NR"))
            Page.set("ID", page.get("ID"))
            PrintSpace = ET.SubElement(Page, "PrintSpace")
            for printspace in page:
                PrintSpace.set("HPOS", printspace.get("HPOS"))
                PrintSpace.set("VPOS", printspace.get("VPOS"))
                PrintSpace.set("WIDTH", printspace.get("WIDTH"))
                PrintSpace.set("HEIGHT", printspace.get("HEIGHT"))
                for textblock in printspace:
                    TextBlock = ET.SubElement(PrintSpace, "TextBlock")
                    TextBlock.set("HPOS", textblock.get("HPOS"))
                    TextBlock.set("VPOS", textblock.get("VPOS"))
                    TextBlock.set("WIDTH", textblock.get("WIDTH"))
                    TextBlock.set("HEIGHT", textblock.get("HEIGHT"))
                    TextBlock.set("ID", textblock.get("ID"))
                    for item in root[1]:
                        if textblock.get("TAGREFS") == item.get("ID"):
                            for ref in tag_label["textblock"]:
                                if ref[1] == item.get("LABEL"):
                                    TextBlock.set("TAGREFS", ref[0])
                    for balise in textblock:
                        if balise.tag == '{http://www.loc.gov/standards/alto/ns-v4#}Shape':
                            Shapeblock = ET.SubElement(TextBlock, "Shape")
                            for polygon in balise:
                                Polygonblock = ET.SubElement(Shapeblock, "Polygon")
                                Polygonblock.set("POINTS", polygon.get("POINTS"))
                        elif balise.tag == '{http://www.loc.gov/standards/alto/ns-v4#}TextLine':
                            TextLine = ET.SubElement(TextBlock, "TextLine")
                            TextLine.set("ID", balise.get("ID"))
                            for item in root[1]:
                                if balise.get("TAGREFS") == item.get("ID"):
                                    for ref in tag_label["textline"]:
                                        if ref[1] == item.get("LABEL"):
                                            TextLine.set("TAGREFS", str(ref[0]))
                            TextLine.set("BASELINE", balise.get("BASELINE"))
                            TextLine.set("HPOS", balise.get("HPOS"))
                            TextLine.set("VPOS", balise.get("VPOS"))
                            TextLine.set("WIDTH", balise.get("WIDTH"))
                            TextLine.set("HEIGHT", balise.get("HEIGHT"))
                            for cas in balise:
                                if cas.tag == '{http://www.loc.gov/standards/alto/ns-v4#}Shape':
                                    Shapeline = ET.SubElement(TextLine, "Shape")
                                    for poly in balise:
                                        for polygon in poly:
                                            Polygonline = ET.SubElement(Shapeline, "Polygon")
                                            Polygonline.set("POINTS", polygon.get("POINTS"))
                                elif cas.tag == '{http://www.loc.gov/standards/alto/ns-v4#}String':
                                    String = ET.SubElement(TextLine, "String")
                                    String.set("CONTENT", cas.get("CONTENT"))
                                    String.set("HPOS", cas.get("HPOS"))
                                    String.set("VPOS", cas.get("VPOS"))
                                    String.set("WIDTH", cas.get("WIDTH"))
                                    String.set("HEIGHT", cas.get("HEIGHT"))
        # on créé un nouveau fichier dans le dossier résultat
        with open(dossier_resultat_standardisation+fichier, mode='wb') as f:
            f.write(ET.tostring(racine, encoding='utf-8'))

    # Test de la validité des fichiers ALTO4
    liste_fichier = []
    for file in os.listdir(dossier_resultat_standardisation):
        liste_fichier.append(file)

    # Deuxième étape de la transformation

    liste_fichier = []
    for file in os.listdir(dossier_resultat_standardisation):
        liste_fichier.append(file)

    root1 = ET.Element("root")
    texte1 = ET.SubElement(root1, "text")
    texte1.text = ark
    with open('./intermediaire/intermediaire/ark.xml', 'wb') as f:
        f.write(ET.tostring(root1))

    root1 = ET.Element("root")
    texte1 = ET.SubElement(root1, "text")
    texte1.text = id_facsimile
    with open('./intermediaire/intermediaire/id_facsimile.xml', 'wb') as f:
        f.write(ET.tostring(root1))

    root = ET.Element("{http://www.tei-c.org/ns/1.0}TEI")

    header = ET.SubElement(root, "teiHeader")
    # Balise fileDesc
    fileDesc = ET.SubElement(header, "fileDesc")
    titleStmt = ET.SubElement(fileDesc, "titleStmt")
    title_main = ET.SubElement(titleStmt, "title")
    title_main.set("type", "main")
    title_main.text = titre
    title_sub = ET.SubElement(titleStmt, "title")
    title_sub.set("type", "sub")
    title_sub.text = edition
    author = ET.SubElement(titleStmt, "author")
    author.set("ref", isni_author)
    author.text = auteur
    editor = ET.SubElement(titleStmt, "editor")
    if len(editeur_ORCID) > 0:
        editor.set("ref", editeur_ORCID)
    editor.text = editeur_identite
    extent = ET.SubElement(fileDesc, "extent")
    measure_images = ET.SubElement(extent, "measure")
    measure_images.set("unit", "images")
    measure_images.set("n", n_image)
    measure_words = ET.SubElement(extent, "measure")
    measure_words.set("unit", "words")
    nb_words = str(count_words(dossier_resultat_standardisation))
    measure_words.set("n", nb_words)
    publicationStmt = ET.SubElement(fileDesc, "publicationStmt")
    publisher = ET.SubElement(publicationStmt, "publisher")
    publisher.text = edition
    ref_publicationStmt = ET.SubElement(publicationStmt, "ref")
    ref_publicationStmt.set("target", url_edition)
    avail = ET.SubElement(publicationStmt, "availability")
    avail.set("status", status_availability)
    avail.set("n", availability)
    licence = ET.SubElement(avail, "licence")
    licence.set("target", target_licence)
    sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
    bibl = ET.SubElement(sourceDesc, "bibl")
    ref_bibl = ET.SubElement(bibl, "ref")
    ref_bibl.set("target", notice_cat)
    author_bibl = ET.SubElement(bibl, "author")
    author_bibl.set("ref", isni_author)
    author_bibl.text = auteur
    title_bibl = ET.SubElement(bibl, "title")
    title_bibl.text = titre
    pubPlace = ET.SubElement(bibl, "pubPlace")
    pubPlace.set("ref", geonames)
    pubPlace.text = ville_edition
    publisher_bibl = ET.SubElement(bibl, "publisher")
    if len(isni_editeur_historique) > 0:
        publisher_bibl.set("ref", isni_editeur_historique)
    else :
        publisher_bibl.set("ref", "None")
    publisher_bibl.text = editeur_historique
    date = ET.SubElement(bibl, "date")
    date.set("when", annee)
    date.text = annee
    msDesc = ET.SubElement(sourceDesc, "msDesc")
    msIdentifier = ET.SubElement(msDesc, "msIdentifier")
    settlement = ET.SubElement(msIdentifier, "settlement")
    settlement.text = "Paris"
    institution = ET.SubElement(msIdentifier, "institution")
    institution.text = "BnF"
    idno = ET.SubElement(msIdentifier, "idno")
    idno.text = ark
    physDesc = ET.SubElement(msDesc, "physDesc")
    decoDesc = ET.SubElement(physDesc, "decoDesc")
    decoNote = ET.SubElement(decoDesc, "decoNote")
    decoNote.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "id_DB_imprimeurs"
    p = ET.SubElement(decoNote, "p")
    p.text = "Les décorations, ornementations, illustrations, initiales liées à cet id proviennent de l'atelier de"
    encodingDesc = ET.SubElement(header, "encodingDesc")
    editorialDecl = ET.SubElement(encodingDesc, "editorialDecl")
    interpretation = ET.SubElement(editorialDecl, "interpretation")
    p_encoding = ET.SubElement(interpretation, "p")
    interpGrp_zone = ET.SubElement(p_encoding, "interpGrp")
    interpGrp_zone.set("type", "zoneSegmOnto")
    interp_BT1 = ET.SubElement(interpGrp_zone, "interp")
    interp_BT1.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "BT1"
    interp_BT1.set("corresp", "https://github.com/SegmOnto/examples/blob/main/zones/Title/Title.md")
    interp_BT2 = ET.SubElement(interpGrp_zone, "interp")
    interp_BT2.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "BT2"
    interp_BT2.set("corresp", "https://github.com/SegmOnto/examples/blob/main/zones/Main/Main.md")
    interp_BT3 = ET.SubElement(interpGrp_zone, "interp")
    interp_BT3.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "BT3"
    interp_BT3.set("corresp", "https://github.com/SegmOnto/examples/blob/main/zones/Damage/Damage.md")
    interp_BT4 = ET.SubElement(interpGrp_zone, "interp")
    interp_BT4.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "BT4"
    interp_BT4.set("corresp", "https://github.com/SegmOnto/examples/blob/main/zones/Decoration/Decoration.md")
    interp_BT5 = ET.SubElement(interpGrp_zone, "interp")
    interp_BT5.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "BT5"
    interp_BT5.set("corresp", "https://github.com/SegmOnto/examples/blob/main/zones/DropCapital/DropCapital.md")
    interp_BT6 = ET.SubElement(interpGrp_zone, "interp")
    interp_BT6.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "BT6"
    interp_BT6.set("corresp", "https://github.com/SegmOnto/examples/blob/main/zones/Figure/Figure.md")
    interp_BT7 = ET.SubElement(interpGrp_zone, "interp")
    interp_BT7.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "BT7"
    interp_BT7.set("corresp", "https://github.com/SegmOnto/examples/blob/main/zones/Margin/Margin.md")
    interp_BT8 = ET.SubElement(interpGrp_zone, "interp")
    interp_BT8.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "BT8"
    interp_BT8.set("corresp", "https://github.com/SegmOnto/examples/blob/main/zones/Numbering/Numbering.md")
    interp_BT9 = ET.SubElement(interpGrp_zone, "interp")
    interp_BT9.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "BT9"
    interp_BT9.set("corresp", "https://github.com/SegmOnto/examples/blob/main/zones/MusicNotation/MusicNotation.md")
    interp_BT10 = ET.SubElement(interpGrp_zone, "interp")
    interp_BT10.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "BT10"
    interp_BT10.set("corresp", "https://github.com/SegmOnto/examples/blob/main/zones/RunningTitle/RunningTitle.md")
    interp_BT11 = ET.SubElement(interpGrp_zone, "interp")
    interp_BT11.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "BT11"
    interp_BT11.set("corresp", "https://github.com/SegmOnto/examples/blob/main/zones/Seal/Seal.md")
    interp_BT12 = ET.SubElement(interpGrp_zone, "interp")
    interp_BT12.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "BT12"
    interp_BT12.set("corresp", "https://github.com/SegmOnto/examples/blob/main/zones/Signatures/Signatures.md")
    interp_BT13 = ET.SubElement(interpGrp_zone, "interp")
    interp_BT13.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "BT13"
    interp_BT13.set("corresp", "https://github.com/SegmOnto/examples/blob/main/zones/Stamp/Stamp.md")
    interp_BT14 = ET.SubElement(interpGrp_zone, "interp")
    interp_BT14.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "BT14"
    interp_BT14.set("corresp", "https://github.com/SegmOnto/examples/blob/main/zones/Table/Table.md")
    interpGrp_line = ET.SubElement(p_encoding, "interpGrp")
    interpGrp_line.set("type", "lineSegmOnto")
    interp_LT1 = ET.SubElement(interpGrp_line, "interp")
    interp_LT1.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "LT1"
    interp_LT1.set("corresp", "https://github.com/SegmOnto/examples/blob/main/lines/Default/Default.md")
    interp_LT2 = ET.SubElement(interpGrp_line, "interp")
    interp_LT2.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "LT2"
    interp_LT2.set("corresp", "https://github.com/SegmOnto/examples/blob/main/lines/DropCapitalLine/DropCapitalLine.md")
    interp_LT3 = ET.SubElement(interpGrp_line, "interp")
    interp_LT3.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "LT3"
    interp_LT3.set("corresp", "https://github.com/SegmOnto/examples/blob/main/lines/Interlinear/Interlinear.md")
    interp_LT4 = ET.SubElement(interpGrp_line, "interp")
    interp_LT4.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "LT4"
    interp_LT4.set("corresp", "https://github.com/SegmOnto/examples/blob/main/lines/MusicLine/MusicLine.md")
    interp_LT5 = ET.SubElement(interpGrp_line, "interp")
    interp_LT5.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "LT5"
    interp_LT5.set("corresp", "https://github.com/SegmOnto/examples/blob/main/lines/Rubric/Rubric.md")
    revisionDesc = ET.SubElement(header, "revisionDesc")
    change = ET.SubElement(revisionDesc, "change")
    change.set("who", "#" + editeur_ORCID)
    current = datetime.datetime.today()
    if len(str(current.day)) == 1:
        day = "0" + str(current.day)
    else:
        day = str(current.day)
    if len(str(current.month)) == 1:
        month = "0" + str(current.month)
    else:
        month = str(current.month)
    year = current.year
    current_date = str(year) + "-" + str(month) + "-" + day
    change.set("when", current_date)
    change.text = commentaire
    facs = ET.SubElement(root, "facsimile")
    facs.attrib["{http://www.w3.org/XML/1998/namespace}id"] = id_facsimile
    facs.set("source", "https://gallica.bnf.fr/ark:/12148/" + ark)
    for fichier in os.listdir(dossier_resultat_standardisation):
        surfaceGrp = ET.SubElement(facs, "surfaceGrp")
        data = fichier.split("_")
        numero_folio_extension = data[-1]
        numero_folio = numero_folio_extension[0:-4]
        if len(numero_folio) == 1:
            numero_folio = "000" + numero_folio
        elif len(numero_folio) == 2:
            numero_folio = "00" + numero_folio
        elif len(numero_folio) == 3:
            numero_folio = "0" + numero_folio
        surfaceGrp.attrib["{http://www.w3.org/XML/1998/namespace}id"] = id_facsimile + "_" + numero_folio
        surfaceGrp.set("type", "page")
        for image in url_images:
            img = image.split('/')
            if img[-5].replace('f', '') == numero_folio:
                surfaceGrp.set('source', image)
        file = ET.parse(dossier_resultat_standardisation + fichier)
        root4 = file.getroot()
        for Page in root4[2]:
            for PrintSpace in Page:
                n = 1
                i = 0
                for TextBlock in PrintSpace:
                    surface = ET.SubElement(surfaceGrp, "surface")
                    surface.attrib["{http://www.w3.org/XML/1998/namespace}id"] = id_facsimile + "_" + numero_folio + "_" + str(TextBlock.get("TAGREFS")) + "_" + str(n)
                    surface.set("source",
                                   "https://gallica.bnf.fr/iiif/ark:/12148/" + ark + "/f" + numero_folio + "/" +
                                   TextBlock.get("HPOS") + "," + TextBlock.get("VPOS") + "," + TextBlock.get(
                                       "WIDTH") + "," +
                                   TextBlock.get("HEIGHT") + "/full/0/native")
                    surface.set("corresp", "#" + str(TextBlock.get("TAGREFS")))
                    if TextBlock.get('TAGREFS') == "BT4":
                        surface.set("ana", "doit pointer vers xml:id dans decoNote")
                    elif TextBlock.get('TAGREFS') == "BT5":
                        surface.set("ana", "doit pointer vers xml:id dans decoNote")
                    elif TextBlock.get('TAGREFS') == "BT6":
                        surface.set("ana", "doit pointer vers xml:id dans decoNote")
                    i += 1
                    o = 1
                    n += 1
                    for TextLine in TextBlock:
                        if TextLine.tag == 'TextLine':
                            zone = ET.SubElement(surface, "zone")
                            zone.attrib["{http://www.w3.org/XML/1998/namespace}id"] = id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS") + "_" + str(n -1) + "_" + TextLine.get("TAGREFS") + "_" + str(o)
                            zone.set("corresp", "#" + TextLine.get("TAGREFS"))
                            o += 1
                            for Shape in TextLine:
                                if Shape.tag == 'Shape':
                                    for Polygon in Shape:
                                        zone.set("points", Polygon.get("POINTS"))
                            zone.set("source",
                                     "https://gallica.bnf.fr/iiif/ark:/12148/" + ark + "/f" + numero_folio + "/" +
                                     TextLine.get("HPOS") + "," + TextLine.get("VPOS") + "," + TextLine.get(
                                         "WIDTH") + "," +
                                     TextLine.get("HEIGHT") + "/full/0/native")
                            p = 1
                            for String in TextLine:
                                if String.tag == 'String':
                                    path = ET.SubElement(zone, "path")
                                    path.attrib["{http://www.w3.org/XML/1998/namespace}id"] = id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS") + "_" + str(n - 1) + "_" + TextLine.get("TAGREFS") + "_" + str(o - 1) + "_" + str(p)
                                    p += 1
                                    path.set("points", TextLine.get("BASELINE"))
    text = ET.SubElement(root, "text")
    body = ET.SubElement(text, "body")

    for fichier in os.listdir(dossier_resultat_standardisation):
        data = fichier.split("_")
        numero_folio_extension = data[-1]
        numero_folio = numero_folio_extension[0:-4]
        if len(numero_folio) == 1:
            numero_folio = "000" + numero_folio
        elif len(numero_folio) == 2:
            numero_folio = "00" + numero_folio
        elif len(numero_folio) == 3:
            numero_folio = "0" + numero_folio
        div = ET.SubElement(body, "div")
        div.set("n", "#" + id_facsimile + "_" + numero_folio)
        file = ET.parse(dossier_resultat_standardisation + fichier)
        root11 = file.getroot()
        for Page in root11[2]:
            for PrintSpace in Page:
                n = 1
                for TextBlock in PrintSpace:
                    if TextBlock.get("TAGREFS") == 'BT1':
                        p = ET.SubElement(div, "p")
                        p.set("facs",
                              "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS") + "_" + str(n))
                        o = 1
                        n += 1
                        for TextLine in TextBlock:
                            if TextLine.tag == 'TextLine':
                                for String in TextLine:
                                    if String.tag == 'String':
                                        lb = ET.SubElement(p, "lb")
                                        lb.set("facs",
                                               "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get(
                                                   "TAGREFS")
                                               + "_" + str(n - 1) + "_" + TextLine.get("TAGREFS") + "_" + str(o))
                                        lb.text = String.get("CONTENT")
                                        if "¬" in String.get("CONTENT"):
                                            lbreak = ET.SubElement(p, "lb")
                                            lbreak.set("break", "no")
                                            lbreak.set("rend", "¬")
                                        o += 1
                    elif TextBlock.get("TAGREFS") == 'BT2':
                        p = ET.SubElement(div, "p")
                        p.set("facs",
                              "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS") + "_" + str(n))
                        o = 1
                        n += 1
                        for TextLine in TextBlock:
                            if TextLine.tag == 'TextLine':
                                for String in TextLine:
                                    if String.tag == 'String':
                                        if TextLine.get("TAGREFS") == "LT1":
                                            lb = ET.SubElement(p, "lb")
                                            lb.set("facs",
                                                   "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get(
                                                       "TAGREFS")
                                                   + "_" + str(n - 1) + "_" + TextLine.get("TAGREFS") + "_" + str(o))
                                            lb.text = String.get("CONTENT")
                                            if "¬" in String.get("CONTENT"):
                                                lbreak = ET.SubElement(p, "lb")
                                                lbreak.set("break", "no")
                                                lbreak.set("rend", "¬")
                                        elif TextLine.get("TAGREFS") == "LT2":
                                            hi = ET.SubElement(p, "hi")
                                            for TextBlockInitiale in PrintSpace:
                                                if TextBlockInitiale.get("TAGREFS") == "BT5":
                                                    for TextLineInitiale in TextBlockInitiale:
                                                        if TextLineInitiale.tag == 'TextLine':
                                                            for StringInitiale in TextLineInitiale:
                                                                if StringInitiale.tag == 'String':
                                                                    hi.set("facs",
                                                                                   "#" + id_facsimile + "_" +
                                                                                   numero_folio + "_" +
                                                                                   TextBlockInitiale.get(
                                                                                       "TAGREFS")
                                                                                   + "_" + str(
                                                                                       n - 1) + "_" +
                                                                                   TextLineInitiale.get("TAGREFS") +
                                                                                   "_" + str(o))
                                                                    hi.text = StringInitiale.get("CONTENT")
                                            lb = ET.SubElement(p, "lb")
                                            lb.set("facs",
                                                   "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get(
                                                       "TAGREFS")
                                                   + "_" + str(n - 1) + "_" + TextLine.get("TAGREFS") + "_" + str(o))
                                            lb.text = String.get("CONTENT")
                                            if "¬" in String.get("CONTENT"):
                                                lbreak = ET.SubElement(p, "lb")
                                                lbreak.set("break", "no")
                                                lbreak.set("rend", "¬")
                                        o += 1
                    elif TextBlock.get('TAGREFS') == 'BT3':
                        note = ET.SubElement(div, "note")
                        damage = ET.SubElement(note, "damage")
                        damage.set("facs",
                            "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS") + "_" + str(n))
                        n += 1
                    elif TextBlock.get("TAGREFS") == 'BT7':
                        note = ET.SubElement(div, "note")
                        note.set("facs",
                              "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS") + "_" + str(n))
                        o = 1
                        n += 1
                        for TextLine in TextBlock:
                            if TextLine.tag == 'TextLine':
                                for String in TextLine:
                                    if String.tag == 'String':
                                        lb = ET.SubElement(note, "lb")
                                        lb.set("facs",
                                               "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS")
                                               + "_" + str(n - 1) + "_" + TextLine.get("TAGREFS") + "_" + str(o))
                                        lb.text = String.get("CONTENT")
                                        if "¬" in String.get("CONTENT"):
                                            lbreak = ET.SubElement(note, "lb")
                                            lbreak.set("break", "no")
                                            lbreak.set("rend", "¬")
                                        o += 1
                    elif TextBlock.get("TAGREFS") == 'BT8':
                        p = ET.SubElement(div, "fw")
                        p.set("facs",
                              "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS") + "_" + str(n))
                        o = 1
                        n += 1
                        for TextLine in TextBlock:
                            if TextLine.tag == 'TextLine':
                                for String in TextLine:
                                    if String.tag == 'String':
                                        lb = ET.SubElement(p, "lb")
                                        lb.set("facs",
                                               "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS")
                                               + "_" + str(n - 1) + "_" + TextLine.get("TAGREFS") + "_" + str(o))
                                        lb.text = String.get("CONTENT")
                                        if "¬" in String.get("CONTENT"):
                                            lbreak = ET.SubElement(p, "lb")
                                            lbreak.set("break", "no")
                                            lbreak.set("rend", "¬")
                                        o += 1
                    elif TextBlock.get("TAGREFS") == 'BT9':
                        figure = ET.SubElement(div, "figure")
                        figure.set("facs",
                              "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS") + "_" + str(n))
                        o = 1
                        n += 1
                        for TextLine in TextBlock:
                            if TextLine.tag == 'TextLine':
                                p = ET.SubElement(figure, "p")
                                for String in TextLine:
                                    if String.tag == 'String':
                                        lb = ET.SubElement(p, "lb")
                                        lb.set("facs",
                                               "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS")
                                               + "_" + str(n - 1) + "_" + TextLine.get("TAGREFS") + "_" + str(o))
                                        if "¬" in String.get("CONTENT"):
                                            lbreak = ET.SubElement(p, "lb")
                                            lbreak.set("break", "no")
                                            lbreak.set("rend", "¬")
                                            lb.text = String.get("CONTENT")[:-1]
                                        else:
                                            lb.text = String.get("CONTENT")
                                        o += 1
                    elif TextBlock.get("TAGREFS") == 'BT10':
                        fw = ET.SubElement(div, "fw")
                        fw.set("facs",
                              "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS") + "_" + str(n))
                        o = 1
                        n += 1
                        for TextLine in TextBlock:
                            if TextLine.tag == 'TextLine':
                                for String in TextLine:
                                    if String.tag == 'String':
                                        lb = ET.SubElement(fw, "lb")
                                        lb.set("facs",
                                               "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS")
                                               + "_" + str(n - 1) + "_" + TextLine.get("TAGREFS") + "_" + str(o))
                                        if "¬" in String.get("CONTENT"):
                                            lbreak = ET.SubElement(p, "lb")
                                            lbreak.set("break", "no")
                                            lbreak.set("rend", "¬")
                                            lb.text = String.get("CONTENT")[:-1]
                                        else:
                                            lb.text = String.get("CONTENT")
                                        o += 1
                    elif TextBlock.get("TAGREFS") == 'BT11':
                        figure = ET.SubElement(div, "figure")
                        figure.set("facs",
                                   "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS") + "_" + str(
                                       n))
                        n += 1
                    elif TextBlock.get("TAGREFS") == 'BT12':
                        p = ET.SubElement(div, "fw")
                        p.set("facs",
                              "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS") + "_" + str(n))
                        o = 1
                        n += 1
                        for TextLine in TextBlock:
                            if TextLine.tag == 'TextLine':
                                for String in TextLine:
                                    if String.tag == 'String':
                                        lb = ET.SubElement(p, "lb")
                                        lb.set("facs",
                                               "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS")
                                               + "_" + str(n - 1) + "_" + TextLine.get("TAGREFS") + "_" + str(o))
                                        lb.text = String.get("CONTENT")
                                        if "¬" in String.get("CONTENT"):
                                            lbreak = ET.SubElement(p, "lb")
                                            lbreak.set("break", "no")
                                            lbreak.set("rend", "¬")
                                        o += 1
                    elif TextBlock.get("TAGREFS") == 'BT13':
                        figure = ET.SubElement(div, "figure")
                        figure.set("facs",
                                   "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS") + "_" + str(
                                       n))
                        n += 1
                    elif TextBlock.get("TAGREFS") == 'BT14':
                        table = ET.SubElement(div, 'table')
                        table.set("facs",
                                   "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS") + "_" + str(
                                       n))
                        o = 1
                        n += 1
                        for TextLine in TextBlock:
                            if TextLine.tag == 'TextLine':
                                for String in TextLine:
                                    if String.tag == 'String':
                                        row = ET.SubElement(table, "row")
                                        row.set("facs",
                                               "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS")
                                               + "_" + str(n - 1) + "_" + TextLine.get("TAGREFS") + "_" + str(o))
                                        row.text = String.get("CONTENT")
                    elif TextBlock.get("TAGREFS") == 'BT4':
                        figure = ET.SubElement(div, "figure")
                        figure.set("facs",
                                   "#" + id_facsimile + "_" + numero_folio + "_" + TextBlock.get("TAGREFS") + "_" +
                                   str(n))
                        figure.set("hand", "à remplir")

    with open(intermediaire + id_facsimile + "_" + ark + ".xml", "wb") as f:
        f.write(ET.tostring(root, encoding="utf-8"))

    sortchildrenby(dossier_resultat_transformation, intermediaire + id_facsimile + "_" + ark + ".xml")

    # Finalisation de la transformation
    shutil.rmtree(intermediaire)

    return dossier_resultat_transformation + id_facsimile + "_" + ark + ".xml"

