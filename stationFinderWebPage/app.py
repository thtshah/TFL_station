from flask import Flask, jsonify, request, render_template
import requests
from flask_bootstrap import Bootstrap5
import sys
app = Flask(__name__)


bootstrap = Bootstrap5(app)
@app.route('/')
def index():
   return '<h1 class="text-primary">Hello, Bootstrap!</h1>'


@app.route("/index")
def index2():
    return render_template("index.html")

@app.route('/error', methods=['GET', 'POST'])
def error():
    return render_template("errorPage.html")

@app.route('/departures', methods=['POST'])
def departures():
    station=request.form.get("stationName")
    station=station.strip(' ')
    if station == "":
        return render_template("errorPage.html")
    else:
        
        station=station+"Underground"
        print(station)
        stopPointId=stopPointId_search(station)
        departures=get_departure(stopPointId)
        noOfDepartures = request.form.get("noOfDepartures")
        noOfDepartures=noOfDepartures.strip(" ")
        if noOfDepartures == "":
            return render_template("errorPage.html")
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

            return render_template("hello.html",results=results,line_classes=line_classes)



@app.route('/home', methods=['GET', 'POST'])
def home():
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
                return render_template("errorPage.html"), None

            else:
                print('Error:', response.status_code)
                return None
        
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return render_template("errorPage.html")
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
                return render_template("errorPage.html"), None
            
    except requests.exceptions.RequestException as e:
        # Handle any network-related errors or exceptions
        print('Error:', e)
        return render_template("errorPage.html"), None
        return None

def parseResult(departures, noOfDepartures):
    try:
        trainInfo=[]
        for i in range (noOfDepartures):  
            station=departures[i]['stationName']
            tubeLine=departures[i]['lineName']
            platform=departures[i]['platformName']
            timeUntilDeparture=str(int(departures[i]['timeToStation'])//60)

            for data in departures[i]:
                if 'destinationName' in departures[i]:
                    destination=departures[i]['destinationName']
                else:
                    destination=""


            if destination == None:
                print('Error: No destination')
                return render_template("errorPage.html"), None

            else:
                trainInfo.append({'station':station, 'tubeLine':tubeLine, 'platform':platform,'destination':destination, 'timeUntilDeparture':timeUntilDeparture})

        trainInfo.sort(key=lambda train: int(train["timeUntilDeparture"]))
        return trainInfo
    
    except requests.exceptions.RequestException as e:
            # Handle any network-related errors or exceptions
            
            print('Error:', e)
            return render_template("errorPage.html"), None

if __name__ == '__main__':
    app.run(debug=True, port=8003)