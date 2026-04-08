import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

def urlToMarkup(url):
    html_data = requests.get(url).content
    return bs(html_data, 'html.parser')

def writeCSV(data, file_name):
    data_obj = pd.DataFrame(data)
    data_obj.to_csv(file_name, index=False)
    print(f"Data successfully written to {file_name}")

def main():
    webpage_list = []
    webpage_url = "https://www.tickertape.in/stocks?filter="
    webpage_dirs = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'others']
    stock_data = []

    print("Starting to collect data from webpages...")
    
    for directory in webpage_dirs:
        url = webpage_url + directory
        markup_data = urlToMarkup(url)
        anchor_tags = markup_data.find_all("a", {'class': 'jsx-1528870203'}) if directory not in ['i', 's', 'others'] else markup_data.find_all("a")

        for tag in anchor_tags:
            try:
                href = tag.get('href')  # Extract 'href' attribute
                if href:  # Only proceed if 'href' is not None
                    path_url = "https://www.tickertape.in" + href + "?checklist=basic"
                    if path_url not in webpage_list and '/stocks/' in path_url:
                        webpage_list.append(path_url)
                        print(f"Found URL: {path_url}")
            except Exception as e:
                print(f"Error processing webpage link: {e}")

    print(f"Total URLs collected: {len(webpage_list)}")

    for url in webpage_list:
        web_data = urlToMarkup(url)
        try:
            # Safely check for the stock elements, ensuring they are not None
            icr = web_data.find_all("span", {'class': ['jsx-1803365110', 'stock-label-title']})
            string = "".join([w.text for w in icr]) if icr else 'N/A'
            
            # Check if the elements exist before accessing `.text`
            stock_symbol_elem = web_data.find("span", {'class': 'text-light'})
            stock_symbol = stock_symbol_elem.text if stock_symbol_elem else 'N/A'
            
            stock_name_elem = web_data.find("h1", {'class': 'stock-name'})
            stock_name = stock_name_elem.text if stock_name_elem else 'N/A'
            
            stock_industry = icr[0].text if icr and len(icr) > 0 and len(icr[0].text) > 2 else 'N/A'
            
            stock_market_cap = ('Smallcap' if 'Smallcap' in string else
                                'Midcap' if 'Midcap' in string else
                                'Largecap' if 'Largecap' in string else 'nocap')
            stock_risk_level = ('Low Risk' if 'Low Risk' in string else
                                'Moderate Risk' if 'Moderate Risk' in string else 'High Risk')

            stock_data.append({
                'stock_symbol': stock_symbol,
                'stock_name': stock_name,
                'stock_industry': stock_industry,
                'stock_market_cap': stock_market_cap,
                'stock_risk_level': stock_risk_level,
                'stock_ticker_url': url
            })
            print(f"Added stock: {stock_name} | {stock_symbol}")
        except Exception as e:
            print(f"Error processing webpage data: {e}")

    print(f"Total stocks processed: {len(stock_data)}")

    writeCSV(stock_data, 'stockDataset_v1.csv')

if __name__ == "__main__":
    main()
