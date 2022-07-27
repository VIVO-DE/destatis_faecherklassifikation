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

    def translatestring(self, inputstring):
        returnedstring = ""
        translations = self.translator.translate(inputstring, dest=self.destination, src=self.source)

        if translations.text.find(",") > -1:
            returnedstring = translations.text.title()
        else:
            returnedstring = translations.text.capitalize()

        return returnedstring
