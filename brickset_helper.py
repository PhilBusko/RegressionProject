"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
BRICKSET HELPER
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import requests
import time
import bs4 as bs
import numpy as np


BASE_URL = 'https://brickset.com'
BROWSE_URL = 'https://brickset.com/browse/sets'


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


# manager function to get all pages of a year
def get_year(year_tx):

    print(f'year: {year_tx}')
    page_no = 0
    pages_all = False
    url_ls = []

    while (pages_all == False):
        
        # stop the loop when the page returns empty

        page_no += 1
        url_page_ls = get_year_paginated(year_tx, page_no)

        if len(url_page_ls) == 0:
            pages_all = True
            print(f'last page: {page_no -1}')

        else:
            url_ls += url_page_ls            

    return url_ls


# endpoint for getting all set urls of parameter year
def get_year_paginated(year_tx, page_no):

    if page_no % 10 == 0:
        print(f'page no: {page_no}')   

    # get the full page html

    if page_no == 1:
        endpoint_url = f'{BASE_URL}/sets/year-{year_tx}'
    else:
        endpoint_url = f'{BASE_URL}/sets/year-{year_tx}/page-{page_no}'

    try:
        response = requests.get(endpoint_url)
        time.sleep(.5)
        # raise an exception based on status code
        response.raise_for_status()
    except Exception as err:
        print(f'Endpoint: {endpoint_url}') 
        print(f'Error: {err}') 
        raise err

    page_sp = bs.BeautifulSoup(response.text, 'html.parser')

    # loop through articles to get urls
    
    url_ls = []
    article_sp = page_sp.find_all('article')
    #print(f'articles found: {len(article_sp)}')

    if len(article_sp) == 0:
        return []

    for artc in article_sp:
        div_meta_sp = artc.find_all('div', {'class': 'meta'})[0]
        h1_sp = div_meta_sp.find_all('h1')[0]
        link_sp = h1_sp.find_all('a')[0]
        text_ls = link_sp.text.split(':')

        # some sets (books, gear) don't have a set-no

        if len(text_ls) == 2:
            set_dx = {
                'set_no': text_ls[0].strip(),
                'name': text_ls[1].strip(),
                'url': link_sp['href'],
            }
        else:
            set_dx = {
                'set_no': '0000',
                'name': text_ls[0].strip(),
                'url': link_sp['href'],
            }

        url_ls.append(set_dx)

    return url_ls


# get all fields for the parameter set
def get_set_data(set_url):

    # get the full page html

    endpoint_url = f'{BASE_URL}{set_url}'

    try:
        response = requests.get(endpoint_url)
        time.sleep(.5)
        # raise an exception based on status code
        response.raise_for_status()
    except Exception as err:
        print(f'Endpoint: {endpoint_url}') 
        print(f'Error: {err}') 
        raise err

    page_sp = bs.BeautifulSoup(response.text, 'html.parser')

    # get the data fields

    set_dx = {
        'set_no': None,
        'name': None,
        'url': set_url, 
        'set_type': None,
        'theme_group': None,
        'theme': None,
        'subtheme': None,
        'year': None,
        'tags': None,
        'piece_cnt': None,
        'minifig_cnt': 0,
        'inventory_url': None,
        'minifig_url': None, 
        'store_price': None,
        'current_price': None,
        'packaging': None,
        'notes': None,
        'rating_value': None,
        'rating_votes': None,
    }

    try:
        section_sp = page_sp.find_all('section', {'class': 'featurebox'})[0]
        section_dl_sp = page_sp.find_all('dl')[0].children
    except Exception as ex:
        return {}

    #print(f'section children: {len(list(section_dl_sp))}')    # this consumes the iterator
    #print(type(section_dl_sp))

    while (True):
        # loop stops when iterator throws error at the end of list
        try:
            # not sure why blank spaces are in iterator as NavigableString
            navstring_skip = next(section_dl_sp)
            field_name_sp = next(section_dl_sp)
            navstring_skip = next(section_dl_sp)
            field_value_sp = next(section_dl_sp)
            #print(field_name_sp.text)
            #print(field_value_sp.text)
        except StopIteration:
            break
        except Exception as ex:
            print(f'Field Error: {endpoint_url}')
            raise ex

        field_name = field_name_sp.text

        if field_name == 'Set number':
            set_dx['set_no'] = field_value_sp.text

        elif field_name == 'Name':
            set_dx['name'] = field_value_sp.text

        elif field_name == 'Set type':
            set_dx['set_type'] = field_value_sp.text

        elif field_name == 'Theme group':
            set_dx['theme_group'] = field_value_sp.text

        elif field_name == 'Theme':
            set_dx['theme'] = field_value_sp.text

        elif field_name == 'Subtheme':
            set_dx['subtheme'] = field_value_sp.text

        elif field_name == 'Year released':
            set_dx['year'] = field_value_sp.text

        elif field_name == 'Tags':
            tags_ls = []
            tags_sp = field_value_sp.find_all('a')
            for tag_a in tags_sp:
                tags_ls.append(tag_a.text.strip())
            set_dx['tags'] = ', '.join(tags_ls) 

        elif field_name == 'Pieces':
            #print(field_value_sp)
            set_dx['piece_cnt'] = field_value_sp.text
            link_sp = field_value_sp.find_all('a')
            if link_sp:
                set_dx['inventory_url'] = link_sp[0]['href']
        
        elif field_name == 'Minifigs':
            set_dx['minifig_cnt'] = field_value_sp.text
            link_sp = field_value_sp.find_all('a')
            if link_sp:
                set_dx['minifig_url'] = link_sp[0]['href']

        elif field_name == 'RRP':
            set_dx['store_price'] = field_value_sp.text.replace(' / ', ', ')

        elif field_name == 'Current value':
            set_dx['current_price'] = field_value_sp.text.replace('\n', '').replace('~', '').replace('U', ', U')

        elif field_name == 'Packaging':
            set_dx['packaging'] = field_value_sp.text

        elif field_name == 'Notes':
            set_dx['notes'] = field_value_sp.text

        elif field_name == 'Rating':
            value_tx = field_value_sp.text[5:].replace('reviews', '').replace('from', ',').replace(' ', '')
            value_ls = value_tx.split(',')
            if len(value_ls) == 2:
                set_dx['rating_value'] = value_ls[0]
                set_dx['rating_votes'] = value_ls[1]
            elif field_value_sp.text.strip() == 'Not yet reviewed':
                pass
            else:
                print(f'rating error: {field_value_sp.text}')

    return set_dx


