from api_key import APIKey
from Trader import Trader
import matplotlib.pyplot as plt
SYMBOL = 'GOOGL'
trader = Trader(APIKey.key, SYMBOL)
df = trader.get_intraday_trading_data(APIKey.key, trader.symbol, '1min', Trader.SIZE_DATA)[0]
df = df.reset_index(0)

for i in range(43, 391):

	DF  = df[:i]
	curr_shareprice = DF['4. close'][DF.index[-1]]

	if trader.decide(DF, curr_shareprice, i):
		print(i)
		print('Total: ', trader.amount + trader.holdings[SYMBOL]*curr_shareprice)
print('Total: ', trader.amount + trader.holdings[SYMBOL]*curr_shareprice)

plt.plot(df['4. close'])
plt.plot([None]*42 + trader.sma_5s, label='sma_5s')
plt.plot([None]*42 + trader.sma_13s, label='sma_13s')
plt.show()
