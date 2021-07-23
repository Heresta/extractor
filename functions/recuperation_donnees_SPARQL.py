from SPARQLWrapper import SPARQLWrapper, JSON


def recup_data_sparql(ark):
    """
    Recovers information thanks to a SPARQL request from data.bnf.fr thanks to an ark, which
    is the id in gallica.bnf.fr.
    :param ark: str
        Id from gallica.bnf.fr which is added in the request.
    :return: json
        JSON file with all the informations from the request.
    """
    # indicates the link to make SPARQL request in data.bnf.fr database
    sparql = SPARQLWrapper("http://data.bnf.fr/sparql")
    # the request
    sparql.setQuery("""PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                       PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
                       PREFIX dcterms: <http://purl.org/dc/terms/>
                       PREFIX rdam: <http://rdaregistry.info/Elements/m/>
                       PREFIX owl: <http://www.w3.org/2002/07/owl#>
                       PREFIX rdarelationships: <http://rdvocab.info/RDARelationshipsWEMI/>
                       PREFIX rdagroup1elements: <http://rdvocab.info/Elements/>
                       PREFIX marcrel: <http://id.loc.gov/vocabulary/relators/>
                       PREFIX isni: <http://isni.org/ontology#>
                       SELECT ?titre ?author ?name_author ?publication_place ?publisher_name 
                       ?publication_date ?isniAuteur ?sameas
                       WHERE {
                       ?manifestation <http://rdvocab.info/RDARelationshipsWEMI/electronicReproduction> <https://gallica.bnf.fr/ark:/12148/""" + ark + """>.
                       ?manifestation dcterms:title ?titre;
                       <http://rdvocab.info/RDARelationshipsWEMI/expressionManifested> ?expression.
                       OPTIONAL {?manifestation rdagroup1elements:publishersName ?publisher_name}.
                       OPTIONAL {?manifestation rdagroup1elements:placeOfPublication ?publication_place}.
                       ?manifestation dcterms:date ?publication_date.
                       OPTIONAL {?expression marcrel:aut ?author.
                       ?auteurConcept foaf:focus ?author.
                       ?auteurConcept owl:sameAs ?sameas FILTER(contains(str(?sameas), 'biblissima')).
                       ?auteurConcept isni:identifierValid ?isniAuteur.
                           ?auteurConcept skos:prefLabel ?name_author}.
                       }"""
                    )

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results

