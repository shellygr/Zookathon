import urllib2

def getEndangeredStatus(titles):
    for title in titles[:5]:
        title = title.replace(' ','_')
        title = title.lower()
        response = urllib2.urlopen('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=categories&clshow=!hidden&titles={0}'.format(title))
        html = response.read()
        print html
        if html.find('IUCN Red List least concern species') != -1:
            return 0
        if html.find('IUCN Red List near threatened species') != -1:
            return 1
        if html.find('IUCN Red List vulnerable species') != -1:
            return 2
        if html.find('IUCN Red List endangered species') != -1:
            return 3
        if html.find('IUCN Red List critically endangered species') != -1:
            return 4
        if html.find('IUCN Red List extinct in the wild species') != -1:
            return 5
        if html.find('IUCN Red List extinct species') != -1:
            return 6
    return -1