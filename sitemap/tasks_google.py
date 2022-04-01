import requests
from requests.utils import quote

def refreshToken(client_id, client_secret, refresh_token):
    params = {
        "grant_type": "refresh_token",
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
    }

    authorization_url = "https://oauth2.googleapis.com/token"

    r = requests.post(authorization_url, data=params)

    if r.ok:
        return r.json()["access_token"]
    else:
        return None




def auth_login():
    client_id = "191006763430-9f531chgal4cuvkpsuq682ppu05cdn9s.apps.googleusercontent.com"
    client_secret = "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"
    refresh_token = "1//099_NNjlL4vjTCgYIARAAGAkSNwF-L9Ir7PirtiOtO0ecAPxDxv90vVFjpzgUooW-QihFWZMBAHw2rw_6X5xTagX9FEn0dJC6cEU"
    access_token = refreshToken(client_id, client_secret, refresh_token)

    access_token = refreshToken(client_id, client_secret, refresh_token)
    headers = {
        "Authorization": "Bearer "+access_token,
        "Accept": "application/json",
    }
    return headers



def sitemap_add_google(sitemap_url):
    siteurl = 'https://vizvasrj.com'
    site_url = quote(siteurl, safe='')


    headers = auth_login()
    sitemap = quote(sitemap_url, safe='')

    url = 'https://searchconsole.googleapis.com/webmasters/v3/sites/'+site_url+'/sitemaps/'+sitemap+'?key=AIzaSyDsyBTWnvjkU-DhNKX8WhNR_HiGBEKW60Q'

    r = requests.put(url, headers=headers)
    return r
