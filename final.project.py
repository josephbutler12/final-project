# cd data_3500_code
# git add
# git commit
# git push

import requests
import json

def simpleMovingAvg(prices, ticker):
    print(ticker, "Simple Moving Average Strategy Output:")
    i = 0
    buy = 0
    total_profit = 0
    first_buy = None  
    signal_today = None

    for price in prices:
        if i >= 5: 
            current_price = price
            avg_price = sum(prices[i - 5:i]) / 5  

            if current_price > avg_price and buy == 0:
                buy = current_price
                if first_buy is None and buy != 0:
                    first_buy = buy

            elif current_price < avg_price and buy != 0:
                trade_profit = current_price - buy
                total_profit += trade_profit
                buy = 0  

        i += 1

    percent_return = (total_profit / first_buy) * 100 if first_buy else 0

    if signal_today:
        print(f"You should {signal_today} {ticker} today (SMA Strategy)")
        
    return total_profit, percent_return  

def meanReversionStrat(prices, ticker):
    print(ticker, "Mean Reversion Strategy Output:")
    i = 0
    buy = 0
    total_profit = 0
    first_buy = None  
    signal_today = None

    for price in prices:
        if i >= 5: 
            current_price = price
            avg_price = sum(prices[i - 5:i]) / 5  #the [i - 5:i] is super efficient. Cool we can do that

            if current_price < avg_price * 0.98 and buy == 0:
                buy = current_price
                if first_buy is None and buy != 0:
                    first_buy = buy

            elif current_price > avg_price * 1.02 and buy != 0:
                trade_profit = current_price - buy
                total_profit += trade_profit
                buy = 0  

        i += 1

    percent_return = (total_profit / first_buy) * 100 if first_buy else 0

    if signal_today:
        print(f"You should {signal_today} {ticker} today (MR Strategy)")

    return total_profit, percent_return  

def bollingerBands(prices, ticker):
    i = 0
    buy = 0
    total_profit = 0
    first_buy = None  
    signal_today = None

    for price in prices:
        if i >= 5: 
            current_price = price
            avg_price = sum(prices[i - 5:i]) / 5  

            if current_price > avg_price * 1.05 and buy == 0:
                buy = current_price
                if first_buy is None and buy != 0:
                    first_buy = buy

            elif current_price < avg_price * 0.95 and buy != 0:
                trade_profit = current_price - buy
                total_profit += trade_profit
                buy = 0  

        i += 1

    percent_return = (total_profit / first_buy) * 100 if first_buy else 0

    if signal_today:
        print(f"You should {signal_today} {ticker} today (BB Strategy)")

    return total_profit, percent_return

def saveResults(dictionary): 
    print(dictionary)
    with open('/home/ubuntu/final_project/results.json', 'w') as f:  
        json.dump(dictionary, f, indent=4)

def initialDataPull(tickers): 
    for ticker in tickers:

        url = ('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&outputsize=full&apikey=NG9C9EPVYBMQT0C8')

        # making API call
        request = requests.get(url)
        request_dictionary = json.loads(request.text)

        # keys
        key_0 = 'Time Series (Daily)'
        # key_1 = '2025-04-08' I need every date
        key_2 = '4. close'

        # print(request_dictionary[key_0][key_1][key_2])
        # print(request_dictionary[key_0].keys())

        lines = []


        for date in request_dictionary[key_0].keys():
            lines.append(date +','+ request_dictionary[key_0][date][key_2] + '\n')

        # reverse the lines so it's not backwards
        lines = lines[::-1]

        with open('/home/ubuntu/final_project/final.project.py'+ticker+'.csv', 'w') as file:
            file.writelines(lines)

def appendData(tickers):
    for ticker in tickers:

        url = ('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol='+ticker+'&outputsize=full&apikey=NG9C9EPVYBMQT0C8')

        # making API call
        request = requests.get(url)
        request_dictionary = json.loads(request.text)

        #send request to API
        #grab relevant data

        #need same key value pairs as initial data pull

        key_0 = 'Time Series (Daily)'
        # key_1 = '2025-04-08' I need every date
        key_2 = '4. close'

        existing_dates = set()
        with open(f'/home/ubuntu/final_project/final.project.py{ticker}.csv', 'r') as file:
            for line in file:
                if line.strip():  # skip blank lines
                    date = line.strip().split(',')[0]
                    existing_dates.add(date)

        new_lines = []

        for date in sorted(request_dictionary[key_0].keys()):
            if date not in existing_dates:
                new_lines.append(date +','+ request_dictionary[key_0][date][key_2] + '\n')

        if new_lines:
        #add new data
            with open('/home/ubuntu/final_project/final.project.py'+ticker+'.csv', 'a') as file:
                file.writelines(new_lines)


def list_maker(ticker):
    filename = f"/home/ubuntu/final_project/final.project.py{ticker}.csv"
    prices = []

    with open(filename, 'r') as file:
        csv_lines = file.readlines()

    for line in csv_lines:
        parts = line.strip().split(',')
        if len(parts) < 2:
            print(f"Skipping malformed line in {ticker}: {line.strip()}")
            continue
        try:
            price = float(parts[1].strip())
            prices.append(price)
        except ValueError:
            print(f"Skipping non-numeric value in {ticker}: {line.strip()}")
            continue

    return prices

def find_highest_return(results):
    max_return = 0
    best_ticker = None
    best_strategy = None

    # Define strategies to check
    strategies = ['SMA_returns', 'MR_returns', 'BB_returns']

    for key, value in results.items():
        # Check if the key ends with a returns category
        for strategy in strategies:
            if key.endswith(strategy):
                if value > max_return:
                    max_return = value
                    best_ticker = key.split('_')[0]  # Extract ticker from key
                    best_strategy = strategy.replace('_returns', '')  # Extract strategy name

    return best_ticker, best_strategy, max_return


#initializing variables we'll need through the code:
results = {}
tickers = ['AAPL', 'GOOG', 'HAS', 'NKE', 'NVDA', 'PLTR', 'SCHD', 'SPXL', 'TQQQ', 'TSLA']

#initialDataPull(tickers) #once all data is in, comment this line out
appendData(tickers)


for ticker in tickers:
    
    prices = list_maker(ticker)

    MR_profit, MR_returns = meanReversionStrat(prices, ticker)
    SMA_profit, SMA_returns = simpleMovingAvg(prices, ticker)
    BB_profit, BB_returns = bollingerBands(prices, ticker)

    #results[f"{ticker}_prices"] = prices
    results[f"{ticker}_SMA_profit"] = SMA_profit
    results[f"{ticker}_SMA_returns"] = SMA_returns
    results[f"{ticker}_MR_profit"] = MR_profit
    results[f"{ticker}_MR_returns"] = MR_returns 
    results[f"{ticker}_BB_profit"] = BB_profit
    results[f"{ticker}_BB_returns"] = BB_returns 


best_ticker, best_strategy, max_return = find_highest_return(results)
results['best_strategy'] = {
'ticker': best_ticker,
'strategy': best_strategy,
'return': max_return}

saveResults(results) 




