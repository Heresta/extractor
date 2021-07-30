import click
from lxml import etree as ET
import os
import re

@click.command("check_strings")
@click.argument("dossier")
def check_strings(dossier):
    for directory in os.listdir(dossier):
        file = ET.parse(dossier + directory)
        root = file.getroot()
        strings = ET.tostring(root, encoding='unicode')
        strings = strings.split("\n")
        dropcapital = root[1][4].get("ID")
        numbering = root[1][8].get("ID")
        runningtitle = root[1][9].get("ID")
        signatures = root[1][11].get("ID")
        layout = root[2]
        final = ""
        for page in layout:
            for printspace in page:
                for textblock in printspace:
                    if textblock.get("TAGREFS") == None:
                        print("Le block " + textblock.get("ID") + " du fichier " + directory + " n'a pas de "
                                                                                               "type. Ce block"
                                                                                               " est à complét"
                                                                                               "er (ajouter "
                                                                                               "un TAGREFS) "
                                                                                               "ou à supprimer.")
                    elif textblock.get("TAGREFS") == "BT":
                        print("Le block " + textblock.get("ID") + " du fichier " + directory + " a un attribut "
                                                                                               "TAGREFS incomplet. "
                                                                                               "Il faut le compléter.")
                    elif textblock.get("ID") == "eSc_dummyblock_":
                        print("Le block " + textblock.get("ID") + " du fichier " + directory + " n'est pas un block "
                                                                                               "correct. Il faut le "
                                                                                               "supprimer et ajouter "
                                                                                               "ce qu'il contient dans"
                                                                                               "le bon block.")
                    elif int(textblock.get('WIDTH')) * int(textblock.get("HEIGHT")) < 101:
                        print("Le block " + textblock.get("ID") + " du fichier " + directory + "est à effacer, puisque "
                                                                                               "trop petit.")
                for textblock in printspace:
                    if textblock.get("ID") == dropcapital:
                        if textblock[1] == "{http://www.loc.gov/standards/alto/ns-v4#}TextLine":
                            pass
                        else:
                            print("Le block " + textblock.get("ID") + " du fichier " + directory + "est à remplir d'une"
                                                                                                   " textline correspon"
                                                                                                   "dante")
                    elif textblock.get("ID") == numbering:
                        if textblock[1] == "{http://www.loc.gov/standards/alto/ns-v4#}TextLine":
                            pass
                        else:
                            print("Le block " + textblock.get("ID") + " du fichier " + directory + "est à remplir d'une"
                                                                                                   " textline correspon"
                                                                                                   "dante")
                    for textline in textblock:
                        if textline.tag == "{http://www.loc.gov/standards/alto/ns-v4#}TextLine":
                            if textline.get("TAGREFS"):
                                pass
                            else:
                                for string in textline:
                                    if string.tag == "{http://www.loc.gov/standards/alto/ns-v4#}String":
                                        print(directory + " : " + string.get("CONTENT"))
                                        reponse = input("If line type is 'Default', type " + root[1][14].get("ID") + ".\n"
                                                        "If line type is 'DropCapitalLine', type " + root[1][15].get("ID") + ".\n"
                                                        "If line type is 'Interlinear', type " + root[1][16].get("ID") + ".\n"
                                                        "If line type is 'MusicLine', type " + root[1][17].get("ID") + ".\n"
                                                        "If line type is 'Rubric', " + root[1][18].get("ID") + ".\n")
                                        for i in strings:
                                            if textline.get("ID") in i:
                                                propre = re.sub('" BASELINE', '" TAGREFS="' + reponse + '" BASELINE',
                                                                i)
                                                final += propre
                                            else:
                                                final += i
                                with open(dossier + directory, "wb") as f:
                                    f.write(bytes(final, encoding="utf-8"))
    for directory in os.listdir(dossier):
        with open(dossier + directory, "r") as f:
            file = f.read()
            if "</alto><alto" in file:
                propre = re.sub("</alto><alto(.)*", "</alto>", file)
                with open(dossier + directory, "wb") as f:
                    f.write(bytes(propre, encoding="utf-8"))
    for directory in os.listdir(dossier):
        file = ET.parse(dossier + directory)
        root = file.getroot()
        ET.indent(root)
        with open(dossier + directory, "wb") as f:
            f.write(ET.tostring(root, encoding="utf-8"))


if __name__ == "__main__":
    check_strings()

