import requests
from bs4 import BeautifulSoup
import yfinance as yf
import os

companies = [
    # 'NASDAQ:AAPL',
    # 'NYSE:ABBV',
    # 'NYSE:ABT',
    # 'NYSE:ACN',
    # 'NASDAQ:ADBE',
    # 'NYSE:AIG',
    # 'NASDAQ:AMD',
    # 'NASDAQ:AMGN',
    # 'NYSE:AMT',
    # 'NASDAQ:AMZN',
    # 'NASDAQ:AVGO',
    # 'NYSE:AXP',
    # 'NYSE:BA',
    # 'NYSE:BAC',
    # 'NYSE:BK',
    # 'NASDAQ:BKNG',
    # 'NYSE:BLK',
    # 'NYSE:BMY',
    # 'NYSE:BRK.B', # has no earning transcripts
    # 'NYSE:C',
    # 'NYSE:CAT',
    # 'NASDAQ:CHTR',
    # 'NYSE:CL',
    # 'NASDAQ:CMCSA',
    # 'NYSE:COF',
    # 'NYSE:COP',
    # 'NASDAQ:COST',
    # 'NYSE:CRM',
    # 'NASDAQ:CSCO',
    # 'NYSE:CVS',
    # 'NYSE:CVX',
    # 'NYSE:DHR',
    # 'NYSE:DIS',
    # 'NYSE:DOW',
    # 'NYSE:DUK',
    # 'NYSE:EMR',
    # 'NASDAQ:EXC',
    # 'NYSE:F',
    # 'NYSE:FDX',
    # 'NYSE:GD',
    # 'NYSE:GE',
    # 'NASDAQ:GILD',
    # 'NYSE:GM',
    # 'NASDAQ:GOOG',
    # 'NASDAQ:GOOGL',
    # 'NYSE:GS',
    # 'NYSE:HD',
    # 'NASDAQ:HON',
    # 'NYSE:IBM',
    # 'NASDAQ:INTC',
    # 'NYSE:JNJ',
    # 'NYSE:JPM',
    # 'NASDAQ:KHC',
    # 'NYSE:KO',
    # 'NYSE:LIN',
    # 'NYSE:LLY',
    # 'NYSE:LMT',
    # 'NYSE:LOW',
    # 'NYSE:MA',
    # 'NYSE:MCD',
    # 'NASDAQ:MDLZ',
    # 'NYSE:MDT',
    # 'NYSE:MET',
    # 'NASDAQ:META',
    # 'NYSE:MMM',
    # 'NYSE:MO',
    # 'NYSE:MRK',
    # 'NYSE:MS',
    # 'NASDAQ:MSFT',
    # 'NYSE:NEE',
    # 'NASDAQ:NFLX',
    # 'NYSE:NKE',
    # 'NASDAQ:NVDA',
    # 'NYSE:ORCL',
    # 'NASDAQ:PEP',
    # 'NYSE:PFE',
    # 'NYSE:PG',
    # 'NYSE:PM',
    # 'NASDAQ:PYPL',
    # 'NASDAQ:QCOM',
    # 'NYSE:RTX',
    # 'NASDAQ:SBUX',
    # 'NYSE:SCHW', # has no earning transcripts
    # 'NYSE:SO',
    # 'NYSE:SPG',
    # 'NYSE:T',
    # 'NYSE:TGT',
    # 'NYSE:TMO',
    # 'NASDAQ:TMUS',
    # 'NASDAQ:TSLA',
    # 'NASDAQ:TXN',
    # 'NYSE:UNH',
    # 'NYSE:UNP',
    # 'NYSE:UPS',
    # 'NYSE:USB',
    # 'NYSE:V',
    # 'NYSE:VZ',
    # 'NASDAQ:WBA',
    # 'NYSE:WFC',
    # 'NYSE:WMT',
    'NYSE:XOM'
]

all_transcript_links = []

