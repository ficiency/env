# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from googlesearch import search
import random
import requests
from googletrans import Translator
import re
from iacleaner import cleaner
import sys
#import concurrent.futures
#from threadings import adriano
import json

def calculate_mode(information):
    diccio = {}
    translater = Translator()
    print("merlin1")

    if information['espa'] != '' and information['lang'] != information['espa']:
        out = translater.translate(information['query'], dest="es")
        print("traduciendo a español...")
        marco = out.text
    elif information['espa'] != '' and information['lang'] == information['espa']:
        marco = information['query']

    if information['engl'] != '' and information['lang'] != information['engl']:
        out = translater.translate(information['query'], dest="en")
        print("traduciendo a ingles...")
        marco = out.text
    elif information['engl'] != '' and information['lang'] == information['engl']:
        marco = information['query']
    
    query_strip = marco
    query_list = query_strip.split(',')

    if information['btnradio'] != '':
        number_p = int(information['btnradio'])

    elif information['pages'] != '':
        number_p = int(information['pages'])

    pages = int(3875*number_p)
    words_per_query = int(pages/int(len(query_list)))
    #print("{} characters in total, then {} characters per page, in merlin2 station".format(words, words_per_query))

    '''
    with concurrent.futures.ThreadPoolExecutor() as executor:
        querys = []
        for query in query_list:
            macron = query + "," + "{}" + "," +information["engl"] + "," + information["espa"]
            querys.append(macron.format(int(words_per_query)))
        print(querys)
        results = executor.map(adriano, querys)
        links = []
        total_accuracy = float()
        texts = ""
        count = 0   
        for result in results:
            print("Terminamos thread...")
            (text, accuracy, references) = result
            texts += str(text)
            total_accuracy += (accuracy*100)
            count += 1
            links.extend(references) 

        average_accuracy = float(total_accuracy/count)
        #print(texts, average_accuracy, links)
        return texts, average_accuracy, links
        '''        

    try:
        for i in query_list:
            diccio[str(i)] = dict()

        
        #unuseful = ["autor", "author", "imagen","figura","animación","animacion","Escrito",
		#		"nota","hecho por","contact","contáct","Sigueme","Siguenos","universidad","copy",
		#		"contacta","actividades","educativas","editado","correo","redes sociales",
		#		"comentario","Suscri","e-mail","email","nombre","web","universidad","contacto",
		#		"direccion","@","podcast","interesado","tabla","publicidad", "resumen",".jpg", ".com"]
        
        
        betweenwords = ["\xa0", "r\n", "\n", "\t", "\r", "\x93", "\x94", "\x96", "\x92"]

        blacklist = ["wikipedia","pdf","steren", "youtube", "amazon", "facebook", "ebay", "mercadolibre","#",".png",
				"homedepot","tool","liverpool",
				"walmart","soriana","heb","prize", "netflix","financiero","aliexpress","khanacademy","senado"]
        functional_links = []
        txt = []
        caracteres = 0
        trash = list()
        none_error = list()
        #print("merlin3")

        start = int(random.randint(1,7))
        stop = int(random.randint(15,25))
        for query in diccio:
            for i in search(query, start=start, stop=stop, pause=3):
                diccio[str(query)][str(i)] = str(query)
                for b in blacklist:
                    checkin = re.findall(b, str(i))
                    if len(checkin) > 0:
                        diccio[str(query)].pop(str(i))
        #print("merlin4")

        for query in diccio:
            subcaracteres = 0
            txt.append(query)
            #print("merlin5")
            try:
                for link in diccio[query]:
                    try:
                        response = requests.get(link)
                        #print("merlin6")

                        if response.status_code == 200:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            texts = soup.find_all("p")
                            functional_links.append(str(link))
                            #print("merlin7")

                            for j in range(0, len(texts)):
                                info = texts[j].get_text()
                                txt.append(str(info))
                                #print("merlin8")
                                

                                for x in range(len(betweenwords)):
                                    if betweenwords[x] in txt[-1]:
                                        txt[-1] = txt[-1].replace(betweenwords[x]," ")
                                        trash.append(betweenwords[x])
                                        #print("merlin9")
                                    else:
                                        continue
                        
                                #for key in unuseful:
                                #    if key in txt[-1].lower():
                                #        txt.remove(str(info))
                                #        trash.append(str(info))
                                

                                caracteres += len(info)
                                subcaracteres += len(info)
                                #print("merlin10")
                                if subcaracteres > int(pages/len(diccio)):
                                    #print("merlin11")
                                    break

                            if subcaracteres > int(pages/len(diccio)):
                                #print("merlin12")
                                break

                        if subcaracteres > int(pages/len(diccio)):
                            #print("merlin13")
                            break

                    except:
                        #return "No he podido conectarme: {}".format(link), diccio
                        continue

                if int(caracteres) > int(pages):
                    #print("merlin14")
                    break

                elif int(subcaracteres) > int(pages/len(diccio)):
                    #print("merlin15")
                    continue

            except:
                none_error.append(query)
                print(none_error)
                continue

        if caracteres > pages:
            print("kennedy")
            if information["engl"] != "":
                cache = list()
                for line in txt:
                    n = translater.translate(line, dest="es")
                    cache.append(n.text)
                texts, nontexts, accuracy = cleaner(cache)
                a = str()
                for i in texts:
                    b = translater.translate(i, dest="en")
                    a += b.text
                    a += " "
            else:
                texts, nontexts, accuracy = cleaner(txt)
                a = str()
                for i in texts:
                    a += i
                    a += " "
            
            return a, accuracy, none_error, functional_links

            '''
            if information["espa"] != "":      
                out = translater.translate(a, dest="en")            
            url = "https://rewriter-paraphraser1.p.rapidapi.com/rewrite"
            payload = "text="
            for element in a:
                if element == " ":
                    a = a.replace(element,"%20")

            payload += a
            headers = {
	                "content-type": "application/x-www-form-urlencoded",
	                "X-RapidAPI-Host": "rewriter-paraphraser1.p.rapidapi.com",
	                "X-RapidAPI-Key": "20cc9d01b0msha912bd887f366dfp1d1fd4jsnde1e9afa9aed"
                            }
            try:
                response = requests.request("POST", url, data=payload, headers=headers)
                augusto = json.loads(response.text) 
                return augusto["paraphrase"], accuracy, none_error, functional_links
            except:
                e = sys.exc_info()[1]
                print(e.args[0])
                return "Error !" 
            '''
            #return a, accuracy, none_error, functional_links 
            
    except:
        e = sys.exc_info()[1]
        print(e.args[0])
        return "Error !" 
