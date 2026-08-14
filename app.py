import os
from datetime import datetime
from zoneinfo import ZoneInfo
from flask import Flask, request, render_template, request, flash
import re
import requests

#from flask_bootstrap import Bootstrap5
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for flash messages
print("heloo")

@app.route('/navbar')
def navbar():
    return render_template("navbar.html")

@app.route('/')
def loginOptions():
   return render_template("loginOptions.html")

@app.route('/loginchoices')
def loginOptions2():
   return render_template("loginOptions.html")

#CHECKS FOR USER'S USERNAME AND EMAIL IN DATABASE
#IF EITHER IS THERE, USER IS SENT TO FINDSTATION PAGE
@app.route('/login', methods=['GET'])
def login():
    return render_template("userLogin.html")

@app.route('/accountManagement', methods=['POST'])
def accountManagement():
    username_or_email=request.form.get("username_or_email")
    password=request.form.get("password")
    file = open("database.txt", "r")
    content = file.read()
    file.close()
    usernamePassword=username_or_email+" - "+password
    if username_or_email==None or password==None:
        return render_template("errorPage.html", loginFail=True)
    elif usernamePassword in content:
        return render_template("findStation.html", username_or_email=username_or_email)
    else:
        return render_template("userLogin.html", loginFail=False)

#ADDS NEW USER'S USERNAME AND EMAIL INTO DATABASE
@app.route('/signup', methods=['GET'])
def signup():
    return render_template("userSignUp.html")

@app.route('/addAccount', methods=['POST'])
def addAccount():
    file = open("database.txt", "r")
    content = file.read()
    file = open("database.txt", "a")
    username=request.form.get("username")
    userEmail=request.form.get("userEmail")
    password=request.form.get("password")
    passwordcheck=request.form.get("passwordcheck")
    if len(password) < 8 or not re.search(r"\d", password) or not re.search(r"[A-Z]", password):
            flash("Password must be at least 8 characters, include a number and an uppercase letter.")
            return render_template("userSignUp.html")
    elif username==None or userEmail==None:
        file.close()
        return render_template("userSignUp.html")
    elif username in content:
        file.close()
        return render_template("userLogin.html")
    elif password != passwordcheck:
        return render_template("userSignUp.html", password=password, passwordcheck=passwordcheck)
    else:
        print(password)
        file.write("\n"+username+" - "+password)
        file.write("\n"+userEmail+" - "+password)
        file.write("\n    ")
        file.close()
        return render_template("userLogin.html")



@app.route('/error', methods=['GET', 'POST'])
def error():
    return render_template("errorPage.html")

@app.route('/departures', methods=['POST'])
def departures():
    station=request.form.get("stationName")
    station=station.strip(' ')
    if station == "":
        return render_template("errorPage.html", response_status_code=404)
    else:
        
        station=station+"Underground"
        print(station)
        stopPointId=stopPointId_search(station)
        departures=get_departure(stopPointId)
        noOfDepartures = request.form.get("noOfDepartures")
        noOfDepartures=noOfDepartures.strip(" ")
        if noOfDepartures == "":
            return render_template("errorPage.html", response_status_code=404)
        else:
            noOfDepartures=abs(int(noOfDepartures))
            results=parseResult(departures, noOfDepartures)
            line_classes = {
                "Bakerloo": "custom-bakerloo",
                "Central": "custom-central",
                "Circle": "custom-circle",
                "District": "custom-district",
                "Hammersmith & City": "custom-hammersmith_city",
                "Jubilee": "custom-jubilee",
                "Metropolitan": "custom-metropolitan",
                "Northern": "custom-northern",
                "Piccadilly": "custom-piccadilly_TFLRail",
                "TFL Rail": "custom-piccadilly_TFLRail",
                "Victoria": "custom-victoria",
                "Waterloo & City": "custom-waterloo_city",
                "Elizabeth": "custom-elizabeth",
                "London Overground": "custom-overground",
                "DLR": "custom-dlr",
                "Tramlink": "custom-tramlink",
                "Superloop": "custom-superloop"
            }
            return render_template("results.html",results=results,line_classes=line_classes)



@app.route('/home', methods=['GET', 'POST'])
def home():
    username=request.form.get("username")
    userEmail=request.form.get("userEmail")
    if username=="" and userEmail=="":
        return render_template("userLogin.html")
    else:
        return render_template("findStation.html", image_file="TFL_TubeMap.jpg")

def stopPointId_search(station):
    url = 'https://api.tfl.gov.uk/StopPoint/Search/'+str(station)

    try:
        response = requests.get(url)

        if response.status_code == 200:
            jsonResponse = response.json()

            for match in jsonResponse['matches']:
                if 'tube' in match['modes']:
                    id = match['id']
                    return id
                    
        else:
            if response.status_code==401 or 403 or 404 or 500 or 503:
                print('Error:', response.status_code)
                return render_template("errorPage.html", response_status_code=response.status_code), None

            else:
                print('Error:', response.status_code)
                return None
        
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return render_template("errorPage.html", response_status_code=500), None
        return None

def get_departure(id):
    if id:
        url = 'https://api.tfl.gov.uk/StopPoint/'+ str(id) +'/arrivals?&app_id=DbProject&app_key=afc7bf1d95b448588b28c712b6ed4ad8'

    else:
        print('Failed to fetch stopPointId from API.')
        return render_template("errorPage.html")

        

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            id = response.json()
            return id
        else:
            if response.status_code==401 or 403 or 404 or 500 or 503:
                print('Error:', response.status_code)
                return render_template("errorPage.html", response_status_code = response.status_code), None
            
    except requests.exceptions.RequestException as e:
        # Handle any network-related errors or exceptions
        print('Error:', e)
        return render_template("errorPage.html", response_status_code = 500), None

def parseResult(departures, noOfDepartures):
    try:
        trainInfo=[]
        for i in range (noOfDepartures):  
            station=departures[i]['stationName']
            tubeLine=departures[i]['lineName']
            platform=departures[i]['platformName']
            currentlocation=departures[i]['currentLocation']
            timeUntilDeparture=str(int(departures[i]['timeToStation'])//60)


            expectedArrivalInUTC=departures[i]['expectedArrival']

            timestamp = expectedArrivalInUTC

            dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

            london_time = dt.astimezone(ZoneInfo("Europe/London"))

            expectedArrival=(london_time.strftime("%H:%M.%S"))

            for data in departures[i]:
                if 'destinationName' in departures[i]:
                    destination=departures[i]['destinationName']
                else:
                    destination=""


            if destination == None:
                print('Error: No destination')
                return render_template("errorPage.html"), None

            else:
                trainInfo.append({'station':station, 'tubeLine':tubeLine, 'platform':platform,'destination':destination, 'currentLocation':currentlocation, 'timeUntilDeparture':timeUntilDeparture, 'expectedArrival':expectedArrival})

            if departures[i] == departures[-1]:
                break

        trainInfo.sort(key=lambda train: int(train["timeUntilDeparture"]))
        return trainInfo
    
    except requests.exceptions.RequestException as e:
            # Handle any network-related errors or exceptions
            
            print('Error:', e)
            return render_template("errorPage.html"), None

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))