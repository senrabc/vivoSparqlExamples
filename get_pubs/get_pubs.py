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

parser = ConfigParser.ConfigParser()
parser.read('config.ini')

debug = parser.get('vivo_sparql_api', 'debug')
if debug: print(parser.get('vivo_sparql_api', 'endpoint_url'))


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

sparql_query = prefixes + 'SELECT ?geoLocation ?label WHERE{?geoLocation rdf:type vivo:GeographicLocation OPTIONAL { ?geoLocation rdfs:label ?label } } LIMIT 20'

#endpoint_url = 'https://vivo.ufl.edu/vivo/api/sparqlQuery'
endpoint_url = parser.get('vivo_sparql_api', 'endpoint_url')
#Auth credentials
email=parser.get('vivo_sparql_api', 'username')
password=parser.get('vivo_sparql_api', 'password')


#result_format options for VIVO sparql api
# result_format=text/plain
# result_format=text/csv
# result_format=text/tab-separated-values
# result_format=application/sparql-results+xml
# result_format=application/sparql-results+json
result_format = 'application/sparql-results+json'



headers = {'user-agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.19 (KHTML, like Gecko) Chrome/1.0.154.53 Safari/525.19', 'Accept' : result_format }

# requests lib ref: http://docs.python-requests.org/en/master/user/quickstart/#make-a-request

#payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
payload = {'email': email, 'password': password, 'query': sparql_query}

#test query
#r = requests.get('http://localhost:8080/vivo/api/sparqlQuery?email=sparql@school.edu&password=password&query=PREFIX+rdf%3A++++++%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0APREFIX+rdfs%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+xsd%3A++++++%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+owl%3A++++++%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0D%0APREFIX+swrl%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F2003%2F11%2Fswrl%23%3E%0D%0APREFIX+swrlb%3A++++%3Chttp%3A%2F%2Fwww.w3.org%2F2003%2F11%2Fswrlb%23%3E%0D%0APREFIX+vitro%3A++++%3Chttp%3A%2F%2Fvitro.mannlib.cornell.edu%2Fns%2Fvitro%2F0.7%23%3E%0D%0APREFIX+bibo%3A+++++%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fbibo%2F%3E%0D%0APREFIX+c4o%3A++++++%3Chttp%3A%2F%2Fpurl.org%2Fspar%2Fc4o%2F%3E%0D%0APREFIX+cito%3A+++++%3Chttp%3A%2F%2Fpurl.org%2Fspar%2Fcito%2F%3E%0D%0APREFIX+event%3A++++%3Chttp%3A%2F%2Fpurl.org%2FNET%2Fc4dm%2Fevent.owl%23%3E%0D%0APREFIX+fabio%3A++++%3Chttp%3A%2F%2Fpurl.org%2Fspar%2Ffabio%2F%3E%0D%0APREFIX+foaf%3A+++++%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2F%3E%0D%0APREFIX+geo%3A++++++%3Chttp%3A%2F%2Faims.fao.org%2Faos%2Fgeopolitical.owl%23%3E%0D%0APREFIX+p1%3A+++++++%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2F%3E%0D%0APREFIX+p2%3A+++++++%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Fterms%2F%3E%0D%0APREFIX+obo%3A++++++%3Chttp%3A%2F%2Fpurl.obolibrary.org%2Fobo%2F%3E%0D%0APREFIX+ocrer%3A++++%3Chttp%3A%2F%2Fpurl.org%2Fnet%2FOCRe%2Fresearch.owl%23%3E%0D%0APREFIX+ocresd%3A+++%3Chttp%3A%2F%2Fpurl.org%2Fnet%2FOCRe%2Fstudy_design.owl%23%3E%0D%0APREFIX+p3%3A+++++++%3Chttp%3A%2F%2Fvivoweb.org%2Fontology%2Fprovenance-support%23%3E%0D%0APREFIX+skos%3A+++++%3Chttp%3A%2F%2Fwww.w3.org%2F2004%2F02%2Fskos%2Fcore%23%3E%0D%0APREFIX+ufVivo%3A+++%3Chttp%3A%2F%2Fvivo.ufl.edu%2Fontology%2Fvivo-ufl%2F%3E%0D%0APREFIX+vcard%3A++++%3Chttp%3A%2F%2Fwww.w3.org%2F2006%2Fvcard%2Fns%23%3E%0D%0APREFIX+vitro%3A++++%3Chttp%3A%2F%2Fvitro.mannlib.cornell.edu%2Fns%2Fvitro%2Fpublic%23%3E%0D%0APREFIX+vivo%3A+++++%3Chttp%3A%2F%2Fvivoweb.org%2Fontology%2Fcore%23%3E%0D%0APREFIX+scires%3A+++%3Chttp%3A%2F%2Fvivoweb.org%2Fontology%2Fscientific-research%23%3E%0D%0A%0D%0A%23%0D%0A%23+This+example+query+gets+20+geographic+locations%0D%0A%23+and+%28if+available%29+their+labels%0D%0A%23%0D%0ASELECT+%3FgeoLocation+%3Flabel%0D%0AWHERE%0D%0A%7B%0D%0A++++++%3FgeoLocation+rdf%3Atype+vivo%3AGeographicLocation%0D%0A++++++OPTIONAL+%7B+%3FgeoLocation+rdfs%3Alabel+%3Flabel+%7D+%0D%0A%7D%0D%0ALIMIT+20%0D%0A%0D%0A++++++++++++')
if debug: print(email,password, endpoint_url)
r = requests.get(endpoint_url, headers=headers, params=payload)


if debug: print(r.text)
