from lxml import etree as ET
import os


def count_words(dossier_resultat_standardisation: str) -> int:
    """
    Counts words in xml ALTO4 files in the directory gave in input. It counts only
    the words that are text data.
    :param dossier_resultat_standardisation: str
        Takes the path towards the files where counting is needed.
    :return: int
        Returns the total of the counting of words for all files in the
        directory.
    """
    mots = []
    for fichier in os.listdir(dossier_resultat_standardisation):
        file = ET.parse(dossier_resultat_standardisation + fichier)
        root4 = file.getroot()
        # move in the file : tag Page
        for Page in root4[2]:
            # tag PrintSpace
            for PrintSpace in Page:
                # tag TextBlock
                for TextBlock in PrintSpace:
                    # tag TextLine
                    for TextLine in TextBlock:
                        if TextLine.tag == "TextLine":
                            # tag String
                            for String in TextLine:
                                if String.tag == "String":
                                    mots.append(String.get("CONTENT"))
    tous = []
    # add one by one the recovered words
    for item in mots:
        mots = item.split()
        tous.append(mots)

    total = 0
    # final count
    for liste in tous:
        calcul = len(liste)
        total += calcul

    return total
