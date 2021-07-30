from functions.recuperation_donnees_SPARQL import recup_data_sparql
import re
import urllib.request
import json


def recuperation_donnees_manifest(manifest):
    """
    Recovers some metadata from manifest IIIF
    :param manifest: json
        URL to manifest IIIF
    :return: list
        List of metadata recovered
    """
    global titre, annee, auteur, auteur_nom, id_facsimile, notice_cat
    fichier = urllib.request.urlopen(manifest)
    myfile = fichier.read()
    with open("./intermediaire/intermediaire/manifest.json", "wb") as f:
        f.write(myfile)
    with open("./intermediaire/intermediaire/manifest.json") as f:
        manifestjson = json.load(f)

    # Récupérer les images
    url_image = []
    if manifestjson["sequences"][0]["canvases"][0]["images"][0]["resource"]["@id"].endswith("/full/full/0/native.jpg"):
        path = manifestjson["sequences"][0]["canvases"]
        for image in path:
            url_image.append(image["images"][0]["resource"]["@id"])
        if manifestjson["sequences"][0]["canvases"][0]["images"][0]["resource"]["@id"].startswith("https://gallica.bnf.fr"):
            # récupération du titre de l'ouvrage
            titre = manifestjson["metadata"][5]["value"]
            # récupération de l'année de publication de l'ouvrage
            annee = manifestjson["metadata"][6]["value"]
            # récupération de l'auteur de l'ouvrage
            auteur = ""
            if manifestjson["metadata"][9]["label"] == "Creator":
                auteur = manifestjson["metadata"][9]["value"].split('.')[0]
                auteur = re.sub('[\(].*?[\)]', "", auteur)
            else:
                ark = manifest.split('/')[-2]
                infos_sparql = recup_data_sparql(ark)
                if len(auteur) == 0:
                    for item in infos_sparql["results"]["bindings"]:
                        if item.keys() == "publication_place":
                            auteur = infos_sparql["results"]["bindings"][0]["publication_place"]["value"]
                        else:
                            auteur = input("Donnez le nom et le prénom de l'auteur, sous forme 'Dupont, Jean' : ")
            # récupération du nom de famille de l'auteur de l'ouvrage
            auteur_nom = auteur.split(",")[0]
            # creation de l'id du facsimile
            determinants = ["Le", "La", "Les", "Du", "De la", "Aux", "Au", "Un", "Une", "Des",
                            "Mon", 'Ton', "Son", 'Notre', "Votre", "Leur", "Ma", "Ta", "Sa",
                            "Mes", "Tes", "Ses", "Nos", "Vos", "Leurs", "Vostre", 'Nostre',
                            "Ce", "Cet", "Cette", "Ces", "Chaque", "Quelques", "Plusieurs"]
            id_facsimile = auteur_nom + titre.split(' ')[0] + annee
            for determinant in determinants:
                if titre.split(' ')[0] == determinant:
                    id_facsimile = auteur_nom + titre.split(' ')[1].capitalize() + annee
            id_facsimile = id_facsimile.replace(" ", "")
            id_facsimile = id_facsimile.replace(",", "")
            # récupération de la notice de catalogue de l'ouvrage
            if manifestjson["metadata"][9]["value"].startswith("Notice du catalogue :"):
                notice_cat = manifestjson["metadata"][9]["value"][22:]
            elif manifestjson["metadata"][10]["value"].startswith("Notice du catalogue :"):
                notice_cat = manifestjson["metadata"][10]["value"][22:]
            elif manifestjson["metadata"][11]["value"].startswith("Notice du catalogue :"):
                notice_cat = manifestjson["metadata"][11]["value"][22:]
            elif manifestjson["metadata"][12]["value"].startswith("Notice du catalogue :"):
                notice_cat = manifestjson["metadata"][12]["value"][22:]
        #elif manifestjson["sequences"][0]["canvases"][0]["images"][0]["resource"]["@id"].startswith("https://api.digitale-sammlungen.de/"):
            #titre = manifestjson["metadata"][1]["value"]
            #root = ET.Element("root")
            #texte = ET.SubElement(root, "text")
            #texte.text = titre
            #with open('./intermediaire/intermediaire/titre.xml', 'wb') as f:
                #f.write(ET.tostring(root))
            #annee = input("Donnez l'année d'édition du document : ")
            #root = ET.Element("root")
            #texte = ET.SubElement(root, "text")
            #texte.text = annee
            #with open('./intermediaire/intermediaire/date.xml', 'wb') as f:
                #f.write(ET.tostring(root))
            #auteur = manifestjson["metadata"][0]["value"].replace("<span>", "")
            #auteur = auteur.replace("<span>", "")
            #auteur = auteur.replace("</span>", "")
            #auteur = auteur.replace("</span>", "")
            #auteur = auteur.split()
            #auteur_identite = auteur[0]
            #auteur_ref = auteur[-1]
            #auteur_ref = re.sub('.*?\'[\>]', "", auteur_ref)
            #auteur_ref = auteur_ref.replace('</a>)', "")
            #auteur_ref = "nid:" + auteur_ref
            #root = ET.Element("root")
            #texte = ET.SubElement(root, "text")
            #texte.text = auteur_identite
            #with open('./intermediaire/intermediaire/auteur.xml', 'wb') as f:
                #f.write(ET.tostring(root))
            #auteur_nom = auteur_identite
            #for caractere in auteur_identite:
                #if caractere == ",":
                    #auteur_nom = auteur_identite.split(", ")[0]
            #id_facsimile = auteur_nom + titre.split(' ')[0] + annee
            #notice_cat = ["seeAlso"][0]["@id"].startswith("Notice du catalogue :")
            #root = ET.Element("root")
            #texte = ET.SubElement(root, "text")
            #texte.text = notice_cat
            #with open('./intermediaire/intermediaire/notice_cat.xml', 'wb') as f:
                #f.write(ET.tostring(root))
        else:
            print("Le traitement de ce type de manifest IIIF n'a pas été implémenté dans ce code. ")
    #elif manifestjson["items"][0]["items"][0]["items"][0]["body"]["id"].endswith("/full/full/0/native.jpg"):
        #path = manifestjson["items"]
        #for image in path:
            #url_image.append(image["items"][0]["items"][0]["body"]["id"])
    else:
        print("Le traitement de ce type de manifest IIIF n'a pas été implémenté dans ce code. ")
        #reponse = input("Souhaitez-vous l'implémenter vous-même ? Si oui, tapez 'o', sinon le programme s'arrêtera.")
        #if reponse == "o":
            #print("Rendez-vous dans le fichier fonctions_generales/récupération_données_manifest.py")
            #print("Cliquez sur 'Ctrl+C' pour finir le programme.")
        #else:
            #sys.exit("Le programme a été arrếté.")


    return titre, annee, auteur, auteur_nom, id_facsimile, notice_cat, url_image
