# transformationTEI17 - Script for information extraction of old French prints from eScriptorium

Python script for transformation ALTO4 files in XML-TEI files depending on a specific ODD.

## Structure

```
├── functions
│     ├── cleaned_file.py
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
│     ├── img
│     │     └── example.jpg
│     ├── xml
│     │     ├── standardisation
│     │     │     └── example.xml
│     │     └── transformation_TEI
│     │           ├── extration_img.xml
│     │           └── output.xml
│     └── README.md
├── alto4_into_TEI.py
├── strings_checking.py
├── count_illustration.py
└── README.md

```
With ``alto4_into_TEI.py`` it is possible to transform XML ALTO4 files from [eScriptorium](http://traces6.paris.inria.fr/) 
into XML-TEI files.

<b>Warning</b>: This XSLT is based on files which used a description layout from the [SegMonto](https://github.com/SegmOnto) 
vocabulary in eScriptorium as it is described in [datasetsOCRSegmenter17 repo](https://github.com/Heresta/datasetsOCRSegmenter17). 

The directory ``functions`` contains several python files used in ``alto4_into_TEI.py`. They are all differents steps of it.

``strings_checking.py`` is a script that allows corrections of segmentation mistakes.

In ``ODD`` directory can be found an ODD based on the work of Alexandre Bartz and Simon Gabay, and especially the first of three 
levels of transcription in XML-TEI (_i.e._ [E-ditiones/ODD17](https://github.com/e-ditiones/ODD17)).

``count_illustration.py`` is a script to count pages, decorations, dropcapitals and figures after TEI transformation. It has to be used on 
`extrated_img.xml` and the path to this file has to be indicated directly into the code.

`example` directory contains an example of result that this program gives.

## Installation
### Create a virtul environment (Linux-Ubuntu)
We need to create a virtual environment in which we will be able to use
 Python 3.6.

To do so, in a terminal, we need to type the following command: 

```shell
sudo apt-get install python3 libfreetype6-dev python3-pip python3-virtualenv
```

Then choose a directory where you want register the app and from where you 
will be able to use it. 

In that repository, we need to clone <i>transformationTEI17</i> repository.

This is from this directory that you need to type the following command to 
create the virtual environment :
 
```shell
virtualenv ~/.transformationTEI17 -p python3
```
Then, we need to type the following command:
```shell
source ~/.transformationTEI17/bin/activate
```
This previous command is mandatory to activate the app.

### Packages' installation
In order for this app to be used, we need to install several python packages. 
They are in `requirements.txt` file. You just need to use this command in the
new virtual environment:
```shell
pip install -r requirements.txt
```

This command is for a single use.

## Explanations about transformation's script

To use this script, you first need to prepare some data on eScriptorium. This script works with IIIF digitization of 17<sup>th</sup>
century books on [Gallica](gallica.bnf.fr). Only the manifest url is needed. Then we recommend to use a segmentation and a transcription
model that can be found on [datasetsOCRSegmenter17 repo](https://github.com/Heresta/datasetsOCRSegmenter17/Model). Kraken could be used 
directly with command line, but we recommand using eScriptorium because it is easier to chose which image to segment and transcribe.

All data obtained after segmentation and transcription needs to be corrected, especially transcription.

When data is clean, you must download it : we need ALTO4 files and the corresponding images.

To be sure that data is ready for transformation, we recommand to use ``strings_checking.py`` script with a command line like this :

``python strings_checking.py PATH_TO_THE_ALTO4_DIRECTORY``

If there is no problem, nothing will appear. If there is, you will be able to correct directly the lack of type for lines. Concerning zones
, you will have to correct the file directly by open it.

After all of that, ``alto4_into_TEI.py`` script can be used with a command line like this :

``python alto4_into_TEI.py 'IIIF_GALLICA_ARK' 'NAME_SURNAME_ORCID' 'PUBLISHER' 'LINK_TO_PUBLIHER_INFO' 'AVAILABILITY' -e`` 

<b>WARNING</b> : the argument 'NAME_SURNAME_ORCID' must be written with underscores instead of blanks to be correctly treated. And if there
is no ORCID, it must be written like 'NAME_SURNAME_'.

<b>WARNING</b> : concerning 'AVAILABILTY', it is a mandatory argument with specific entries. They are 'cc by', 'cc by-sa', 'cc by-nb',
 'cc by-nc', 'cc by-nc-sa' or 'cc by-nc-nd', and all correspond to a different type of Common Creative licence.

<b>WARNING</b> : -e is an option that gives a extra xml file with the list of all "Decoration", "Figure" and "DropCapital" zone and their
IIIF link.

Then the script will ask the path to ALTO4 files and images directory.

Finally, it will return a directory in the one of the script. It will follow this structure :

```
├── xml
│     ├── standardisation
│     │      └── all ALTO4 files renamed thanks to a created id of the facsimile and normalized
│     └── transformation_TEI
│            ├── output.xml
│    	     └── extraction_img.py
└── img
      └── all images renamed thanks to a created id of the facsimile
```
  

## Thanks to
Thanks to Simon Gabay, Juliette Janes and Alexandre Bartz for their help and work.

## Contacts
Claire Jahan : claire.jahan[at]chartes.psl.eu

Simon Gabay : Simon.Gabay[at]unige.ch

## Cite this dataset
Claire Jahan and Simon Gabay, _Transformation pipeline for XML-ALTO4 files from eScriptorium_, 2021, Paris: ENS Paris,  https://github.com/Heresta/datasetsOCRSegmenter17.

## Licence
Data is CC-BY, except images which come from Gallica (cf. [conditions d'utilisation](https://gallica.bnf.fr/edit/und/conditions-dutilisation-des-contenus-de-gallica)).

![68747470733a2f2f692e6372656174697665636f6d6d6f6e732e6f72672f6c2f62792f322e302f38387833312e706e67](https://user-images.githubusercontent.com/56683417/115237678-2150d080-a11d-11eb-903e-5a26587e12e1.png)
