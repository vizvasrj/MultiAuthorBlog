def rundemo():
    print('Hello')

def runtcollector():
    import requests, json
    import time

    from bs4 import BeautifulSoup
    from termcolor import colored
    from thesaurus.models import RelationsScore, Thesaurus

    headers = {
        'Host': 'www.thesaurus.com',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': 'bid=434421-1644557003888; sid=725019-1649858435629',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
    }

    with open('thesaurus/list.txt', 'r') as f:
        op = f.readlines()

    list_op = []
    for a in op:
        list_op.append(a.strip())


    for b in list_op:
        print(b)
        num = b

        url = 'https://www.thesaurus.com/list/'+str(num)

        r = requests.get(url, headers=headers)

        soup = BeautifulSoup(r.text, 'html.parser')

        ul_soup = soup.findAll('ul', {'data-testid':"list-az-results"})[0]

        li_list = []
        for c in ul_soup.findAll('li'):
            li_list.append((c.get_text()).strip())

        for d in li_list:
            # print(d)
            word = Thesaurus.objects.get_or_create(name=d)[0]
            from requests.utils import quote
            # time.sleep(0.7)
            d_encode = quote(d)
            d_2 = d_encode.replace('/', '%2F')
            url2 = "https://tuna.thesaurus.com/pageData/"+d_2
            r = requests.get(url2)
            rj = r.json()
            try:
                syn = rj["data"]["definitionData"]["definitions"][0]["synonyms"]
                ant = rj["data"]["definitionData"]["definitions"][0]["antonyms"]
            except KeyError:
                print(colored('KeyError '*500, 'blue'))
                print(rj)    
                print(colored('KeyError '*500, 'blue'))
                return False
            try:
                for e in syn:
                    term = e['term']
                    similarity = e['similarity']
                    rel_to = Thesaurus.objects.get_or_create(name=term)[0]
                    r = RelationsScore.objects.get_or_create(
                        word=word, related_word=rel_to,
                        score=similarity, syn=True
                    )[0]
            except KeyError:
                pass

            try:
                for f in ant:
                    term = f['term']
                    similarity = f['similarity']
                    rel_to = Thesaurus.objects.get_or_create(name=term)[0]
                    r = RelationsScore.objects.get_or_create(
                        word=word, related_word=rel_to,
                        score=similarity, syn=False
                    )[0]
            except KeyError:
                pass


            # print(syn, ant)
