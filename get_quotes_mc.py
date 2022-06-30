import bs4 as bs
import requests
import csv
import pandas as pd

# function to get the links of all the alphabetical pages on index url and get all the quotes and their link on mc
def get_quotes():
	index_url = "https://www.moneycontrol.com/india/stockpricequote/"

	resp = requests.get(index_url)  # used for reponse - 200 OK
	soup = bs.BeautifulSoup(resp.text, 'lxml')  # parse using bs4
	page_div = soup.find('div', {'class': 'MT2 PA10 brdb4px alph_pagn'})  # find the div where all the alphabets and links are present
	page_elements = page_div.find_all('a')  # get all the links from the div

	pages = {}  # dict to store all the links with key as the title on the website

	for element in page_elements:
		pages[element.get('title')] = 'https://www.moneycontrol.com' + element.get('href')  # appending every link to the dictionary

	stocks = {}   #dict to save all the quotes and their mc link

	for i in list(pages.keys())[1:]:  # iterating over every page to get the quotes and their links
		print(pages[i])
		resp = requests.get(pages[i])
		soup = bs.BeautifulSoup(resp.text, 'lxml')
		table = soup.find('table', {'class': 'pcq_tbl MT10'})  # get the table containig all the quotes in the particular page


		for stock in table.find_all('td'):  # iterate over every table data in table on page
			links = stock.find_all('a')  # getting 'a' tag from the table data
			for link in links:  # iterating over the 'a' tags found in the previous step
				# need to use get_text() to get the value of the 'a' tag
				stocks[link.get_text()] = link.get('href')  # saving the data in the dictionary

	data = pd.DataFrame(stocks.items(), columns=['Quote', 'Link'])

	return data
	
if __name__ == "__main__":
	data = get_quotes()
	print(data.head())
	print(data.tail())
	data.to_csv('quotes.csv')