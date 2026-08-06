import requests

from main import main_flow
    

def stopPointId_search():
    url = 'https://api.tfl.gov.uk/StopPoint/Search/CanaryWharfUnderground'

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
        url_list = ['https://api.tfl.gov.uk/StopPoint/', str(id) ,'/arrivals?&app_id=DbProject&app_key=afc7bf1d95b448588b28c712b6ed4ad8']
        url= ("").join(url_list)

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


def main():
    stopPointId = stopPointId_search()
    #check stoppoint
    if stopPointId!="Error":
        departure=get_departure(stopPointId)

        station=departure[0]['stationName']
        tubeLine=departure[0]['lineName']
        platform=departure[0]['platformName']
        destination=departure[0]['destinationName']
        waitTime=str(int(departure[0]['timeToStation'])//60)

        formatted_msg=('The next train from {} on the {} line departs from {} and is going to {} in {} minutes').format(station, tubeLine, platform, destination, waitTime)
        print(formatted_msg)
    else:
        print('Error')


main()

'''

#main()
# 1. call the search endpoint
    #1.1. loop over results, find the stop point id
    # modes will contain 'tube'
# 2. get_departures(stop_point_id)
    #2.1 call stop point departures endpoint, using the stop point id we found in 1.1

    '''