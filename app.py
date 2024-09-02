from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.exchange-rates.org/exchange-rate-history/usd-idr')
soup = BeautifulSoup(url_get.content,"html.parser")

#find your right key here
table = soup.find('section', attrs={'class':'box history-rates-table-box'})
usdrates = table.find_all('tr')
row_length = len(usdrates)

temp = [] #initiating a list 

for i in range(1, row_length):
#insert the scrapping process here
    try: 
        time = usdrates[i].find('a', attrs={'class':'n'}).text
        price = usdrates[i].find('span', attrs={'class':'w'}).text
        temp.append((time, price))
    except:
        pass

temp = temp[::-1]

#change into dataframe
data = pd.DataFrame(temp)
data.rename(columns= {0: 'date',
                    1 : 'exchange_rates'},
                    inplace= True)


#insert data wrangling here
data['exchange_rates'] = data['exchange_rates'].str.replace("1 USD = ","")
data['exchange_rates'] = data['exchange_rates'].str.replace(" IDR","")
data['exchange_rates'] = data['exchange_rates'].str.replace(",","")
data['exchange_rates'] = data['exchange_rates'].astype('float64')
data['date'] = data['date'].astype('datetime64[ns]')

data = data.set_index('date')

#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{data["exchange_rates"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	ax = data.plot(figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)