for company in companies:
    exchange = company.split(':')[0]
    ticker = company.split(':')[1]

    # print(exchange + " " + ticker)

    url = "https://www.fool.com/quote/" + exchange + "/" + ticker + "/"
    base_url = "https://fool.com"

    print(url)

    # Send a GET request to the URL and retrieve the webpage content
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        quote_earnings_div = soup.find("div", id="quote-earnings-transcripts")
        transcripts_div = quote_earnings_div.find("div", id="earnings-transcript-container")

        # page = 1
        if transcripts_div is not None:
            page_div = transcripts_div.find("div", class_="page", attrs={"data-pagenum": "1"})

            if page_div is not None:
                transcript_links = page_div.find_all("a")

                button = quote_earnings_div.find("button", class_="load-more-button")
                if button is None:
                    print("button is none")
                    for link in transcript_links:
                        length = len(link["href"])
                        transcript_url = "fool.com" + link["href"][2:length-4]
                        all_transcript_links.append(transcript_url)
                        transcript_title = link.get_text()

                    exit
                
                data_per_page = button["data-per-page"]
                data_total = button["data-total"]
                data_container_id = button["data-container-id"]
                data_url = button["data-url"]

                ajax_url = base_url + data_url

                # Simulate button clicks until all links are loaded
                while len(transcript_links) < int(data_total):
                    # Construct the URL for the AJAX request
                    ajax_url = base_url + data_url
                    
                    # Send a GET request to the AJAX URL
                    ajax_response = requests.get(ajax_url)
                    ajax_soup = BeautifulSoup(ajax_response.content, "html.parser")

                    # Update the button details for the next AJAX request
                    button = ajax_soup.find("button", class_="load-more-button")
                    if button is not None:
                        data_url = button.get("data-url")
                    else:
                        transcript_links = ajax_soup.find_all("a")
                        break

                for link in transcript_links:
                    length = len(link["href"])
                    transcript_url = "fool.com" + link["href"][2:length-4]
                    all_transcript_links.append(transcript_url)
                    transcript_title = link.get_text()

                    # print("Transcript URL:", transcript_url)
                    # print("Transcript Title:", transcript_title)
                    # print("-----------------------------------")

                # page += 1
                # page_div = transcripts_div.find("div", class_="page", attrs={"data-pagenum": str(page)})

                # print(len(transcript_links))
                # print(int(data_total))

            else:
                print("Child div with class 'page' and data-pagenum='1' not found.")
        else:
            print("Earning transcripts div not found on the webpage.")
            
    except Exception as e:
        print("An error occurred:", e)

print(len(all_transcript_links))

for link in all_transcript_links:
    print(link)

file_name = "earning_transcripts.txt"
ticker_folder = f"{ticker}"
os.makedirs(ticker_folder, exist_ok=True)
index = 0
length = len(all_transcript_links)

year_recent_folder = "2023"
year_recent_path = os.path.join(ticker_folder, year_recent_folder)
os.makedirs(year_recent_path, exist_ok=True)
year_recent_file_path = os.path.join(year_recent_path, file_name)
with open(year_recent_file_path, "w") as file:
    for count in range(0, 1):
        file.write(f"{all_transcript_links[index]}\n")
        index += 1

for year in range(2022, 2018, -1):
    year_folder = f"{year}"
    year_path = os.path.join(ticker_folder, year_folder)
    os.makedirs(year_path, exist_ok=True)
    year_file_path = os.path.join(year_path, file_name)
    with open(year_file_path, "w") as file:
        top = 5
        # if year == 2022:
            # top = 2
        # if year == 2021:
            # top = 2
        # if year == 2020:
            # top = 1
        # if year == 2019:
            # top = 2
        # if year == 2018:
            # top = 3
        for count in range(1, top):
            if index < length:
                file.write(f"{all_transcript_links[index]}\n")
            index += 1

year_2018_folder = "2018"
year_2018_path = os.path.join(ticker_folder, year_2018_folder)
os.makedirs(year_2018_path, exist_ok=True)
year_2018_file_path = os.path.join(year_2018_path, file_name)
with open(year_2018_file_path, "w") as file:
    for link in all_transcript_links[index:]:
        file.write(f"{link}\n")

all_links_file_name = "all_earning_transcripts.txt"
all_links_file_path = os.path.join(ticker_folder, all_links_file_name)
with open(all_links_file_path, "w") as file:
    for link in all_transcript_links:
        file.write(f"{link}\n")
