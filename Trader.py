from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import matplotlib.pyplot as plt
from api_key import APIKey
import numpy as np
from scipy.signal import find_peaks

class Trader:
	SIZE_DATA = 390
	def __init__(self, key, symbol,amount=10000, trade_limit = 0.1):
		self.key = key
		self.amount = amount
		self.symbol = symbol
		self.buying = True
		self.trade_limit = trade_limit
		self.holdings = {}	#num shares, price per share tuple in these
		self.sma_5s = []
		self.sma_13s = []
	def decide(self, df, curr_shareprice, i):
		sma_5 = self.get_sma(df, 15)
		self.sma_5s.append(sma_5)

		sma_13 = self.get_sma(df, 42)
		self.sma_13s.append(sma_13)

		if df.count()['4. close'] < 42 or self.amount <= 0:
			return False
		if self.buying:
			if sma_5 > sma_13:
				self.buy(curr_shareprice)
				return True
		else:
			if sma_5 < sma_13:
				self.sell(curr_shareprice)

				return True

		return False


	def buy(self, curr_shareprice):
		##TRADE!!
		##figure out amount
		purchase_amount = self.amount * self.trade_limit
		print("buying at: ", curr_shareprice)
		self.amount -= purchase_amount
		self.holdings[self.symbol] = purchase_amount/curr_shareprice
		#print("holdings: ", self.amount, self.holdings)

		self.buying = False

	def sell(self, curr_shareprice):
		sell_amount = self.holdings[self.symbol] * curr_shareprice
		print("selling at: ", curr_shareprice)
		self.amount += sell_amount
		self.holdings[self.symbol] = 0
		#print("holdings: ", self.amount, self.holdings)
		self.buying = True


	def get_sma(self, df, n):
		""" uses mean of high and low for datapoint to calculate 
		SMA of df looking back n steps
		"""
		return df['4. close'][-1*n:].mean(axis=0)

	def get_intraday_trading_data(self, key, symbol, interval, outputsize):
	    """get intraday data from alpha vantage using https://github.com/RomelTorres/alpha_vantage

	    :param key: @str - the API key (get from http://www.alphavantage.co/support/#api-key)
	    :param symbol: @str - the stock symbol
	    :param interval: @str - time frequency of trading data. Format: https://www.alphavantage.co/documentation/
	    :return:

	        - data: pandas dataframe with intratrading data updated realtime
	        - metadata: info on data dataframe
	            - formats: https://github.com/RomelTorres/alpha_vantage
	    """
	    ts = TimeSeries(key=key, output_format='pandas')
	    data, meta_data = ts.get_intraday(symbol, interval=interval, outputsize='full')
	    print(data.count()['4. close'] - outputsize)
	    return data[:outputsize], meta_data
