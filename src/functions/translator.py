# -*- coding: utf-8 -*-
from googletrans import Translator
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import SKOS, DC, RDFS


class RDFTranslator:

    def __init__(self, inputfile, source, destination):
        self.g = Graph().parse(inputfile)
        self.translator = Translator()
        self.source = source
        self.destination = destination

    def processrdf(self):
        for subj, pred, obj in self.g.triples((None, SKOS.prefLabel, None)):
            if (subj, pred, obj) not in self.g:
                raise Exception("It better be!")
            print(" ------------------------------------------------------------------------- ")
            print("Translating \"" + obj + "\" from " + self.source + " to " + self.destination)
            translatedobject = Literal(self.translatestring(obj), lang='en')
            print("Got translation: ")
            print(translatedobject)
            print(" ------------------------------------------------------------------------- ")
            self.g.add((subj, SKOS['prefLabel'], translatedobject))
            self.g.add((subj, RDFS['label'], translatedobject))
            self.g.add((subj, RDFS['label'], obj))

        for subj, pred, obj in self.g.triples((None, SKOS.note, None)):
            if (subj, pred, obj) not in self.g:
                raise Exception("It better be!")
            print(" ------------------------------------------------------------------------- ")
            print("Translating \"" + obj + "\" from " + self.source + " to " + self.destination)
            translatedobject = Literal(self.translatestring(obj), lang='en')
            print("Got translation: ")
            print(translatedobject)
            print(" ------------------------------------------------------------------------- ")
            self.g.add((subj, SKOS['note'], translatedobject))

        return self.g

    def capitalizenames(self, language):
        qres = self.g.query(
            """SELECT ?label
                WHERE {
                    ?s ?p ?label
                    FILTER langMatches( lang(?label), "en" )
                }"""
        )
        for row in qres:
            print(row.label)
        # for s, p, o in self.g:
        #     if not (s, p, o) in self.g:
        #         raise Exception("Iterator / Container Protocols are Broken!!")
        #     if p.__str__() == 'http://www.w3.org/2004/02/skos/core#prefLabel':
        #         print("SUBJECT")
        #         print(s)
        #         print("PREDICATE")
        #         print(p)
        #         print("OBJECT")
        #         print(o)


    def translatestring(self, inputstring):
        returnedstring = ""
        translations = self.translator.translate(inputstring, dest=self.destination, src=self.source)
        returnedstring = self.capitalizestring(translations)
        return returnedstring

    def capitalizestring(self, inputstring):
        returnedstring = ""

        if inputstring.text.find(",") > -1:
            returnedstring = inputstring.text.title()
        else:
            returnedstring = inputstring.text.capitalize()

        return returnedstring
