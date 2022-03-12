'''
@author:Benny Lisangi
'''
import os
import requests
def query_pararms(name:str, id_):
    '''
    returns the query parameters of this function comprising name and id.
    '''
    return "/review and comments"+"?name="+name+"&id="+id_

def fetch_yt(word:str)->str:
    '''
    Returns a YouTube a link for the trailer after
    fetching the trailing video key from The Movie Database.
    '''
    url = "http://api.themoviedb.org/3/movie/"+word+"/videos?"
    query_args = {
        "api_key":os.getenv("TMDB_KEY"),
    }
    response_ = requests.get(url, params= query_args)
    try:
        key = response_.json()["results"][0]["key"]
        yt_url = "https://www.youtube.com/embed/"
        return yt_url+key
    except IndexError:
        return None
        
def fetch_wiki(term:str)->str:
    '''fetch_wiki takes a string, finds the wikipedia page id that corresponds to the search term
    then builds a wikipedia link for that page.

    '''
    wiki_url = "https://en.wikipedia.org/w/api.php"
    wiki_params = {
        "action": "query",
        "titles":term,
        "format":"json",
    }
    output = requests.get(wiki_url, wiki_params)
    pageid= list(output.json()['query']['pages'])[0]
    if pageid != '-1':
        return "http://en.wikipedia.org/?curid="+pageid
    return "/Home"