# clean the store-price so it is a float in dollars
def clean_price(price):
    # skip when price doesn't have a value
    if isinstance(price, float):
        #print(f'float found {price}')
        return np.nan

    price_ls = price.split(',')
    fprice = None
    
    for prc in price_ls:
        if '$' in prc:
            fprice = float(prc.strip()[1:])
    
    if fprice:
        return fprice
    else:
        return np.nan


# clean the current-price so it is a float in dollars
def get_price_used(price):
    return get_current_price(price, 'used')

def get_price_new(price):
    return get_current_price(price, 'new')

def get_current_price(price, price_type):
    
    # this data is never NaN

    price_ls = price.split(',')
    
    if price_type == 'used':
        fprice = price_ls[1].replace('Used: $', '')

    else:
        fprice = price_ls[0].replace('New: $', '')

    try:
        nprice = int(fprice)
    except:
        nprice = None

    return nprice


# clean the ratings votes
def clean_votes(votes_tx):
    # skip when price doesn't have a value
    if isinstance(votes_tx, float):
        #print(f'float found {price}')
        return np.nan

    votes_cl = votes_tx.replace('review', '')
    return float(votes_cl)


# get a count of the entries in the list of lists
def count_in_lists(list_ls):
    
    # get counts of each tag

    counts_dx = {}

    for lst in list_ls:
        entry_ls = lst.split(', ')

        for ntr in entry_ls:

            if ntr not in counts_dx:
                counts_dx[ntr] = 1
            else:
                counts_dx[ntr] += 1

    # tranform to structure good for dataframe

    counts_ls = []

    for key, val in counts_dx.items():
        new_dx = {
            'tag': key,
            'count': val,
        }
        counts_ls.append(new_dx)

    return counts_ls





"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DEPRECATED
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# endpoint for listing years and corresponding urls
def get_years():

    # get the page's full html

    endpoint_url = BROWSE_URL
    try:
        response = requests.get(endpoint_url)
        # raise an exception based on status code
        response.raise_for_status()
    except Exception as err:
        print(f'Endpoint: {endpoint_url}') 
        print(f'Error: {err}') 
        return

    page_sp = bs.BeautifulSoup(response.text, 'html.parser')

    # find the years section
    
    section_sp = page_sp.find_all('section', {'class': 'navrow'})
    #print(len(section_sp))

    year_sp = None
    for sect in section_sp:
        h1_sp = sect.find_all('h1')
        
        for h1 in h1_sp:
            if h1.text == 'Years':
                year_sp = sect

    if not year_sp:
        print(f'year section not found')
        return

    # get the years data

    year_ls = []

    year_link_sp = year_sp.find_all('a')
    print(f'years found: {len(year_link_sp)}')

    for link in year_link_sp:
        year_dx = {
            'year': link.text,
            'url': link['href'],
        }
        year_ls.append(year_dx)

    return year_ls






