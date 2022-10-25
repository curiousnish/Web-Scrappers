import pandas as pd
import bs4 as bs
import requests
# from stock_quotes_mc import get_quotes


def get_urls(company):
    data = pd.read_csv("quotes.csv")  # read every quote and get their link
    data.set_index('Quote', inplace=True)  # setting the index as the quote
    # dropping the unused index column
    data.drop("Unnamed: 0", axis=1, inplace=True)
    link = data.loc[str(company), 'Link']  # getting the link of the quote

    resp = requests.get(link)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    # finding the div with all the financial reports links
    div = soup.find('div', {'class': 'quick_links clearfix'})
    fin_links = {}
    for fin_link in div.find_all('a'):
        # creating a dictionary with all the links of the financial reports
        fin_links[fin_link.get('title')] = fin_link.get('href')

    bs_url = fin_links['Balance Sheet']  # getting the link for the bs
    is_url = fin_links['Profit & Loss']  # getting the link for the is
    cf_url = fin_links['Cash Flows']  # getting the link for the cf

    return bs_url, is_url, cf_url

# # getting the urls
# def get_urls(stock):
#     stocks = get_quotes()
#     stock_url = stocks[stock]
#     resp = requests.get(stock_url)
#     soup = bs.BeautifulSoup(resp.text, 'lxml')
#     div = soup.find('div', {'class': 'quick_links clearfix'})
#     links = {}
#     for link in div.findAll('a'):
#         links[link.get('title')] = link.get('href')

#     bs_url = links['Balance Sheet']
#     is_url = links['Profit & Loss']
#     cf_url = links['Cash Flows']
#     return bs_url, is_url, cf_url

# get income statement


def get_is(is_url):
    resp = requests.get(is_url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'mctable1'})
    table_rows = table.find_all('tr')

    l = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        l.append(row)

    df = pd.DataFrame(l)
    df.to_excel("Income Statement.xlsx")

# get balance sheet


def get_bs(bs_url):
    resp = requests.get(bs_url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'mctable1'})
    table_rows = table.find_all('tr')

    l = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        l.append(row)

    df = pd.DataFrame(l)
    df.to_excel("Balance_Sheet.xlsx")

# get cash flow statement


def get_cf(cf_url):
    resp = requests.get(cf_url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'mctable1'})
    table_rows = table.find_all('tr')

    l = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        l.append(row)

    df = pd.DataFrame(l)
    df.to_excel("Cash_Flow.xlsx")


if __name__ == "__main__":
    bs_url, is_url, cf_url = get_urls('Sirca Paints')
    get_is(is_url)
    get_bs(bs_url)
    get_cf(cf_url)
