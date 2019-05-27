import urllib.request
import urllib.error as liberr
import csv
from bs4 import BeautifulSoup
import re


#declarations
encoding = 'UTF-8'
city_list_file_name = "CityURLList.txt"
out_file_name = "city_data.csv"
add_city_url = "https://en.wikipedia.org/wiki/Category:Lists_of_cities_in_the_United_States_by_state"#"https://en.wikipedia.org/wiki/Lists_of_cities_in_the_United_States"
landing_page = "https://en.wikipedia.org/wiki/U.S._state"
state_univ_list_url = "https://en.wikipedia.org/wiki/List_of_state_universities_in_the_United_States"

use_old_list = False
print_city_name = False

state_url_list = []
city_url_list  = []
city_url_with_public_univ = []

# looks for population data from these years
pop_years = ["1698","1712","1723","1737","1746","1756","1771","1790","1800","1810","1820","1830","1840","1850","1860","1870","1880","1890","1900","1910","1920","1930","1940","1950","1960","1970","1980","1990","2000","2010","2011","2012","2013","2014","2015","2016","2017","2018"]


def GetCityPosIndex (tab, type):
    head = tab.find('thead')
    list = []
    head_tr = None
    if (head != None):
        print(head.getText())
        head_tr = head.find('tr')

    else:
        head = tab.find('tbody')
        head_tr_temp = head.find_all('tr')
        if (len(head_tr_temp) >= 2):
            if(type == 1):
                head_tr = head_tr_temp[1]
            elif type == 2:
                head_tr = head_tr_temp[0]
            else:
                head_tr = head_tr_temp[0]

    if (head_tr != None):
        head_th = head_tr.find_all('th')
        count = 0
        for values in head_th:
            count += 1
            if ("Community name" in values.getText() or "City" in values.getText() or "Name" in values.getText()):
                list.append(count)

    return list


def IsCityListTable (tab):
    #if tab.has_attr('class') and tab['class'] == "navbox":
    trs = tab.find_all('tr')

    caption = tab.find('caption')
    if (caption != None):
        sup = caption.find('sup')
        if (sup != None):
            sup.clear()
        if (caption != None):
            if ("Census Estimate" in caption.getText()):
                trs = tab.find_all('tr')
                return 5, range (1, len(trs))
            if "City" in caption.getText() or "town" in caption.getText():
                return 3, GetCityPosIndex(tab, 3)
            if ("cities" in caption.getText() or " Cities" in caption.getText()):
                return 2, GetCityPosIndex(tab, 2)

    trs = tab.find_all('tr')
    if (len(trs) > 0):
        th2 = trs[0].find('th')
        if th2 != None:
            div = th2.find_all('div')
            if len(div) >= 3:
                caption_3 = div[2]
                if (caption_3 != None):
                    if ("Washington" in caption_3.getText()):
                        return 1, [2]
                    if("cities" in caption_3.getText()):
                        return 1, GetCityPosIndex(tab, 1)
        th = trs[0].find_all('th')
        if len(th)>1 and ("City" in th[1].getText() or "Name" in th[1].getText()):
            return 1, [2]
        if (len(th)>0) and ("City" in th[0].getText() or "Name" in th[0].getText() or "Place" in th[0].getText()):
            return 3, [1]

    caption_2 = None
    if len(trs) > 1:
        ltd = trs[0].find_all('th')
        if (len(ltd) >= 2):
            caption_2 = ltd[1]
            if (caption_2 != None and ("Community name" in caption_2.getText() or "cities" in caption_2.getText())):
                return 4, GetCityPosIndex(tab, 4)
    return 0, []


