#!/usr/bin/env python
"""
get_pubs.py

Report on publications in VIVO data via SPARQL queries
 Version 0.1.0 2017-02-22
    - stubbed out using vivo sparql api using python requests lib
    - using the local vagrant
    - requires using the web interface to login and make a user called
      sparql@vivo.shcool.edu and making them an admin

"""
__author__ = "Christopher P. Barnes"
__copyright__ = "Copyright 2017, Christopher P. Barnes"
__license__ = "BSD 2-Clause"
__version__ = "0.1.0"
__email__ = "senrabc@gmail.com"
__status__ = "Development"
import requests
import ConfigParser
import csv

parser = ConfigParser.ConfigParser()
parser.read('config.ini')

#debug = parser.get('vivo_sparql_api', 'debug')
#if debug: print(parser.get('vivo_sparql_api', 'endpoint_url'))


prefixes=' \
PREFIX rdf:      <http://www.w3.org/1999/02/22-rdf-syntax-ns#> \
PREFIX rdfs:     <http://www.w3.org/2000/01/rdf-schema#> \
PREFIX xsd:      <http://www.w3.org/2001/XMLSchema#> \
PREFIX owl:      <http://www.w3.org/2002/07/owl#> \
PREFIX swrl:     <http://www.w3.org/2003/11/swrl#> \
PREFIX swrlb:    <http://www.w3.org/2003/11/swrlb#> \
PREFIX vitro:    <http://vitro.mannlib.cornell.edu/ns/vitro/0.7#> \
PREFIX bibo:     <http://purl.org/ontology/bibo/> \
PREFIX c4o:      <http://purl.org/spar/c4o/> \
PREFIX cito:     <http://purl.org/spar/cito/> \
PREFIX event:    <http://purl.org/NET/c4dm/event.owl#> \
PREFIX fabio:    <http://purl.org/spar/fabio/> \
PREFIX foaf:     <http://xmlns.com/foaf/0.1/> \
PREFIX geo:      <http://aims.fao.org/aos/geopolitical.owl#> \
PREFIX p1:       <http://purl.org/dc/elements/1.1/> \
PREFIX p2:       <http://purl.org/dc/terms/> \
PREFIX obo:      <http://purl.obolibrary.org/obo/> \
PREFIX ocrer:    <http://purl.org/net/OCRe/research.owl#> \
PREFIX ocresd:   <http://purl.org/net/OCRe/study_design.owl#> \
PREFIX p3:       <http://vivoweb.org/ontology/provenance-support#> \
PREFIX skos:     <http://www.w3.org/2004/02/skos/core#> \
PREFIX ufVivo:   <http://vivo.ufl.edu/ontology/vivo-ufl/> \
PREFIX vcard:    <http://www.w3.org/2006/vcard/ns#> \
PREFIX vitro:    <http://vitro.mannlib.cornell.edu/ns/vitro/public#> \
PREFIX vivo:     <http://vivoweb.org/ontology/core#> \
PREFIX scires:   <http://vivoweb.org/ontology/scientific-research#> \
'

#sparql_query = prefixes + 'SELECT ?geoLocation ?label WHERE{?geoLocation rdf:type vivo:GeographicLocation OPTIONAL { ?geoLocation rdfs:label ?label } } LIMIT 20'

# SELECT  ?author ?article ?articleLabel ?venue ?venueLabel ?datetime  ?pmid
# WHERE
# {
# ?author a ufVivo:UFEntity .
# ?author ufVivo:gatorlink ?gatorlink .
# ?author obo:ARG_2000028 ?vcard .
# ?author vivo:relatedBy ?authorship .
# ?authorship a vivo:Authorship .
# ?authorship vivo:relates ?article .
# ?article a bibo:AcademicArticle .
# ?article rdfs:label ?articleLabel .
# ?venue vivo:publicationVenueFor ?article .
# ?venue  rdfs:label ?venueLabel .
# ?article vivo:dateTimeValue ?dateTimeValue .
# ?dateTimeValue vivo:dateTime ?datetime .
# OPTIONAL {?article bibo:pmid ?pmid }
#
# }


sparql_query = prefixes + ' \
 \
SELECT ?gatorlink ?author ?fName ?lName ?article \
?article_label ?journal_uri ?journal_label ?pub_date ?pubmed_id \
WHERE \
{ \
?author a ufVivo:UFEntity . \
?author ufVivo:gatorlink ?gatorlink . \
?author obo:ARG_2000028 ?vcard . \
?vcard a vcard:Individual . \
?vcard vcard:hasName ?name . \
?name a vcard:Name . \
?name vcard:givenName ?fName; \
vcard:familyName ?lName . \
?author vivo:relatedBy ?authorship . \
?authorship a vivo:Authorship . \
?authorship vivo:relates ?article . \
?article a bibo:AcademicArticle . \
?article rdfs:label ?article_label . \
?journal_uri vivo:publicationVenueFor ?article . \
?journal_uri  rdfs:label ?journal_label . \
?article vivo:dateTimeValue ?dateTimeValue . \
?dateTimeValue vivo:dateTime ?pub_date . \
OPTIONAL {?article bibo:pmid ?pubmed_id } \
\
} \
\
LIMIT 20 \
\
'
# limit needs to be changed to 500000 for full run. Don't ask me why this works
# it just works better than with no LIMIT which will sometimes run forever.



#endpoint_url = 'https://vivo.ufl.edu/vivo/api/sparqlQuery'
endpoint_url = parser.get('vivo_sparql_api', 'endpoint_url')
#Auth credentials
email=parser.get('vivo_sparql_api', 'username')
password=parser.get('vivo_sparql_api', 'password')


#result_format options for VIVO sparql api
# result_format=text/plain
result_format='text/csv'
# result_format=text/tab-separated-values
# result_format=application/sparql-results+xml
# result_format=application/sparql-results+json
#result_format = 'application/sparql-results+json'



headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19', 'Accept' : result_format }

# requests lib ref: http://docs.python-requests.org/en/master/user/quickstart/#make-a-request

#payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
payload = {'email': email, 'password': password, 'query': sparql_query}

#print(payload)

#if debug: print(email,password, endpoint_url)
r = requests.get(endpoint_url, headers=headers, params=payload)


#if debug: print(r.text)
#output the results
print(r.text)



# data = r.json()['results']
#
# with open("pubs.csv", "wb") as csvfile:
#     f = csv.writer(csvfile)
#     f.writerow(["author", "article","articleLabel","venue","venueLabel","dateTime"]) # write the headers
#     for elem in data:
#         #f.writerow([elem["author"], elem["article"],elem["articleLabel"], \
#         #elem["venue"],elem["venueLabel"],elem["dateTime"]])
#         f.writerow([elem[0], elem[1],elem[2], \
#         elem[3],elem[4],elem[5]])
