@author Chase Fensore

from bs4 import BeautifulSoup
import requests
import re
import csv
import urllib3
#CALL function to recieve URL

#exampleURL = 'http://www.calendariodoagronegocio.com.br/Evento/visualizar/portugues/3226'

#run this for each URL, 1 file total
#repeat is BOOLEAN
#'local' is 'venue'
def write_ToCSV(fileName, address, local, addressLocality, startDay, startMonth, startYear, endDay, endMonth, endYear, segmento, repeat):
    csvData = [['Address', 'Venue', 'City', 'Start Day', 'Start Month', 'Start Year', 'End Day', 'End Month', 'End Year', 'Segment'],
    [address, local, addressLocality, startDay, startMonth, startYear, endDay, endMonth, endYear, segmento]]

    with open(fileName, 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    if repeat==False:
        csvFile.close()

def process_URL(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data.decode('utf-8'), features="html.parser")
    return soup


#MAIN 
#soup is the pool of HTML we search from
def main():

    fileName = input('Enter file name ex. brazilEvents.csv (n to quit): ')

    url = input('Enter full event URL (n to quit): ')

    repeat = True
    while url != 'n':
        #soup = process_URL(url)
        http = urllib3.PoolManager()
        response = http.request('GET', url)
        soup = BeautifulSoup(response.data.decode('utf-8'), features="html.parser")
        startDate = str(soup.find("span", itemprop="startDate").text)
        startDay = startDate[0: 2]

        startYear = startDate[len(startDate)-4: len(startDate)]


    #TRANSFORM startMonth into numeral ex.) 01
        startMonth = startDate[6: len(startDate)-8]
        if startMonth=='janeiro':
            startMonth = '01'
        elif startMonth=='fevereiro':
            startMonth = '02'
        elif startMonth=='março':
            startMonth = '03'
        elif startMonth=='abril':
            startMonth = '04'
        elif startMonth=='maio':
            startMonth = '05'
        elif startMonth=='junho':
            startMonth = '06'
        elif startMonth=='julho':
            startMonth = '07'
        elif startMonth=='agosto':
            startMonth = '08'
        elif startMonth=='setembro':
            startMonth = '09'
        elif startMonth=='outubro':
            startMonth = '10'
        elif startMonth=='novembro':
            startMonth = '11'
        elif startMonth=='dezembro':
            startMonth = '12'



    #FIND itemprop="endDate"
    #endDate = soup.find("span", itemprop="endDate").text
    #TRANSFORM into date/time
        #FIND itemprop="endDate"
        endDate = str(soup.find("span", itemprop="endDate").text)
        endYear = endDate[len(endDate)-4: len(endDate)]

        #FIND itemprop="endDate"
        endMonth = endDate[6: len(endDate)-8]
        if endMonth == 'janeiro':
            endMonth = '01'
        elif endMonth=='fevereiro':
            endMonth = '02'
        elif endMonth=='março':
            endMonth = '03'
        elif endMonth=='abril':
            endMonth = '04'
        elif endMonth=='maio':
            endMonth = '05'
        elif endMonth=='junho':
            endMonth = '06'
        elif endMonth=='julho':
            endMonth = '07'
        elif endMonth=='agosto':
            endMonth = '08'
        elif endMonth=='setembro':
            endMonth = '09'
        elif endMonth=='outubro':
            endMonth = '10'
        elif endMonth=='novembro':
            endMonth = '11'
        elif endMonth=='dezembro':
            endMonth = '12'

        endDay = endDate[0: 2]

    #FIND "Periodicidade" (FREQUENCY)
        frequency = str(soup.find(text=re.compile("Periodicidade: (.*)")))
        frequency = frequency[15: len(frequency)]

    #FIND ADDRESS
    #soup = BeautifulSoup(str(spanParent), features="html.parser")
        address = str(soup.find("span", itemprop="streetAddress").text)
    #FIND addressLocality
    #soup = BeautifulSoup(str(spanParent), features="html.parser")
        addressLocality = str(soup.find("span", itemprop="addressLocality").text)
        addressLocality = addressLocality[1: len(addressLocality)]

    #FIND addressRegion
        addressRegion = str(soup.find("span", itemprop="addressRegion").text)

    #FIND "Pais" (Country)
        pais = str(soup.find(text=re.compile("País: (.*)")))
        pais = pais[6:len(pais)]

    #FIND postalCode
        postalCode = str(soup.find("span", itemprop="postalCode").text)
        postalCode = postalCode[1:]

    #FIND "Local" (Location/Venue)
        local = str(soup.find(text=re.compile("Local: (.*)")))
        local = local[7:len(local)]

    #FIND "Categoria" (Category)
        category = str(soup.find(text=re.compile("Categoria: (.*)")))
        category = category[11:len(category)]

    #FIND Segmento (Segment)
        segmento = str(soup.find(text=re.compile("Segmento: (.*)")))
        segmento = segmento[10:len(segmento)]

    #FIND Promoter (promotor)
        promotor = str(soup.find(text=re.compile("Promotor: (.*)")))
        promotor = promotor[10:len(promotor)]

    #FIND address of Promotor
        promotorAddress = str(soup.find(text=re.compile("do Promotor: (.*)")))
        promotorAddress = promotorAddress[22:len(promotorAddress)]

    #FIND telefone
        telefone = str(soup.find(text=re.compile("Telefone: (.*)")))
        telefone = telefone[10:len(telefone)]


        url = input("Enter full event URL (n to quit): ")
        if url == 'n':
                repeat = False
        #WRITE to csv file
    write_ToCSV(fileName, address, local, addressLocality, startDay, startMonth, startYear, endDay, endMonth, endYear, segmento, repeat)

if __name__ == "__main__":
    main()