def ProcessCityTables(data, url):
    tables = data.find_all('table')
    for tab in tables:
        if not tab.has_attr('class') or tab['class'] != "wikitable":
            local_tr = tab.find_all('tr')
            for tr1 in local_tr:
                local_td = tr1.find_all('td')
                for td1 in local_td:
                    if len(td1) > 0:
                        ParseCityList(td1, url, False)
        type, pos = IsCityListTable(tab)
        if type > 0:
            #print(tab)
            #print(type, pos)
            trs = tab.find_all('tr')
            col_count = -1
            for tr in trs:
                #if type == 3:
                tds = tr.find_all('th')
                if(len(tds)<1):
                    tds = tr.find_all('td')
                else:
                    if (tds[0].has_attr('class') and tds[0]['class'] == "navbox-title"):
                        continue
                    if(col_count==-1):
                        col_count = len(tds)
                if type <= 5:
                    adj=0
                    if(col_count>len(tds)):
                        adj=-1
                    for i in pos:
                        if (len(tds) >= i+adj and tds[i+adj - 1].find('a') != None):
                            if tds[i+adj - 1].getText().replace("\n","") == "Name":
                                if tds[i+adj - 1].find('a') !=None :
                                    AddCityFromSeperateListPage("https://en.wikipedia.org" + tds[i+adj - 1].find('a')['href'])
                            elif ("https://en.wikipedia.org" + tds[i+adj - 1].find('a')['href']) not in city_url_list and "/wiki" in tds[i+adj - 1].find('a')['href']:
                                city_url_list.append("https://en.wikipedia.org" + tds[i+adj - 1].find('a')['href'])
                                if (print_city_name):
                                    print(tds[i+adj - 1].getText().replace("\n",""))


def IsCityGallery (data):
    caption = data.find('li', attrs={'class': "gallerycaption"})
    if(caption != None):
        if ("Cities" in caption.getText()):
            return True
    return False


def ProcessCityGallery(data):
    gallery = data.find_all('ul', attrs={'class': "gallery"})
    for gal in gallery:
        if IsCityGallery (gal):
            all_li = gal.find_all('li')
            for li in all_li:
                if li['class'] == "gallerybox":
                    item = li.find('div', attrs={'class': "gallerytext"})
                    if item != None:
                        a = item.find('a')
                        if (a != None and "https://en.wikipedia.org" + a['href']) not in city_url_list and "/wiki/" in a['href']:
                            city_url_list.append("https://en.wikipedia.org" + a['href'])
                            if (print_city_name):
                                print(a.getText().replace("\n",""))


def AddCityFromSeperateListPage (url):

    if "/wiki/" not in  url:
        return
    #print ("\t*******Data from Subpage: ", url)
    success, response = GetWebPage(url)
    if (success):
        soup = BeautifulSoup(response, 'html.parser')
        ProcessCityTables(soup, url)
    else:
        print("Error in requesting URL: \"", url, "\". Error: \"", response, "\"")


def ProcessCityWithSeperateLists(data) :
    notes = data.find_all('div', attrs={'role': "note"})
    if (len(notes) > 0):
        for note in notes:
            all_a = note.find_all('a')
            if (len(all_a)>0):
                for a in all_a:
                    if a.has_attr('title') and "List of cities" in a['title']:
                        AddCityFromSeperateListPage("https://en.wikipedia.org" +a['href'])


def ProcessCityClimate(data, url, rows, is_external):
    climate_span = data.find('span', attrs={'id': "Climate"})
    if climate_span is None:
        #print("Climate data missing.")
        return
    koppen_val = ["Af","Am","Aw","As","BW","BS","Csa","Csb","Csc","Cfa","cfb","Cfb(2)","ET","EF",
                  "Cfc","Cwa","Cwb","Dfa","Dwa","Dsa","Dfb","Dwb","Dsb","Dfc","Dwc","Dsc","Dfd","Dwd","Dsd"]
    # regex for Köppen
    climate_h = climate_span.parent
    climate_p1 = climate_h.find_next('p')
    if climate_p1 is not None:
        climate_text = climate_p1.getText()
        res = re.findall("Köppen[^\.]*abbreviated[^\.]*[\"][^.]*[\"]", climate_text)
        if len(res) < 1:
            res = re.findall("Köppen[^\.]*is[^\.]*[\"][^.]*[\"]", climate_text)
        if len(res) > 0:
            ans = re.search("\"(.+?)\"", res[0])
            if ans:
                rows[InfoBoxHeader().index("Climate")] = ans.group(1)
                #print(ans.group(1))
                return
        res = re.findall("\(Köppen.*\)", climate_text)
        if(len(res)>0):
            for x in koppen_val:
                if x in res[0]:
                    rows[InfoBoxHeader().index("Climate")] = x
                    #print(x)
                    return
        res = re.findall("Köppen climate.*[c|C]limate \(.*\)", climate_text)
        if (len(res) > 0):
            for x in koppen_val:
                res = re.findall("\(.*\)", res[0])
                if (len(res) > 0):
                    if x in res[0]:
                        rows[InfoBoxHeader().index("Climate")] = x
                        #print(x)
                        return


