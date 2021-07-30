# Example

This is an example of result that this program gives.

## Structure

```
├── xml
│     ├── ALTOs
│     │      ├──author_title_date_ID_folio.xml
│     │      ├──…
│     │      └── author_title_date_ID_folio.xml
│     └── TEI
│            ├── author_title_date_ID.xml
│            └── author_title_date_ID_decorations.xml
├── img
│     ├──author_title_date_ID_folio.jpg
│     ├──…
│     └── author_title_date_ID_folio.jpg
└── README.md

```

## Explanation

`img` and `xml` directories are contained in another one called as facsimile id.

In `img` directory there are all images renamed to be more easily linked with corresponding xml file.

In `xml` directory there are two other directories : `ALTOS` contains all xml files renamed to be more easily linked with 
corresponding image file and `TEI` contains two files that are `author_title_date_ID_decorations.xml` and `author_title_date_ID.xml`.

`author_title_date_ID.xml` is a TEI file that contains all ALTO files as described in main README.

`author_title_date_ID_decorations.xml` is an optional TEI file that contains all information about images from facsimile tag in TEI output file.
