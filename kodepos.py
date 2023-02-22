import time

import requests
from bs4 import BeautifulSoup
import json
import csv

# set the URL and initial search parameters
url = "https://kodepos.posindonesia.co.id/kodeposalamatlist?cmd=search"
params = {
    "z_Propinsi": "=",
    "x_Propinsi": "",
    "z_Kabupaten": "=",
    "x_Kabupaten": "",
    "z_Kecamatan": "=",
    "x_Kecamatan": "",
    "z_Kelurahan": "=",
    "x_Kelurahan": "",
    "search": "",
    "searchtype": "",
    "recperpage": "100",
}
# params["x_Propinsi"] = str('31')
# params["x_Kabupaten"] = str('31.71')
# params["x_Kecamatan"] = str('31.71.01')

# function to retrieve data from a single page
def get_data_from_page(url, params,prov,kab,kec):
    data = []
    while True:
        # Send a GET request to the URL with the current query parameters
        response = requests.get(url, params)

        # Parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table rows that contain the province data
        rows = soup.select('#tbl_kodeposalamatlist tbody tr')

        # If there are no rows, we have reached the end of the pages
        if not rows:
            break

        # Loop through each row and extract the data
        for idx, row in enumerate(rows):
            cols = row.select('td')
            # Extract the data from each column
            data.append({
                'kodepos' : cols[9].text.strip(),
                'propinsi' : cols[1].text.strip(),
                'kabupaten' : cols[2].text.strip(),
                'kecamatan' : cols[3].text.strip(),
                'kelurahan' : cols[4].text.strip(),
                'alamat' : cols[7].text.strip(),
            })

        # Find the next button and update the query parameters to go to the next page
        next_button = soup.select_one('button.btn-default[data-value="next"][data-ew-action="redirect"]')
        print('NEXT BUTTON', next_button)
        if next_button:
            next_url = next_button['data-url']
            params = {
                'recperpage': 100,
                **dict(q.split('=') for q in next_url.split('?')[-1].split('&'))
            }
            params["x_Propinsi"] = str(prov)
            params["x_Kabupaten"] = str(kab)
            params["x_Kecamatan"] = str(kec)
            # time.sleep(5)
        else:
            break

    return data




# set the list to hold all data
all_data = []

# propinsi = []
# with open('propinsi.csv', 'r') as fileProv:
#     readerProv = csv.DictReader(fileProv)
#     for rowProv in readerProv:
#         propinsi.append(rowProv)
#
# kabupaten = []
# with open('kabupaten_kota.csv', 'r') as fileKab:
#     readerKab = csv.DictReader(fileKab)
#     for rowKab in readerKab:
#         kabupaten.append(rowKab)

kecamatan = []
with open('kecamatan.csv', 'r') as fileKec:
    readerKec = csv.DictReader(fileKec)
    for rowKec in readerKec:
        kecamatan.append(rowKec)

# for rowProv in propinsi:
#     for rowKab in kabupaten:
#         if rowKab['propinsi'] == rowProv['nama']:
with open('kodepos.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write the header row
    writer.writerow(['kodepos', 'propinsi', 'kabupaten', 'kecamatan', 'kelurahan', 'alamat'])

    for rowKec in kecamatan:
        # if rowKec['kabupaten'][5:] == rowKab['nama']:
        params["x_Propinsi"] = str(rowKec['propinsi'])
        params["x_Kabupaten"] = str(rowKec['kabupaten'])
        params["x_Kecamatan"] = str(rowKec['kode'])
        data=get_data_from_page(url, params, rowKec['propinsi'], rowKec['kabupaten'], rowKec['kode'])
        # all_data.extend(data)
            # time.sleep(10)
        for i in range(len(data)):
            kodepos = data[i]['kodepos']
            propinsiData = data[i]['propinsi']
            kabupatenData = data[i]['kabupaten']
            kecamatanData = data[i]['kecamatan']
            kelurahanData = data[i]['kelurahan']
            alamat = data[i]['alamat']
            writer.writerow([kodepos, propinsiData, kabupatenData, kecamatanData, kelurahanData, alamat])








print("Finished scraping {} pages".format(len(all_data)))