def ParseCityList(data, url, is_external):
    ProcessCityWithSeperateLists(data)
    ProcessCityGallery (data)
    ProcessCityTables(data, url)


def PrepareCityURLList(url):
    if "/wiki/" not in  url:
        return
    print(url)
    success, response = GetWebPage(url)
    if (success):
        soup = BeautifulSoup(response, 'html.parser')
        ParseCityList(soup, url, False)
        #print ("Total candidate URL's: ", len(city_url_list))
    else:
        print("Error in requesting URL: \"", url, "\". Error: \"", response, "\"")


def ParseStateList(data):
    list_container = data.find('div', attrs={'class': "plainlist"})
    list_l = list_container.find_all('li')
    for elem in list_l:
        span = elem.get('span')
        if(span != None):
            span.clear()
        state_url_list.append("https://en.wikipedia.org"+elem.find('a')['href'])
    for state in state_url_list:
        PrepareCityURLList(state)
    return


def populate_state_wiki_url():
    success, response = GetWebPage(landing_page)
    if (success):
        soup = BeautifulSoup(response, 'html.parser')
        ParseStateList(soup)
    else:
        print("Error in requesting URL: \"", landing_page, "\". Error: \"", response, "\"")
    AddAdditonalCity()


def GetWebPage (city_page_url):
    try:
        city_web_page = urllib.request.urlopen(city_page_url)
    except (liberr.HTTPError,liberr.URLError,liberr.ContentTooShortError) as err:
        return False, err
    else:
        return True, city_web_page


def GetPopHeaderText(year):
    ret = "Population " + year
    return ret#.encode(encoding)


def GetDefaultRowVal():
    rows = ["",                     #"Name",
            "",                     #"category",
            "",                     #"Country",
            "",                     #"State",
            "",                     #"County",
            "",                     #"Region",
            "",                     #"Settled",
            "false",                #"Has Public University",
            "false",                #"Has Airport",
            "false",                #"Has SeaPort",
            "false",                #"Has Rapid transit",
            "false",                #"Has Commuter rail",
            "false",                #"Has Intercity rail",
            "false",                #"Has Rail",
            "false",                #"Has Ferries",
            "false",                #"Has Tourism",
            "",                     #"Consolidated",
            "",                     #"Incorporated",
            "",                     #"Named for",
            "0.0",                  #"Elevation",
            "0.0",                  #"Highest elevation",
            "0.0",                  #"Lowest elevation",
            "",                     #"FIPS code",
            "",                     #"GNIS feature ID",
            "",                     #"Website",
            "",                     #"Demonym(s)",
            "",                     #"Government•Type",
            "",                     #"Government•Body",
            "",                     #"Government•Mayor",
            "",                     #"Government•City Manager",
            "",                     #"Government•Deputy mayors",
            "",                     #"Government•City Council",
            "0.0",                   #"Area•Land",
            "0.0",                   #"Area•Water",
            "0.0",                   #"Area•Metro",
            "0.0",                   #"Area•Total",
            "0.0",                   #"Area•Urban",
            "0.0",                   #"Area•City",
            "0.0",                   #"Area•Metropolitan city",
            "0.0",                   #"Population•Estimate ",
            "0.0",                   #"Population•Rank",
            "0.0",                   #"Population•Density",
            "0.0",                   #"Population•Metro",
            "0.0",                   #"Population•Metropolitan city",
            "0.0",                   #"Population•Urban",
            "0.0",                  #"Population•City",
            "0.0",                   #"Population•CSA",
            "0.0",                  #"Population•MSA",
            "",                     #"Time zone",
            "",                     #"Climate"
            ]  # "ZIP Codes","Area code","Area code(s)",
    for year in pop_years:
        rows.append("0")
    return rows


