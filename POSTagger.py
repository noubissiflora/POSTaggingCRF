#!/usr/bin/env python
#import nltk
#from nltk.tag import CRFTagger

# -*- coding: utf-8 -*-
# Natural Language Toolkit: Interface to the CRFSuite Tagger
#
# Copyright (C) 2001-2016 NLTK Project
# Author: Long Duong <longdt219@gmail.com>
# URL: <http://nltk.org/>
# For license information, see LICENSE.TXT

"""
A module for POS tagging using CRFSuite of NLTK.tag : realise par fotcheping noubissi flora
"""
from __future__ import absolute_import
from __future__ import unicode_literals


from nltk.tag import CRFTagger

from nltk.corpus import  PlaintextCorpusReader 

import shutil
import sys
import struct
import os
#from test import  DataProcessing

 
def construct_List_data_train( source):
    text=[]
    phrase=[] 
    for ligne in source:
        mots=ligne.split()
        for word in mots:    
            mot=word.split('/')[0]
            tagt=word.split('/')[1]
            phrase.append((mot,tagt))
        if phrase != []:
            text.append(phrase)       
            phrase=[]
    return text
    
def construct_List_data_test( source):
    text=[]
    phrase=[]
    for ligne in source:
        mots=ligne.split()
        for word in mots:    
            mot=word.split('/')[0]   
            phrase.append((mot))
        if phrase != []:
            text.append(phrase)
            phrase=[]
    return text



def construct_data (path):
    
   # path = "/media/flora/Data/NIVEAU5/modelisation_de_pos_tagging/BrownCorpus/brown"
    corpus = path 
    dossierBrown = PlaintextCorpusReader(corpus,'.*')
    l = 0
    train_data=[]
    test_data=[]
    gold_sent=[]
    
    for  filename in dossierBrown.fileids() :
        #print(filename)
         
        if  filename == "README" or filename == "CONTENTS" or filename == "categories.pickle"  or filename == "cats.txt":
                continue
        file = corpus + '/'+filename
        
        #CONTROLER L'INTERVAL DANS LEQUEL DOIVENT SE TROUVER LES FICHIERS NECESSAIRES POUR L'ENTRAINEMENT
        if l <=15 :
              #  print("training")
            source_train = open(file, "r")   
                     #entrainement
            train_data =train_data + construct_List_data_train(source_train)
        
        
        #CONTROLER L'INTERVAL DANS LEQUEL DOIVENT SE TROUVER LES FICHIERS NECESSAIRES POUR LE TEST 
        elif l>15 and l<=20:
            source_test = open(file, "r")
            gold_file= open(file, "r") 
               # print("test")
                    #test du modele
            test_data =test_data + construct_List_data_test(source_test)
            gold_sent =gold_sent + construct_List_data_train(gold_file)
            source_train.close()
            gold_file.close()
            source_test.close()
                
        elif l>20 :
            break
                    
        l=l+1
       
    return train_data, test_data, gold_sent

def stockage_model (model_file, model_text):
      
# CONVERTIR LE FICHIER BINAIRE EN FICHIER TEXTE
    file =open(model_text,"w")
    file_model = open(model_file, "r")
    try:
        s = struct.Struct("<dffflfffffffl") # Binary data format
        while True:
            record = file_model.read(56)
            if len(record) != 56:
                break
 
# DECODAGE DE L'ENREGISTREMENT SITUE DANS LE FICHIER BINAIRE
            p= s.unpack(record) # Decode ("unpack")
           
#STOCKAGE DES POIDS DECODES DANS UN FICHIER TEXTE
            file.write('(')
            for w in p :
                file.write(str(w))
                file.write(',')
            file.write(')')
            file.newlines
            
    except IOError:
        # Your error handling here
        # Nothing for this example
            pass
    finally:
        file_model.close()
        file.close()
   # print("stop")
    #print(p)
   # print(len(p))
    return file


if __name__ == '__main__':

#INSTANTIER LE MODEL
    ct = CRFTagger()
   
#RECUPERER LE CHEMIN VERS LE CORPUS
    data_path = str(sys.argv[1])
    train_data, test_data, gold_sent = construct_data(data_path) 
    print("training_model....")
   # print(train_data)
    #model.crf.tagger
    
#ENTRAINER LE MODELE ET LE STOCKER DANS UN FICHIER
    if sys.argv[2].lower() == "train":
              
        ct.train(train_data,'model')          
        print("model_trained")
       
    #STOCKAGE DU MODELE DANS UN FICHIER TEXXTE
        print("stockage du modele dans un fichier texte")
        ficher2 =stockage_model("model", "modele")
    else:
        #VERIFIER SI LE MODEL FILE EXISTE DEJA
        if os.path.isfile("./model"): 
            ct.set_model_file('model')
            
         #SINON RETOURNER UN MESSAGE D'ERREUR  
        else:
            print("Aucun modele entrainr pour le moment. Preciser 'train' comme second arg pour entrainer le modele")
            sys.exit(0) 
#TEST DU MODELE
   # ct1 = CRFTagger()
    ct.set_model_file('model')
    print("tagging_texte....")
    test=ct.tag_sents(test_data)
    print("texte_tagged")
   # print(test_data)
    #print("texte_tagged")
   # print(test)
    
    
    
#CALCULER "accuracy" 
    print("precision...")
    #print(gold_sent)
    #ct = CRFTagger() 
    #ct.set_model_file('model.crf.tagger')
    print("precision=  ", ct.evaluate(gold_sent))
    
   # source_gold.close()
   
    
    
    
    
    
    
    
    