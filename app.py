# -*- coding: utf-8 -*-
import sys
from flask import Flask, request, session
from flask.templating import render_template
from googletrans import Translator
from processing import calculate_mode
import time
import datetime, pytz
print("Hola")
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "asdzxcfghvbnasfgraarasd"

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/contact")
def contact():
    return render_template('index.html')

@app.route("/donate")
def donate():
    return render_template('donate.html')

@app.route("/new")
def new():
    return render_template('new.html')

@app.route("/mse-t", methods=["GET", "POST"])
def mode_page():
    result = ""
    no_content = ''
    pages_problem = ''
    lang_problem = ''
    beaft_doc = "Your document will be here..."
    accuracy = ""
    links_user = ""
    #session.clear()
    print(session)
    time_remaining = ""

    if "user" not in session:
        #session.clear()
        session["user"] = []
        session["tickets"] = int(3)
        session["t1"] = int(1)
        session["counter"] = int(0)
        session["next-date"] = "empty"
        session["current-date"] = "empty"
    
    if session["counter"] != 0:
        if session["tickets"] <= 0:
            session["current-date"] = datetime.datetime.now()
            session["current-date"] = pytz.utc.localize(session["current-date"])
            if session["current-date"] > session["next-date"]:
                session.clear()
                mode_page()
                
            elif session["current-date"] < session["next-date"]:
                time_remaining = str(session["next-date"] - session["current-date"])
                hours_s = time_remaining.split(":")
                hours = f"Refresh timer: {hours_s[0]} hours."
                return render_template("mse-t.html", beaft_doc = beaft_doc, time_remaining = hours)
       
    print("mode_page ROUTE")

    if request.method == "POST":
        print("mode_page POST")
        if request.form.get("action", False) == "Go":
            inicio = time.time()
            print("mode_page GO")
            try:
                answers = request.form
            except:
                pass    

            information = answers.copy()
            information.setdefault('btnradio','')
            information.setdefault('pages','')
            information.setdefault('espa','')
            information.setdefault('engl','')
            information.setdefault('br','off')
            information.setdefault('pt','off')
            information.setdefault('ii','off')
            session["user"] = [information]
            print(session)
            translator = Translator()

            try:
                if information['query'] == '': 
                    no_content = '*Please insert at least one theme.' 
          
                lines = information['query']
                list_lines = lines.split(',')
                first = translator.detect(list_lines[0])  
                
                for line in list_lines:
                    line_lang = translator.detect(line)
                    if line_lang.lang != first.lang:
                        no_content = "*Please only use one language. If you used the same language, please use other words"
                        break
                    else:
                        continue

                information["lang"] = str(first.lang)

                if information['btnradio'] != '' and information['pages'] != '' or information['btnradio'] == '' and information['pages'] == '': 
                    pages_problem = '*Please realod the page and only give us one number of pages.'
                if information['pages'] > "10":
                    pages_problem = "*Max: 1 pages"
                if information['espa'] != '' and information['engl'] != '' or information['espa'] == '' and information['engl'] == '': 
                    lang_problem = '*Please select only one language.' 
                if no_content != '' or pages_problem != '' or lang_problem != '':
                    raise NameError('Error')
            except:
                return render_template("mse-t.html", no_content = no_content, pages_problem = pages_problem, lang_problem = lang_problem)

            else:
                print("Ingreso correctamente")
                print(information)
                try:
                    print("hola")
                    inite = time.time()
                    calculus = list(calculate_mode(information))
                    fin = time.time()
                    total_time = fin-inite
                    print("{:2f} segundos en total".format(total_time))
                    
                    if calculus[0] != "":
                        beaft_doc = "Your document:"
                        calculated = calculus[0]
                        realaccuracy = calculus[1]
                        links = calculus[3]
                        result += "{}".format(calculated)
                        accuracy += "Text accuracy: {:2}%".format(round(float(realaccuracy*100)))
                        #print(calculus)
                        if information["br"] == "on":
                            links_user += "Bibliographic references: {}".format(links)           
                        fin = time.time()
                        print(f"{fin-inicio} segundos")
                        print(links)                       
                        session["tickets"] = session["tickets"] - session["t1"]
                        print(session["tickets"])
                        t_remaining = session["tickets"]
                        tickets = f"Tickets remaining: {t_remaining}"
                        if session["tickets"] == 0:
                            #session["current_date"] = datetime.datetime.today()
                            session["counter"] = int(1)
                            session["next-date"] = datetime.datetime.today() + datetime.timedelta(days=1) 
                            print(session["next-date"])
                            #session.clear()
                            
                        
                except Exception:
                    e = sys.exc_info()[1]
                    print("ErrorName: ", e.args[0])
                    no_content = "*Please try other words."
                    return render_template("mse-t.html", no_content = no_content)
               
    else:
        t_remaining = session["tickets"]
        tickets = f"Tickets remaining: {t_remaining}"
        return render_template("mse-t.html", beaft_doc = beaft_doc, tickets = tickets)

    return render_template("mse-t.html", result = result, beaft_doc = beaft_doc, accuracy = accuracy, links = links_user, tickets = tickets)

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000)