def InfoBoxHeader():
    rows =["Name",
           "category",
           "Country",
           "State",
           "County",
           "Region",
           "Settled",
           "Has Public University",
           "Has Airport",
           "Has SeaPort",
           "Has Rapid transit",
           "Has Commuter rail",
           "Has Intercity rail",
           "Has Rail",
           "Has Ferries",
           "Has Tourism",
           "Consolidated",
           "Incorporated",
           "Named for",
           "Elevation",
           "Highest elevation",
           "Lowest elevation",
           "FIPS code",
           "GNIS feature ID",
           "Website",
           "Demonym(s)",
           "Government•Type",
           "Government•Body",
           "Government•Mayor",
           "Government•City Manager",
           "Government•Deputy mayors",
           "Government•City Council",
           "Area•Total",
           "Area•Land",
           "Area•Water",
           "Area•Metro",
           "Area•Urban",
           "Area•City",
           "Area•Metropolitan city",
           "Population•Estimate ",
           "Population•Rank",
           "Population•Density",
           "Population•Metro",
           "Population•Metropolitan city",
           "Population•Urban",
           "Population•City",
           "Population•CSA",
           "Population•MSA",
           "Time zone",
           "Climate"
           ] #"ZIP Codes","Area code","Area code(s)",
    for year in pop_years:
        rows.append(GetPopHeaderText(year))
    return rows


def AddValToList (container, list):
    if len(container) == 0:
        list.append("")
    else:
        list.append(container.getText())#.encode(encoding))


def check_is_valid_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def GetCounty (conatiner, list, pos, is_number):
    value = conatiner.find('td')
    if (value != None and len(value)> 0):
        span = value.find('span', attrs={'class': "nowrap"})
        if (span == None or len(span)==0):
            inner_span = value.find('span', attrs={'class': "flagicon"})
            if (inner_span != None):
                inner_span.clear()
            if is_number:
                x = re.findall("[0123456789,]+[.]*[0123456789]+", value.getText().replace('\xa0', ''))
                if len(x)> 0 :
                    if "." in x[0]:
                        list[pos] = x[0]
                    else:
                        list[pos] = x[0] + ".00"
                    list[pos]=list[pos].replace(',', '')
                    if not check_is_valid_number(list[pos]):
                        list[pos] = ""
                    #print(value.getText().replace('\xa0', ''), " to", x[0])
            else:
                list[pos] = value.getText().replace('\xa0', '')#.encode(encoding)
        else:
            inner_span = span.find('span', attrs={'class': "flagicon"})
            if (inner_span != None):
                inner_span.clear()
            list[pos] = span.getText().replace('\xa0', '')#.encode(encoding)


def HandleGroupedComp (item, tr, parent_list, rows, tbl_header):
    size = len(parent_list)
    cur_index = parent_list.index(tr) + 1
    sub_list = []
    is_number = True
    if item == "Government":
        is_number = False
        sub_list = ["•Type","•Mayor", "•City Manager","•Body","•Deputy mayors","•City Council"]
    elif item == "Area":
        sub_list = ["•Total","•Land", "•Water","•Metro","•Metropolitan city","•Urban","•City"]
    elif item == "Population":
        sub_list = ["•Estimate ","•Rank", "•Density","•Metro","•Metropolitan city","•Urban","•City","•CSA","•MSA"]
    while (cur_index < size):
        next_row = parent_list[cur_index]
        if (next_row.has_attr('class') and next_row['class'] == "mergedtoprow"):
            break
        table_header = next_row.find('th')
        if(table_header!=None):
            for sub_item in sub_list:
                if (table_header.getText().replace('\xa0', '').startswith(sub_item)):
                    GetCounty(next_row, rows, tbl_header.index(item+sub_item), is_number)
        cur_index = cur_index + 1


