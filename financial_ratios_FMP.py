import requests
import bs4 as bs
import pickle
import pandas as pd

def get_ratios(stock):
    ratio_url = "https://financialmodelingprep.com/financial-ratios/{}"
    stock = stock

    resp = requests.get(ratio_url.format(stock))
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    tables = soup.findAll('table', {'class': 'table table-striped table-sort'})

    h3 = soup.findAll('h3')
    i = 1

    ratios = {}

    for table in tables:
        ratio_name = h3[i].text

        ratios[ratio_name] = {}

        for row in table.findAll('tr'):
            ratio = row.findAll('td')[0].text
            ratios[ratio_name][ratio] = row.findAll('td')[2].text

        i += 1
        
    print(ratios)
    return ratios


get_ratios("NTPC.NS")

def to_dataframe():
    ratios = get_ratios("TATASTEEL.NS")
    df = pd.DataFrame.from_dict({(i, j): ratios[i][j]
                                for i in ratios.keys()
                                for j in ratios[i].keys()},
                                orient='index')
    df.reset_index(inplace=True)
    ratio_type = []
    ratio = []

    for i in range(len(df)):
        lst = df['index'].to_list()
        ratio_type.append(lst[i][0])
        ratio.append(lst[i][1])

    df['ratio_type'] = ratio_type
    df['ratio'] = ratio
    df.drop('index', axis=1, inplace=True)
    df.columns = ["Value", "Ratio_Type", "Ratio"]
    df.set_index(['Ratio_Type', 'Ratio'], inplace=True)
    df.to_csv("ratios.csv")
    print(df)
    return df

# to_dataframe()

