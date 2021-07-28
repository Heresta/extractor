# Example

This is an example of result that this program gives.

## Structure

```
├── img
│    └── example.jpg
│ 
├── xml
│     ├── standardisation
│     │     └── example.xml
│     └── transformation_TEI
│           ├── extration_img.xml
│           └── output.xml
└── README.md

```

## Explanation

`img` and `xml` directories are contained in another one called as facsimile id.

In `img` directory there are all images renamed to be more easily linked with corresponding xml file.

In `xml` directory there are two other directories : `standardisation` contains all xml files renamed to be more easily linked with 
corresponding image file and `transformation_TEI` contains two files that are `extration_img.xml` and `ouput.xml`.

`output.xml` is a TEI file that contains all ALTO files as described in main README.

`extration_img.xml` is an optional TEI file that contains all information about images from facsimile tag in TEI output file.