def ProcessPopulationData(rows, popt, header):
    pop_body = popt.find('tbody')
    if(pop_body != None and len(pop_body)>0):
        pop_tr = pop_body.find_all('tr')
    else:
        pop_tr = popt.find_all('tr')
    for tr in pop_tr:
        th = tr.find('th')
        if(th==None):
            td = tr.find_all('td')
            check = td[0].getText()
            if len(td)>=2:
                val = td[1]
            else:
                val = None
        else:
            td = tr.find_all('td')
            body = th.find('a')
            if(body == None):
                check = th.getText()
            else:
                check = body.getText()
            if(len(td)>=2):
                val = td[0]
            else:
                val = None

        if(val == None):
            continue
        for year in pop_years:
            if year in check :
                sup = val.find('sup')
                if(sup != None):
                    sup.clear()
                index =header.index(GetPopHeaderText(year))
                rows[index] = val.getText().replace(",","")
                if len(rows[index] )> 0 :
                    if not check_is_valid_number(rows[index] ):
                        rows[index]  = ""
                break


def ProcessTransportData(data, rows):
    all_mw_headline = data.findAll('span', attrs={'class': "mw-headline"})
    for line in all_mw_headline:
        if line.has_attr('id'):
            if "sea" in line['id'] or "Sea" in line['id']:
                rows[InfoBoxHeader().index("Has SeaPort")] = "True"
            elif "Airport" in line['id'] or "airport" in line['id']:
                rows[InfoBoxHeader().index("Has Airport")] = "True"
            elif "Ferries" in line['id'] or "ferries" in line['id']:
                rows[InfoBoxHeader().index("Has Ferries")] = "True"
            elif "Rail" in line['id'] or "rail" in line['id']:
                rows[InfoBoxHeader().index("Has Rail")] = "True"
            elif "Intercity rail" in line['id'] or "Intercity Rail" in line['id']:
                rows[InfoBoxHeader().index("Has Intercity rail")] = "True"


def ProcessTransportationURL(url, rows):
    if "/wiki/" not in  url:
        return
    #print("Processing additional transportation URL: ", url)
    success, response = GetWebPage(url)
    if (success):
        soup = BeautifulSoup(response, 'html.parser')
        ProcessTransportData(soup, rows)
    else:
        print("Error in requesting URL: \"", url, "\". Error: \"", response, "\"")


def ProcessTransportation (data, link, rows):
    all_note = data.findAll('div', attrs={'class': "hatnote navigation-not-searchable", 'role': "note"})
    for note in all_note:
        a = note.find('a')
        if a is not None and a.has_attr('title'):
            if "Transportation in" in a['title']:
                ProcessTransportationURL("https://en.wikipedia.org"+a['href'], rows)


def ProcessBooleanInfo(data, link, rows):
    ProcessTransportation(data, link, rows)
    headline = data.findAll('span', attrs={'class': "mw-headline"})
    for line in headline:
        if "Tourism" in line.getText() or "tourism" in line.getText():
            rows[InfoBoxHeader().index("Has Tourism")] = "True"
    if link in city_url_with_public_univ:
        rows[InfoBoxHeader().index("Has Public University")] = "True"


def ParseInfoBox (web_page_html_soup, link):
    header = InfoBoxHeader()
    rows = GetDefaultRowVal ()

    ProcessBooleanInfo(web_page_html_soup, link, rows)

    #processClimateData
    ProcessCityClimate(web_page_html_soup, link, rows, False)

    #get the population data
    popt = web_page_html_soup.find('table', attrs={'class': "toccolours"})

    if(popt != None and len(popt)>0):
        ProcessPopulationData(rows, popt, header)

    #get the infobox table
    ibt = web_page_html_soup.find('table', attrs={'class':"infobox geography vcard"})
    if (ibt == None):
        #print ("infobox missing: ", link)
        return None
    ibt_tr = ibt.find_all('tr')

    for tr in ibt_tr:
        first_th = tr.find('th')
        if first_th is not None:
            if "Airport" in first_th.getText() or "airport" in first_th.getText():
                rows[InfoBoxHeader().index("Has Airport")] = "True"
            if "Rapid transit" in first_th.getText() or "Rapid Transit" in first_th.getText():
                rows[InfoBoxHeader().index("Has Rapid transit")] = "True"
            if "Commuter rail" in first_th.getText() or "Commuter Rail" in first_th.getText():
                rows[InfoBoxHeader().index("Has Commuter rail")] = "True"
        name = tr.find('div', attrs={'class': "fn org"})
        if (name != None and len(name)>0):
            rows[0] = name.getText()
            continue
        category = tr.find('div', attrs={'class': "category"})
        if (category != None and len(category)>0):
            rows[1] = category.getText()
            continue
        table_header = tr.find('th')
        if (table_header != None and len(table_header)>0):
            grouped_content = ["Government","Area","Population"]
            for item in grouped_content:
                if (table_header.getText().startswith(item)):
                    HandleGroupedComp(item, tr, ibt_tr, rows, header)
            local_list = ["Time zone","Incorporated","Demonym(s)","Website","Country",
                          "State","County","Region","Settled","Consolidated","Named for",
                          "GNIS feature ID", "FIPS code"]
            for item in local_list:
                if (table_header.getText() == item):
                    GetCounty(tr, rows, header.index(item), False)
            local_list = ["Highest elevation", "Lowest elevation", "Elevation"]
            for item in local_list:
                if (table_header.getText() == item):
                    GetCounty(tr, rows, header.index(item), True)
    return rows


