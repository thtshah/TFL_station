from flask import Flask, jsonify, request
import requests
app=Flask(__name__)

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message':'Hello, world'})

@app.route('/departures', methods=['GET'])
def departures():
    data=request.get_json()
    stopPointId=stopPointId_search((data["stationName"]).strip(' '))
    departures=get_departure(stopPointId)
    noOfDepartures = int(data["noOfDepartures"])
    results=parseResult(departures, noOfDepartures)
    return results

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
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

def get_departure(id):
    if id:
        url = 'https://api.tfl.gov.uk/StopPoint/'+ str(id) +'/arrivals?&app_id=DbProject&app_key=afc7bf1d95b448588b28c712b6ed4ad8'

    else:
        print('Failed to fetch stopPointId from API.')

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            id = response.json()
            return id
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        # Handle any network-related errors or exceptions
        print('Error:', e)
        return None

def parseResult(departures, noOfDepartures):
    trainInfo=[]
    num=0
    for i in range (noOfDepartures+1):
        station=departures[num]['stationName']
        tubeLine=departures[num]['lineName']
        platform=departures[num]['platformName']
        destination=departures[num]['destinationName']
        timeUntilDeparture=str(int(departures[num]['timeToStation'])//60)
        if num>0:
            if (int(departures[num]['timeToStation'])//60) < (int(departures[num-1]['timeToStation'])//60):
                trainInfo.insert((num-1), {'station':station, 'tubeLine':tubeLine, 'platform':platform,'destination':destination, 'timeUntilDeparture':timeUntilDeparture})
            else:
                trainInfo.append({'station':station, 'tubeLine':tubeLine, 'platform':platform,'destination':destination, 'timeUntilDeparture':timeUntilDeparture})
                        
        num=num+1

    return jsonify(trainInfo)


if __name__ == '__main__':
    app.run(debug=True)