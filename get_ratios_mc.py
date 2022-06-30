import requests
import bs4 as bs
import pandas as pd

# function to get all the links from quote hompage
def get_urls(company):
	data = pd.read_csv("quotes.csv")  # read every quote and get their link
	data.set_index('Quote', inplace=True)  # setting the index as the quote
	data.drop("Unnamed: 0", axis=1, inplace=True)  # dropping the unused index column
	link = data.loc[str(company), 'Link']  # getting the link of the quote

	resp = requests.get(link)  
	soup = bs.BeautifulSoup(resp.text, 'lxml')
	div = soup.find('div', {'class': 'quick_links clearfix'})  # finding the div with all the financial reports links
	fin_links = {}
	for fin_link in div.find_all('a'):
		fin_links[fin_link.get('title')] = fin_link.get('href')  # creating a dictionary with all the links of the financial reports

	ratio_link = fin_links['Ratios']  # getting the link for the ratios

	return ratio_link


# get_urls("Tata Steel")

def get_ratios(company):
	link = get_urls(company)  # get the link from the above function
	resp = requests.get(link)
	soup = bs.BeautifulSoup(resp.text, 'lxml')
	table = soup.find('table', {'class': 'mctable1'}) 
	table_rows = table.find_all('tr')  # finding all the table rows in the ratios table
    
	l = []

	for tr in table_rows:
		td = tr.find_all('td')
		row = [tr.text for tr in td]
		l.append(row)

	df = pd.DataFrame(l)
	df.to_excel("ratios.xlsx")

	print(df)


if __name__ == "__main__":
	get_ratios("Tata Steel")