def WriteCityListToFile (name):
    with open(name, 'w') as filehandle:
        for listitem in city_url_list:
            filehandle.write('%s\n' % listitem)


def ReadListFromFile(name):
    with open(name, 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1]

            # add item to the list
            if(currentPlace not in city_url_list) and "/wiki/" in currentPlace:
                city_url_list.append(currentPlace)


def ProcessUnivPage(data, url):

    info_box = data.find('table', attrs={'class': "infobox vcard"})
    if info_box is not None:
        print(url)
        all_tr =info_box.findAll('tr')
        for tr in all_tr:
            th = tr.find('th')
            if th is not None and (th.getText()=="Location" or th.getText()=="Address"):
                #td = tr.find('td', attrs={'class': "adr"})
                td = tr.find('td')
                if td is not None:
                    div = td.find('div', attrs={'class': "locality"})
                    if div is None:
                        div = td.find('div', attrs={'class': "extended-address"})
                    if div is not None:
                        a = div.find('a')
                    else:
                        a = td.find('a')
                    if a is not None:
                        new_url = "https://en.wikipedia.org" + a['href']
                        if new_url not in city_url_list and "/wiki/" in new_url:
                            city_url_list.append(new_url)
                        city_url_with_public_univ.append(new_url)


def ProcessUniversityURL(url):
    if "/wiki/" not in  url:
        return
    success, response = GetWebPage(url)

    if success:
        soup = BeautifulSoup(response, 'html.parser')
        # print (soup)
        ProcessUnivPage(soup, url)

    else:
        print("Error in requesting public univ page: \"", url, "\". Error: \"", response, "\"")


def MapCityToAddMeta(data):
    all_li = data.findAll('li', recursive=True)
    for li in all_li:
        sub_list = li.find('ul')
        if sub_list is not None:
            continue
        a = li.find('a')
        if (a is not None and a.has_attr('href') and "/wiki/" in a['href']):
            url = "https://en.wikipedia.org" + a['href']
            ProcessUniversityURL(url)


def ProcessStateUniversity():
    success, response = GetWebPage(state_univ_list_url)

    if success:

        soup = BeautifulSoup(response, 'html.parser')
        # print (soup)
        MapCityToAddMeta(soup)
        print("Done")

    else:
        print("Error in requesting public univ page: \"", state_univ_list_url, "\". Error: \"", response, "\"")


