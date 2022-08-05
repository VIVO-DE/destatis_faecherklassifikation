# -*- coding: utf-8 -*-
import json

from googletrans import Translator
from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import SKOS, DC, RDFS
import re


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
        g2 = Graph()
        names = self.fetchcapitalizednames(language)

        for subj, pred, obj in self.g.triples((None, SKOS.prefLabel, None)):
            if (subj, pred, obj) not in self.g:
                raise Exception("It better be!")
            print(" ------------------------------------------------------------------------- ")
            print(" SETTING " + names[subj][language] + " IN LANGUAGE " + language + " FOR ")
            print(subj)
            self.g.remove((subj, SKOS.prefLabel, obj))
            self.g.remove((subj, RDFS.label, obj))
            self.g.add((subj, SKOS.prefLabel, names[subj][language]))
            self.g.add((subj, RDFS.label, names[subj][language]))

            self.g.add((subj, RDFS.label, names[subj][obj.language]))
            self.g.add((subj, SKOS.prefLabel, names[subj][obj.language]))
            print(" SETTING " + names[subj][obj.language] + " IN LANGUAGE " + obj.language + " FOR ")
            print(subj)
            print(" ------------------------------------------------------------------------- ")

        return self.g

    def fetchcapitalizednames(self, language):
        names = {}
        for subj, pred, obj in self.g.triples((None, SKOS.prefLabel, None)):
            if (subj, pred, obj) not in self.g:
                raise Exception("It better be!")
            if subj not in names:
                names[subj] = {}
            if obj is not None and obj.language == language:
                capitalizedpreflabel = Literal(self.capitalizestring(obj), lang=language)
                names[subj][language] = capitalizedpreflabel
            elif obj is not None and obj.language != language:
                names[subj][obj.language] = Literal(obj, obj.language)
        return names

    def translatestring(self, inputstring):
        translations = self.translator.translate(inputstring, dest=self.destination, src=self.source)
        returnedstring = self.capitalizestring(translations.text)
        return returnedstring

    def capitalizestring(self, inputstring):
        inputstring = self.clean_data(inputstring)
        inputstring = re.sub(" {2,}", " ", inputstring.strip())
        return ' '.join([s[0].upper() + s[1:] for s in inputstring.split(' ')])

    def clean_data(self, data):
        return data.replace('\u200c', '')
