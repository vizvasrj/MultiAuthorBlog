from scrape.models import Healthline
from scrape.models import HealthlineParsed
from termcolor import colored
from datetime import datetime
from stringcolor import cs
# from deep_translator import GoogleTranslator
# from markdown_1 import markdown_html

import redis

redis = redis.Redis(
    host='localhost',
    port='6379'
)

article = []
for x in Healthline.objects.all():
    article.append(x.url)

health = []
for x in HealthlineParsed.objects.all():
    health.append(x.url)

set_parsed = set(set(article)-set(health))


def clean_data_and_save(pk):
    from bs4 import BeautifulSoup
    import time
    from termcolor import colored

    article = Healthline.objects.get(id=pk).description
    soup = BeautifulSoup(article, 'html.parser')
    try:
        soup_v2 = soup.article.find_all()
    except AttributeError:
        return False
    soup_v3 = BeautifulSoup(str(soup_v2), 'html.parser')
    
    
    blockquote = []
    table = []
    p = []
    h2 = []

    # def translate_tags(tag_string):
    #     if len(tag_string) > 0:
    #         print(colored(GoogleTranslator(
    #             source='auto', target='hi'
    #             ).translate(tag_string), "green"))


    # this is the function where printing happens
    def _remove_all_attrs_except_saving(soup):
        from lxml import html
        from lxml.html import clean
        
        html_string = soup
        tree = html.fromstring(html_string)
        
        cleaner = html.clean.Cleaner()
        cleaner.safe_attrs_only = True
        cleaner.safe_attrs=frozenset(['href', 'src', 'target'])
        cleaned = cleaner.clean_html(tree)
        return str(html.tostring(cleaned), 'utf-8')


    # This is to find url and assigne it to me

    def get_full_amzn_address(link):
        import requests
        print(cs(link, '#ffbbcc'))
        value = redis.get(link)
        if value:
            my_amazon_url = str(value, 'utf-8')
            print(value)
        else:
            my_amazon_url = requests.head(link).headers['location']
            redis.set(link, my_amazon_url)

        return my_amazon_url


    def upload_to_imgbb(img_url):
        import requests
        url = "https://api.imgbb.com/1/upload"
        payload={
        'key':"5fa37a82b258559698525ff7c0bc0c5a",
        'image':img_url
        }
        response = requests.post(
            url,
            payload
            )
        import json
        json_data = json.loads(response.text)
        return json_data['data']['image']['url']


    # Amazon checker
    def amazon_checker(url):
        if url.startswith("https://www.amazon."):
            url = url.replace(";", "&")
            splitted = url.split("&")
            # print(splitted)
            all_url = []
            for x in splitted:
                # print(x)
                if x.startswith("tag"):
                    if url.startswith("https://www.amazon.com"):
                        all_url.append("tag=vizvasrj-20")
                    elif url.startswith("https://www.amazon.in"):
                        all_url.append("tag=vizvasrj-21")
                else:
                    all_url.append(x)
            # print(colored("&".join(all_url),"yellow"))
            return "&".join(all_url)
        # This will do good for amzn.to
        elif url.startswith("https://amzn.to/"):
            # This will send small url to get full url 
            url = get_full_amzn_address(link=url)
            url = url.replace(";", "&")
            splitted = url.split("&")
            # print(splitted)
            all_url = []
            for x in splitted:
                # print(x)
                if x.startswith("tag"):
                    if url.startswith("https://www.amazon.com"):
                        all_url.append("tag=vizvasrj-20")
                    elif url.startswith("https://www.amazon.in"):
                        all_url.append("tag=vizvasrj-21")
                else:
                    all_url.append(x)
            # print(colored("&".join(all_url),"yellow"))
            return "&".join(all_url)
        elif url.startswith("/health/"):

            return url
        else:
            return url


    # url changer // to http:
    def change_src(src):
        return "http:"+src


    # This tag checker checks that small_tag that is/
    # <a> or <blockquote> is in <p>
    # <a> in <h2>
    def tag_checker(small_tag, big_tag):
        if str(small_tag) in str(big_tag):
            return ""
        else:
            return small_tag

    inside_tags = []

    # its take only tag and it do find all the tag inside it
    def inner_tag(tag):
        for all_tag in tag.find_all():
            # print(colored(all_tag.name, "red"))
            # this is to add all tag inside 
            # For example inside paragraph there could be i and div
            # and strong this will add to the list inside _tags
            #  
            inside_tags.append(all_tag.name)
            """This will remove all the div from that inside_tags list"""
            for x in range(len(all_tag.name)):
                try:
                    inside_tags.remove("div")
                except ValueError:
                    pass
                # print(colored(inside_tags, "blue"))

    all_html = []

    # This will change it to str ie
    # all tags to string
    # so i can append to all_html = []

    def change_to_str(tag):
        all_html.append(str(tag))
        return True



    # change href before everything:
    for x in soup_v3.find_all('a'):
        try:
            if x['href']:
                # print(x['href'])
                x['href'] = amazon_checker(url=x['href'])
        except KeyError:
            pass

    for tag in soup_v3:
        if tag.name:
            if tag.name == 'p':
                try:
                    if tag['class'][0] == 'hl-cr-note':
                        break
                except KeyError:
                    pass
                # i like to empty all the find tags inside that
                p_tag_checker = tag_checker(
                    small_tag=tag, big_tag=blockquote
                    )
                # this will empty all inside_tags before filling it up
                inside_tags = []
                # this will fill inside_tags
                inner_tag(tag)

                p = []
                p.append(p_tag_checker)
                p_tag_checker = str(p_tag_checker).replace("&amp;check;", "&#10003;")
                change_to_str(p_tag_checker)
            elif tag.name == 'h1':
                change_to_str(tag)
            elif tag.name == 'h2':
                inside_tags = []
                inner_tag(tag)

                h2 = []
                h2.append(tag)
                change_to_str(tag)
            elif tag.name == 'a':
                if 'a' in inside_tags:
                    inside_tags.remove("a")
                else:
                    try:
                        classes = tag["class"]
                        if "icon-hl-pinterest" in classes:
                            pass
                        else:
                            try:
                                href = amazon_checker(tag['href'])
                                if href.startswith('/'):
                                    try:
                                        if tag['class'][0] == "css-prnfjo":
                                            pass
                                        else:
                                            a_href = "<a data-href='"+href+"'>"+tag.string+"</a>"
                                    except TypeError:
                                        a_href = ""
                                else:
                                    # if str(tag.string) is None:
                                    #     a_href = "<a href='"+href+"'>"+""+"</a>"
                                    try:
                                        a_href = "<a href='"+href+"'>"+tag.string+"</a>"
                                    except TypeError:
                                        a_href = ""
                            except KeyError:
                                a_href = ""
                            change_to_str(a_href)
                    except KeyError:
                        pass
                # print(colored(inside_tags, "yellow"))
                # a_tag_checker = tag_checker(
                #     small_tag=tag, big_tag=p
                #     )
                # print(a_tag_checker)
            elif tag.name == 'h3':
                inside_tags = []
                inner_tag(tag)
                change_to_str(tag)
            elif tag.name == 'blockquote':
                change_to_str(tag)
                blockquote = []
                blockquote.append(tag)
            elif tag.name == 'ul':
                inside_tags = []
                inner_tag(tag)
                ul_tag_checker = tag_checker(
                    small_tag=tag, big_tag=table
                    )

                # !!!!!!!!!!!!!!!!!!!!!!!
                # try:
                #     tag = ul_tag_checker
                # except:
                #     pass
                tag = ul_tag_checker
                # !!!!!!!!!!!!!!!!!!!!!!!
                change_to_str(tag)
            elif tag.name == 'lazy-image':
                src = tag['src']
                src = change_src(src)
                src = upload_to_imgbb(img_url=src)
                print(colored(src, "green"))
                change_to_str('<img src="'+src+'">')

                
                # for a in tag:
                #     if a.name == 'img':
                #         print(a)
            elif tag.name == 'picture':
                try:
                    src = tag.img['src']
                    src = change_src(src)
                    src = upload_to_imgbb(img_url=src)
                    print(colored(src,"green"))
                    change_to_str('<img src="'+src+'">')
                except TypeError:
                    pass
            
            elif tag.name == 'ol':
                inside_tags = []
                inner_tag(tag)
                change_to_str(tag)

            elif tag.name == 'h4':
                inside_tags = []
                inner_tag(tag)
                change_to_str(tag)
            
            elif tag.name == 'hr':
                break

            elif tag.name == 'table':
                table = []
                table.append(tag)
                inner_tag(tag)
                if "&amp;check;" in str(tag):
                    tag = str(tag).replace("&amp;check;", "&#10003;")

                html_table = []
                table_body = tag.find('tbody')
                rows = table_body.find_all('tr')
                count = 0
                for row in rows:
                    th_cols = row.find_all('th')
                    for th in th_cols:
                        if th.a:
                            th_a_st = th.a.string
                            th_a_href = th.a['href']
                            # html_table.append()
                            full_a = "<a href="+th_a_href+">"+th_a_st+"</a>"
                            # print(cs(str(th).replace(str(th.a), full_a), "#324871"))
                        else:
                            pass
                            # print(cs(th, "yellow"))
                    td_cols = row.find_all('td')
                    td_fill = []
                    for td in td_cols:
                        if td.a:
                            td_a_st = td.a.string
                            td_a_href = td.a['href']
                            # html_table.append()
                            full_a = "<a href="+td_a_href+">"+td_a_st+"</a>"
                            td_fill.append(str(td).replace(str(td.a), full_a))
                        else:
                            td_fill.append(str(td))
                    if count == 0:
                        html_table.append("<tr>"+("".join(td_fill)).replace("<td>", "<th>").replace("</td>", "</th>")+"</tr>")
                        count += 1
                    else:
                        html_table.append("<tr>"+("".join(td_fill))+"</tr>")
                    # print(colored(cols, "blue"))
                full_tabel = "<table>"+"".join(html_table)+"</table>"
                change_to_str(full_tabel)

            elif tag.name == 'div':
                try:
                    if tag['class'][0] in 'hl-cr-drug-comparison-filter':
                        break
                except KeyError:
                    pass
    # print(colored("".join(all_html), "green"))
    if all_html == []:
        article_description = None
        article_description_2 = None
    else:
        article_description = _remove_all_attrs_except_saving("".join(all_html))
        article_description_2 = article_description.replace('</div>', '').replace('<div>', '')
    # print(colored(str(article_description_2), "green"))
    # import time
    # time.sleep(20)
    author = Healthline.objects.get(id=pk).author
    a_soup_v1 = BeautifulSoup(author, 'html.parser')
    try:
        a_soup_v2 = a_soup_v1.section.find_all()
        a_soup_v3 = BeautifulSoup(str(a_soup_v2), 'html.parser')
    except AttributeError:
        pass

    def get_author(a_soup_v3):
        for x in a_soup_v3:
            if x.name == 'span':
                if 'authors' in str(x):
                    #print(x)
                    auth = x.getText()
                    if "by" in auth:
                        return auth.split("by")[1].lstrip()
                    else:
                        return auth


    # as function suggest date from string
    def date_from_string(date_time_str):
        date_time_obj = datetime.strptime(str(date_time_str), '%B %d, %Y')
        return date_time_obj

    # 
    
    def date_span_to_date(span):
        date_with_space = span.split("on")[1].split("<")[0]
        stript_date = date_with_space.lstrip()
        return date_from_string(stript_date)

    def get_date_span(a_soup_v3):
        # print(colored(a_soup_v3, "yellow"))
        for t in  a_soup_v3:
            if t.name == "span":
                if 'on January' in str(t):
                    date_str = date_span_to_date(str(t))
                elif 'on February' in str(t):
                    date_str = date_span_to_date(str(t))
                elif 'on March' in str(t):
                    date_str = date_span_to_date(str(t))
                elif 'on April' in str(t):
                    date_str = date_span_to_date(str(t))
                elif 'on May' in str(t):
                    date_str = date_span_to_date(str(t))
                elif 'on June' in str(t):
                    date_str = date_span_to_date(str(t))
                elif 'on July' in str(t):
                    date_str = date_span_to_date(str(t))
                elif 'on August' in str(t):
                    date_str = date_span_to_date(str(t))
                elif 'on September' in str(t):
                    date_str = date_span_to_date(str(t))
                elif 'on October' in str(t):
                    date_str = date_span_to_date(str(t))
                elif 'on November' in str(t):
                    date_str = date_span_to_date(str(t))
                elif 'on December' in str(t):
                    date_str = date_span_to_date(str(t))
                else:
                    date_str = datetime.today().strftime("%Y-%m-%d")
        return date_str
    try:
        author_name = get_author(a_soup_v3)
        article_date = get_date_span(a_soup_v3)
    except UnboundLocalError:
        article_date = None
        author_name = None
    article_url = Healthline.objects.get(id=pk).url
    article_title = Healthline.objects.get(id=pk).title
    article_thumbnail = Healthline.objects.get(id=pk).thumbnail
    # print(colored(article_date, "blue"))
    # print(colored(author_name, "blue"))
    # print(colored(article_url, "blue"))
    print(colored(article_title, "blue"))

    # print(colored(article_description_2, "red"))
    # print(GoogleTranslator(source='auto', target='hi').translate(article_title))
    print(Healthline.objects.get(id=pk).url)

    # import sys
    # sys.exit("Hi I exit")
    # article_t_title = markdown_html(article_title)
    # article_t_description = markdown_html(article_description_2)

    ddd = article_date
    if article_description_2 is None:
        print(article_description_2)
        pass
    else:
        print(colored(HealthlineParsed.objects.get_or_create(
            title=article_title,
            # news_website="1",
            description=article_description_2,
            url=article_url,
            thumbnail=article_thumbnail,
            author=author_name,
            original_date = ddd
            # checker_runtime="1",
        ), "red"))


for x in set_parsed:
    print(colored(x,"red"))
    article_id = Healthline.objects.get(url=x).id

    clean_data_and_save(pk=article_id)
# clean_data_and_save(pk=17072)
