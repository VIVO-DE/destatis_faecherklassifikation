# -*- coding: utf-8 -*-

from functions.translator import RDFTranslator

rdftranslator = RDFTranslator('../faecherklassifikation.rdf', 'de', 'en')

skosgraph = rdftranslator.processrdf()

print("Serializing graph to XMl/RDF")
with open('../faecherklassifikation_en.rdf', 'w') as file_object:
    file_object.write(skosgraph.serialize(format='xml'))

print("Serializing graph to turtle format")
with open('../faecherklassifikation_en.ttl', 'w') as file_object:
    file_object.write(skosgraph.serialize())

print("Serializing graph to n3 format")
with open('../faecherklassifikation_en.ttl', 'w') as file_object:
    file_object.write(skosgraph.serialize(format="n3"))

