import requests
from bs4 import BeautifulSoup
import csv

# Set the base URL and query parameters
base_url = 'https://kodepos.posindonesia.co.id/kabupatenkotalist'
params = {
    'recperpage': 100,
    'search': '',
}

# Create a CSV file to store the scraped data
with open('kabupaten_kota.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['No.', 'Kode', 'Nama', 'Propinsi', 'Jenis','Ibu Kota'])

    # Keep looping until there are no more pages
    while True:
        # Send a GET request to the URL with the current query parameters
        response = requests.get(base_url, params=params)

        # Parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table rows that contain the province data
        rows = soup.select('#tbl_kabupatenkotalist tbody tr')

        # If there are no rows, we have reached the end of the pages
        if not rows:
            break

        # Loop through each row and extract the data
        for idx,row in enumerate(rows):
            cols = row.select('td')

            # Extract the data from each column
            no = cols[1].text.strip()
            kode = cols[4].text.strip()
            nama = cols[5].text.strip()
            provinsi = cols[2].text.strip()
            jenis = cols[3].text.strip()
            ibukota = cols[6].text.strip()

            # Write the data to the CSV file
            writer.writerow([no, kode, nama,provinsi,jenis,ibukota])

        # Find the next button and update the query parameters to go to the next page
        next_button = soup.select_one('button.btn-default[data-value="next"][data-ew-action="redirect"]')
        print('NEXT BUTTON', next_button)
        if next_button:
            next_url = next_button['data-url']
            params = {
                'recperpage': 100,
                'search': '',
                **dict(q.split('=') for q in next_url.split('?')[-1].split('&'))
            }
        else:
            break
