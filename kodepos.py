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
params["x_Propinsi"] = str('31')
params["x_Kabupaten"] = str('31.71')
params["x_Kecamatan"] = str('31.71.01')

# function to retrieve data from a single page
def get_data_from_page(url, params):
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
            data.append({'kode' : cols[9].text.strip()})

        # Find the next button and update the query parameters to go to the next page
        next_button = soup.select_one('button.btn-default[data-value="next"][data-ew-action="redirect"]')
        print('NEXT BUTTON', next_button)
        if next_button:
            next_url = next_button['data-url']
            params = {
                'recperpage': 100,
                **dict(q.split('=') for q in next_url.split('?')[-1].split('&'))
            }
            params["x_Propinsi"] = str('31')
            params["x_Kabupaten"] = str('31.71')
            params["x_Kecamatan"] = str('31.71.01')
        else:
            break

    return data




# set the list to hold all data
all_data = []
data=get_data_from_page(url, params)
all_data.extend(data)
# loop over all possible combinations of search parameters
# for propinsi in range(1, 35):
#     for kabupaten in range(1, 500):
#         for kecamatan in range(1, 500):
#             search_params["x_Propinsi"] = str(propinsi)
#             search_params["x_Kabupaten"] = "{:02d}".format(kabupaten)
#             search_params["x_Kecamatan"] = "{:02d}.{:02d}".format(kabupaten, kecamatan)
#             response = requests.get(url, params=search_params)
#             soup = BeautifulSoup(response.content, "html.parser")
#             pager = soup.find("div", {"class": "paging"})
#             if pager is not None:
#                 num_pages = len(pager.findAll("a")) - 2
#             else:
#                 num_pages = 1
#             for page in range(1, num_pages + 1):
#                 search_params["page"] = str(page)
#                 data = get_data_from_page(url, search_params)
#                 all_data.extend(data)
#                 print("Scraped page {} of {} for propinsi {}, kabupaten {:02d}, kecamatan {:02d}".format(
#                     page, num_pages, propinsi, kabupaten, kecamatan))

# save the data to a JSON file
# with open("kode_pos.json", "w") as outfile:
#     json.dump(all_data, outfile)

with open('kodepos.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    writer.writerow(['Kode'])

    for i in range(len(all_data)):
        kode = all_data[i]['kode']
        writer.writerow([kode])

print("Finished scraping {} pages".format(len(all_data)))