def ProcessCityListTables(data):
    soup = data
    # print (soup)
    table_all = soup.findAll('table', attrs={'class': ["wikitable", "sortable"]})
    for table in table_all:
        head = table.find('thead')
        pos = 0
        if head is not None:
            #print(head)
            all_th = head.findAll("th")
            for th in all_th:
                pos = pos + 1
                if "Name" in th.getText()or"City" in th.getText()or "Municipality" in th.getText() or "place" in th.getText() or "Place" in th.getText():
                    break
        body = table.find('tbody')
        if body is not None:
            all_tr = body.findAll('tr')
            if head is None:
                #print(all_tr[0])
                all_th = all_tr[0].findAll("th")
                for th in all_th:
                    pos = pos + 1
                    if "Name" in th.getText()or"City" in th.getText()or "Municipality" in th.getText() or "place" in th.getText()or "Place" in th.getText():
                        break
            #print(pos)
            for tr in all_tr:
                all_th = tr.find_all('td')
                if (len(all_th) >= pos):
                    #print(all_th)
                    a = all_th[pos - 1].find('a')
                    #print(a)
                    if a is not None:
                        new_url = "https://en.wikipedia.org" + a['href']
                        if new_url not in city_url_list and "/wiki/" in new_url:
                            city_url_list.append(new_url)
                            #print("New City: ", new_url)


def ProcessAddCityPage (url):
    if "/wiki/" not in  url:
        return
    success, response = GetWebPage(url)

    if success:
        #print("1************************************************************************")
        print(url)
        soup = BeautifulSoup(response, 'html.parser')
        ProcessCityListTables(soup)
        #process for list of city and town in page
        all_li = soup.find_all('li', recursive=True)
        for li in all_li:
            a =li.find('a')
            keywords = ["Lists of United States cities","List of cities","List of towns","List of places","List of municipalities"]
            if a is not None:
                for key in keywords:
                    if a.has_attr('title') and key in a['title'] and "World" not in a.getText():
                        new_url = "https://en.wikipedia.org" + a['href']
                        #new_url = "https://en.wikipedia.org/wiki/List_of_cities_and_counties_in_Virginia"
                        #print(key)
                        #print(li)
                        if "/wiki/" in  url:
                            success, response = GetWebPage(new_url)

                            if success:
                                #print("2************************************************************************")
                                print(new_url)
                                soup = BeautifulSoup(response, 'html.parser')
                                ProcessCityListTables(soup)




    else:
        print("Error in requesting public univ page: \"", url, "\". Error: \"", response, "\"")


def ProcessAddAdditonalCity(data):
    div = data.find('div', attrs={'class': "mw-parser-output"})
    ul = div.find('ul')
    all_li = ul.findAll('li')
    for li in all_li:
        a = li.find('a')
        if a is not None and a.has_attr('href'):
            new_url = "https://en.wikipedia.org" + a['href']
            ProcessAddCityPage (new_url)

def AddAdditonalCity():

    success, response = GetWebPage(add_city_url)

    if success:
        soup = BeautifulSoup(response, 'html.parser')
        # print (soup)
        ProcessAddAdditonalCity(soup)

    else:
        print("Error in requesting public univ page: \"", add_city_url, "\". Error: \"", response, "\"")


def main ():
    print_city_name = True
    #city_list_file_name = "CityList.txt"
    # PrepareCityURLList("https://en.wikipedia.org/wiki/Delaware")
    # print (city_url_list)

    with open(out_file_name, 'w', encoding=encoding, newline='') as f_output:

        csv_output = csv.writer(f_output)
        csv_output.writerows([InfoBoxHeader()])

        if not use_old_list:
            populate_state_wiki_url()
            WriteCityListToFile(city_list_file_name)
        else:
            ReadListFromFile(city_list_file_name)

        ProcessStateUniversity ()

        total = len(city_url_list)
        start_index = 0
        count = start_index

        print("Total candidate URL's: ", total)

        for city_page_url in city_url_list[start_index:]:

            count = count + 1

            if (count%50) == 0:
                #print(count, "/", total, " City URL: ", city_page_url)
                print(count, "/", total)

            success, response = GetWebPage(city_page_url)

            if success:

                soup = BeautifulSoup(response, 'html.parser')
                # print (soup)
                info = ParseInfoBox(soup, city_page_url)

                if info is not None:
                    #print(info)
                    if info[InfoBoxHeader().index("Name")] == "" or info[InfoBoxHeader().index("Name")] is None:
                        info = None
                        #print("#####################No Name Entry: ",city_page_url)
                    else:
                        csv_output.writerows([info])

            else:
                print("Error in requesting URL: \"", city_page_url, "\". Error: \"", response, "\"")


if __name__ == "__main__":
    main()