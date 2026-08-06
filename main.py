from tracemalloc import stop

import requests

     # get the stop point

def main_flow():
    url = 'https://api.tfl.gov.uk/StopPoint/Search/CanaryWharfUnderground'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            #for match in matches
            #if mode contains 'tube'
            #stop point id = match.id
            #call get_posts(stoppointid)
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None

    
     #get_posts(stop point id)
     # - parameterise the url using the retrieved stop point id


def get_posts(posts):
    # Define the API endpoint URL
    posts=main_flow()
    if posts:
        stopPoint = posts['matches']
        stopPointId = stopPoint[0]['id']
        url_list = ['https://api.tfl.gov.uk/StopPoint/', stopPointId ,'/arrivals?&app_id=DbProject&app_key=afc7bf1d95b448588b28c712b6ed4ad8']
        url= ("").join(url_list)
    else:
            print('Failed to fetch posts from API.')

    try:
        # Make a GET request to the API endpoint using requests.get()
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            posts = response.json()
            return posts
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        # Handle any network-related errors or exceptions
        print('Error:', e)
        return None


def get_posts_DLR():
    url_1='https://api.tfl.gov.uk/StopPoint/940GZZDLCAN/arrivals?&app_id=DbProject&app_key=afc7bf1d95b448588b28c712b6ed4ad8'

    try:
            # Make a GET request to the API endpoint using requests.get()
            response_1 = requests.get(url_1)
    
            # Check if the request was successful (status code 200)
            if response_1.status_code == 200:
                posts_1 = response_1.json()
                return posts_1
            else:
                print('Error:', response_1.status_code)
                return None
    except requests.exceptions.RequestException as e:
            # Handle any network-related errors or exceptions
            print('Error:', e)
            return None
     


def main():
    posts = get_posts()
    posts_1 = get_posts_DLR()

    if posts and posts_1:
        num=0
        for i in range (3):
            if int(posts[num]['timeToStation']) < int(posts_1[num]['timeToStation']):
                 print('The next train from', posts[num]['stationName'],'on the',posts[num]['lineName'], 'line departs from', posts[num]['platformName'], 'and is going to', posts[num]['destinationName'], 'in', str(int(posts[num]['timeToStation'])//60),'minutes')
            elif int(posts[num]['timeToStation']) > int(posts_1[num]['timeToStation']):
                 print('The next train from', posts_1[num]['stationName'],'on the',posts_1[num]['lineName'], 'line departs from', posts_1[num]['platformName'], 'and is going to', posts_1[num]['destinationName'], 'in', str(int(posts_1[num]['timeToStation'])//60),'minutes')
            elif int(posts[num]['timeToStation']) == int(posts_1[num]['timeToStation']):
                 print('The next train leaves in', str(int(posts_1[num]['timeToStation'])//60),'minutes from', posts[num]['stationName'],'on the',posts[num]['lineName'], 'line and departs from', posts[num]['platformName'], 'and is going to', posts[num]['destinationName'],', or the next train from', posts_1[num]['stationName'],'on the',posts_1[num]['lineName'], 'line departs from', posts_1[num]['platformName'], 'and is going to', posts_1[num]['destinationName'])
            else:
                print('Failed to fetch posts from API.')
            num=num+1

if __name__ == '__main__':
    main()



#main()
# 1. call the search endpoint
    #1.1. loop over results, find the stop point id
    # modes will contain 'tube'
# 2. get_departures(stop_point_id)
    #2.1 call stop point departures endpoint, using the stop point id we found in 1.1
