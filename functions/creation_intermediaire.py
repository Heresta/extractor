import os
import errno

def creation_interm():
    """
    Creates all of the median directories to store some metadata
    """
    intermediaire = "./intermediaire/"
    intermediaire_copie_xml = "./intermediaire/copie_fichier_xml/"
    intermediaire_copie_img = "./intermediaire/copie_fichier_img/"
    intermediaire_post_copie = "./intermediaire/post_copie_fichier_xml/"
    intermediaire_transformation_xml = "./intermediaire/intermediaire/"

    # si le dossier intermédiare n'existe pas pour les fichiers xml, on le crée, sinon, on ne fait rien
    if not os.path.exists(os.path.dirname(intermediaire)):
        try:
            os.makedirs(os.path.dirname(intermediaire))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # si le dossier copie_fichier_xml n'existe pas pour les fichiers xml, on le crée, sinon, on ne fait rien
    if not os.path.exists(os.path.dirname(intermediaire_copie_xml)):
        try:
            os.makedirs(os.path.dirname(intermediaire_copie_xml))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # si le dossier copie_fichier_img n'existe pas pour les fichiers xml, on le crée, sinon, on ne fait rien
    if not os.path.exists(os.path.dirname(intermediaire_copie_img)):
        try:
            os.makedirs(os.path.dirname(intermediaire_copie_img))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # si le dossier post_copie_fichier_xml n'existe pas pour les fichiers xml, on le crée, sinon, on ne fait rien
    if not os.path.exists(os.path.dirname(intermediaire_post_copie)):
        try:
            os.makedirs(os.path.dirname(intermediaire_post_copie))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # si le dossier intermédiaire n'existe pas pour les fichiers xml, on le crée, sinon, on ne fait rien
    if not os.path.exists(os.path.dirname(intermediaire_transformation_xml)):
        try:
            os.makedirs(os.path.dirname(intermediaire_transformation_xml))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise
