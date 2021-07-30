import click
import os
import errno
from functions.recuperation_donnees_SPARQL import recup_data_sparql
from functions.Transkribus_ABBYY_native import tes
from functions.recuperation_donnees_manifest import recuperation_donnees_manifest
from functions.extraction_img import extraction_image
from functions.creation_intermediaire import creation_interm
from functions.cleaned_file import clean_file


@click.command("transformation")
@click.argument("ark", type=str)
@click.argument("editeur", type=str)
@click.argument("edition", type=str)
@click.argument("url_edition", type=str)
@click.option("-st", "--segmtrans", "segmentationTranscription", help="Si on souhaite faire automatiquement la "
                                                                       "segmentation et la transcription",
              is_flag=True, default=False)
@click.option("-a", "--availability", type=click.Choice(['cc by', 'cc by-sa', 'cc by-nb', 'cc by-nc', 'cc by-nc-sa',
                                                         'cc by-nc-nd'], case_sensitive=False), required=True,
              help="Indiquer la licence Creative Commons choisie : 'cc by', 'cc by-sa', 'cc by-nb','cc by-nc', "
                   "'cc by-nc-sa' ou 'cc by-nc-nd'")
@click.option("-e", "--extraction", "extraction_img", help="""rend une liste en format XML-TEI des 
                                                illustrations repérées comme Decoration par le 
                                                segmenteur""", is_flag=True, default=False)
def transformation(ark, editeur, edition, url_edition, segmentationTranscription, availability,
                   extraction_img):
    # création des dossiers intermédiaires
    creation_interm()

    # récupération des images IIIF sur Gallica
    infos = recuperation_donnees_manifest('https://gallica.bnf.fr/iiif/ark:/12148/' + ark + '/manifest.json/')
    titre = infos[0]
    annee = infos[1]
    auteur = infos[2]
    nom_auteur = infos[3]
    id_facsimile = infos[4]
    notice_cat = infos[5]
    url_images = infos[6]

    # récupération infos SPARQL
    infos_sparql = recup_data_sparql(ark)
    if infos_sparql["results"]["bindings"]:
        if infos_sparql["results"]["bindings"][0].get("publication_place"):
            ville_edition = infos_sparql["results"]["bindings"][0]["publication_place"]["value"]
        else:
            ville_edition = None
        if infos_sparql["results"]["bindings"][0].get("publisher_name"):
            editeur_historique = infos_sparql["results"]["bindings"][0]["publisher_name"]["value"]
        else:
            editeur_historique = None
        if infos_sparql["results"]["bindings"][0].get("isniAuteur"):
            isniauteur = infos_sparql["results"]["bindings"][0]["isniAuteur"]["value"]
        else:
            isniauteur = None
    else:
        ville_edition = None
        editeur_historique = None
        isniauteur = None

    # récupération de chemin de fichiers ALTO en export d'eScriptorium
    output = input("Entrez le chemin du dossier ALTO4 en export d'eScriptorium : ")

    # récupération de chemin de fichiers ALTO en export d'eScriptorium
    output_img = input("Entrez le chemin du dossier image en export d'eScriptorium : ")

    # fonction de transformation
    doc_final = tes(output, output_img, editeur, edition, url_edition, availability, isniauteur, editeur_historique,
                    ville_edition, titre, annee, auteur, nom_auteur, id_facsimile, notice_cat, ark, url_images)

    # fonction de récupération de la liste des imprimeurs
    if extraction_img:
        extraction_image(doc_final, titre, editeur, id_facsimile, ark)
        clean_file(doc_final)
    else:
        clean_file(doc_final)


if __name__ == "__main__":
    transformation()
