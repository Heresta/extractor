# Extractor - From ALTO to TEI

Python script for transformation ALTO4 files in XML-TEI files.

<b>Warning</b>: For now, this pipeline only works with
* files annotated with the [SegMonto controlled vocabulary](https://github.com/SegmOnto)
* ALTO files created with [eScriptorium](https://gitlab.inria.fr/scripta/escriptorium). Data and models for the latter can be found in the [OCR17plus](https://github.com/e-ditiones/OCR17plus) repo. 
* Prints found on [Gallica](https://gallica.bnf.fr) and their IIIF manifest.

## Structure of the repository

```
├── functions
│     ├── cleaned_file.py
│     ├── count_illustration.py
│     ├── count_words.py
│     ├── creation_intermediaire.py
│     ├── extraction_img.py
│     ├── geonames.json
│     ├── licences.json
│     ├── recuperation_donnees_SPARQL.py
│     ├── récupération_données_manifest.py
│     ├── sorted.py
│     ├── Transkribus_ABBYY_native.py
│     └── __init__.py
│ 
├── ODD
│     ├── ODD.xml
│     └── out
│           └── ODD.rng
├── example
│     ├── xml
│     │     ├── ALTOs
│     │     │      ├──author_title_date_ID_folio.xml
│     │     │      ├──…
│     │     │      └── author_title_date_ID_folio.xml
│     │     └── TEI
│     │            ├── author_title_date_ID.xml
│     │            ├── author_title_date_ID_decorations.xml
│     │            └── extraction_img.py
│     ├── img
│     │     ├──author_title_date_ID_folio.jpg
│     │     ├──…
│     │     └── author_title_date_ID_folio.jpg
│     └── README.md
├── alto4_into_TEI.py
├── strings_checking.py
├── count_illustration.py
└── README.md

```
With ``alto4_into_TEI.py`` it is possible to transform XML ALTO4 files from [eScriptorium](http://traces6.paris.inria.fr/) 
into XML-TEI files. 

The directory ``functions`` contains several python files used in ``alto4_into_TEI.py`. They are all differents steps of it.

``strings_checking.py`` is a script that allows corrections of segmentation mistakes.

In ``ODD`` directory can be found an ODD based on the work of Alexandre Bartz and Simon Gabay, and especially the first of three 
levels of transcription in XML-TEI (_i.e._ [E-ditiones/ODD17](https://github.com/e-ditiones/ODD17)).

`example` directory contains an example of result that this program gives.

## How to
### Install

Copy those commands in a terminal.

```console
git clone https://github.com/e-ditiones/extractor
cd extractor
pip install virtualenv
virtualenv env
source env/bin/activate
pip install -r requirements.txt
```

### Run

To use this script, you first need to prepare some data on eScriptorium. This script works with IIIF digitization of 17<sup>th</sup>
century books on [Gallica](gallica.bnf.fr). Only the manifest url is needed. Then we recommend to use a segmentation and a transcription
model that can be found on [datasetsOCRSegmenter17 repo](https://github.com/Heresta/datasetsOCRSegmenter17/Model). Kraken could be used 
directly with command line, but we recommand using eScriptorium because it is easier to chose which image to segment and transcribe.

All data obtained after segmentation and transcription needs to be corrected, especially transcription.

When data is clean, you must download it : we need ALTO4 files and the corresponding images in two separate folders.

Control the consistency of data thanks to ``strings_checking.py`` script with a command line like this :

``python strings_checking.py PATH_TO_THE_ALTO4_DIRECTORY``

In case you encountered a problem, correct lines or zones errors.

After all of that, ``alto4_into_TEI.py`` script can be used to transform the data with a command line like this :

``python alto4_into_TEI.py 'IIIF_GALLICA_ARK' 'NAME_SURNAME_ORCID' 'PUBLISHER' 'LINK_TO_PUBLIHER_INFO' 'AVAILABILITY' -e`` 

* `IIIF_GALLICA_ARK`: provide the qualifier (`btv1b86262420` in `ark:/12148/btv1b86262420`)
* `'NAME_SURNAME_ORCID'` must be written with underscores instead of blanks to be correctly treated. And if you do not have an ORCID, use 'NAME_SURNAME_'.
* `'PUBLISHER'` is the name of the project publishing the document.
* `'LINK_TO_PUBLIHER_INFO'` is the url of the project.
* `-a 'AVAILABILTY'`, it is a mandatory argument with specific entries. They are 'cc by', 'cc by-sa', 'cc by-nb',
 'cc by-nc', 'cc by-nc-sa' or 'cc by-nc-nd' (cf. [creattive commons licences](https://creativecommons.org)).
* `-e` is an option that gives a extra xml file with the list of all "Decoration", "Figure" and "DropCapital" zones and their
IIIF link.



Then the script will ask the path to ALTO4 files and images directory.

Finally, it will return a directory in the one of the script. It will follow this structure :

```
├── xml
│     ├── ALTOs
│     │      ├──author_title_date_ID_folio.xml
│     │      ├──…
│     │      └── author_title_date_ID_folio.xml
│     └── TEI
│            ├── author_title_date_ID.xml
│            ├── author_title_date_ID_decorations.xml
│            └── extraction_img.py
└── img
      ├──author_title_date_ID_folio.jpg
      ├──…
      └── author_title_date_ID_folio.jpg
```

1. ALTO files (one per page in the original document) are cleaned and renamed
2. 2 TEI files are created:
 * one complete
 * one with just the decorations, only if the `-e` parameter has been used
3. Images are renamed, with the same name that the ALTO files

## Thanks to
Thanks to Simon Gabay, Juliette Janes and Alexandre Bartz for their help and work.

## Contacts
Claire Jahan : claire.jahan[at]chartes.psl.eu

Simon Gabay : Simon.Gabay[at]unige.ch

## Cite this dataset
Claire Jahan and Simon Gabay, _Extractor - From ALTO to TEI_, 2021, Paris/Geneva: ENS Paris/UniGE, https://github.com/e-ditiones/extractor.

## Licence
Data is CC-BY, except images which come from Gallica (cf. [conditions d'utilisation](https://gallica.bnf.fr/edit/und/conditions-dutilisation-des-contenus-de-gallica)).

![68747470733a2f2f692e6372656174697665636f6d6d6f6e732e6f72672f6c2f62792f322e302f38387833312e706e67](https://user-images.githubusercontent.com/56683417/115237678-2150d080-a11d-11eb-903e-5a26587e12e1.png)
