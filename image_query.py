import requests
import random
from pprint import pprint
from collections import Counter

# global lists so that the user's data does not get reset
type_likes = []
make_likes = []
color_likes = []
condition_likes = []

count = 0

# car object for storing query information.
class Car():
    def __init__(self, url='', type='', make='', color='', condition=''):
        self.url = url
        self.type = type
        self.make = make
        self.color = color
        self.condition = condition
    
    def set_url(self, url):
        self.url = url

    def get_url(self):
        return self.url
    
    def get_color(self):
        return self.color

    def get_type(self):
        return self.type
    
    def get_make(self):
        return self.make

    def get_condition(self):
        return self.condition
    
    def set_type(self, type):
        self.type = type
    
    def set_condition(self, condition):
        self.condition = condition
    

def make_request(website, car):
    """ 
    This is the function that makes the actual query. It can be given any parameters
    so that it can be called in instances other than random.
    """
    api_key = '40942229-12632621050d81131aeb8535b'
    google_api_key = ' AIzaSyCnaNHhVk7mCTB4r_V3ACbkOazY05B4uF4 '
    cse_id = '97ea8e86608a74b0a'

    fail_image = 'https://i.redd.it/this-guy-from-strange-addiction-who-is-in-love-with-his-car-v0-g1hxcgdio7i81.jpg?width=2340&format=pjpg&auto=webp&s=73551fc5611686f3aa6b71c83d10de77e2057a67'

    query = f'Vehicle - {car.get_color()} {car.get_make()} {car.get_type()} {car.get_condition()}'

    if website != 'google':
        # pixabay API query
        url = f'https://pixabay.com/api/?key={api_key}&q={query}'
    else:
        # google query API (only use this for final product)
        url = f'https://www.googleapis.com/customsearch/v1?key={google_api_key}&cx={cse_id}&q={query}&searchType=image'


    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()

        if 'hits' in data and data['hits']: # pixabay
            image = random.choice(data['hits'])
            car.set_url(image['largeImageURL'])
            return True, car 
        elif 'items' in data and data['items']: # google
            print('Google image!')
            image = random.choice(data['items'])
            car.set_url(image['link'])
            return True, car
        else:
            return False, car
        
    else:
        print('API request error!')
        car.set_url(fail_image)
        return False, car
    
def query(website):
    """ This is the function that randomly queries the search engines """

    car_makes = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'Volkswagen', 'BMW', 'Mercedes-Benz', 'Audi', 'Nissan']
    color_list = ['red', 'blue', 'green', 'yellow', 'orange', 'white', 'black', 'silver', 'gold']
    car_types = ['car', 'truck', 'van', 'SUV']
    conditions = ['new', 'used', 'old']

    make_random = random.choice(car_makes)
    color_random = random.choice(color_list)
    type_random = random.choice(car_types)
    condition_random = random.choice(conditions)

    # build return object
    car = Car(type=type_random, make=make_random, color=color_random, condition=condition_random)
    return make_request(website, car)

def like_data(type, make, color, cond):
    """ This function adds the names of the liked attributes """
    global count
    type_likes.append(type)
    make_likes.append(make)
    color_likes.append(color)
    condition_likes.append(cond)
    print(type_likes)
    print(make_likes)
    print(color_likes)
    print(condition_likes)
    count += 1
    return count
    
def result_data():
    """ This function returns the names of the most common items ineach attribute list """
    type_count = Counter(type_likes)
    make_count = Counter(make_likes)
    color_count = Counter(color_likes)
    condition_count = Counter(condition_likes)
    common_type = type_count.most_common(1)[0][0]
    common_make = make_count.most_common(1)[0][0]
    common_color = color_count.most_common(1)[0][0]
    common_condition = condition_count.most_common(1)[0][0]
    return (common_type, common_make, common_color, common_condition)

def enough_data():
    """ This function determines when we are finished with mathing. """
    thresh = 3
    makes = Counter(make_likes)
    colors = Counter(color_likes)
    return makes.most_common(1)[0][1] >= thresh and colors.most_common(1)[0][1] >= thresh

def clear_data():
    """ This funcion ensures that the data is cleared """
    global count 
    count = 0
    type_likes.clear()
    make_likes.clear()
    color_likes.clear()
    condition_likes.clear()

def increment_count():
    """ just a little setter type function """
    global count
    count += 1

if __name__ == "__main__":
    result = query()
    print(result)
