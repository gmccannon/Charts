from flask import Flask, render_template, request
from plotly.graph_objects import Figure, Candlestick
from pandas import DataFrame, to_datetime
from yfinance import download, Ticker
from datetime import datetime, timedelta
from pandas_market_calendars import get_calendar
from number_formatting import format_large_number

app = Flask(__name__)

#default values
INPUT_TICKER = "QQQ"
TICKER_INFO = download(INPUT_TICKER, period='1y', interval='1d')

def generate_candlestick_chart():
    # Get today's date
    today = datetime.now().date()

    # Get the nyse calendar
    nyse = get_calendar('XNYS')

    #get the date information by filtering non open days, half year time frame
    candle_period = 180
    market_open_days = [day.date().strftime('%Y-%m-%d') for day in nyse.valid_days(end_date=today, start_date=today - timedelta(days=candle_period))]
    number_open_days = len(market_open_days)
    
    try:
        # get specific stock price data
        data = {
        'Date': market_open_days,
        'Open': [TICKER_INFO['Open'].iloc[i] for i in range(-number_open_days, 0, 1)],
        'High': [TICKER_INFO['High'].iloc[i] for i in range(-number_open_days, 0, 1)],
        'Low': [TICKER_INFO['Low'].iloc[i] for i in range(-number_open_days, 0, 1)],
        'Close': [TICKER_INFO['Close'].iloc[i] for i in range(-number_open_days, 0, 1)],
        }

        df = DataFrame(data)
        df['Date'] = to_datetime(df['Date'])

        # Create candlestick chart
        fig = Figure(data=[Candlestick(x=df['Date'],
                                            open=df['Open'],
                                            high=df['High'],
                                            low=df['Low'],
                                            close=df['Close'])])

        # Customize the layout
        fig.update_layout(
            title= f"{INPUT_TICKER} - {Ticker(INPUT_TICKER).info.get('longName', '')}",
            xaxis_title='Date',
            yaxis_title='Price',
            xaxis_rangeslider_visible=False
        )
    except:
        return "Invalid ticker"

    # Convert the Plotly chart to HTML
    return fig.to_html(full_html=True)


def generate_info_table():
    try:
        # Create a Ticker object for the specified stock
        ticker_object = Ticker(INPUT_TICKER)

        foward_eps = ticker_object.info.get('forwardPE', 0)
        trailing_eps = ticker_object.info.get('trailingEps', 0)
        pe_ratio = ticker_object.info.get('trailingPE', 0)
        beta = ticker_object.info.get('beta', 0)

        price_open = TICKER_INFO['Open'].iloc[-1]
        price_close = TICKER_INFO['Close'].iloc[-1]
        price_high = TICKER_INFO['High'].iloc[-1]
        price_low = TICKER_INFO['Low'].iloc[-1]
        
        sector = ticker_object.info.get('sector', 'Not available')
        industry = ticker_object.info.get('industry', 'Not available')
        market_cap = ticker_object.info.get('marketCap', 0)
        dividend_yield = ticker_object.info.get('dividendYield', 0)


        info_table = [
            [f"Today's Open: ${price_open:.2f}", f"Trailing EPS: {trailing_eps} E/S", f"Sector: {sector}"],
            [f"Today's Close: ${price_close:.2f}", f"Foward PE: {foward_eps} P/E", f"Industry: {industry}"],
            [f"Today's High: ${price_high:.2f}", f"Trailing PE: {pe_ratio} P/E", f"Market Cap: ${format_large_number(market_cap)}"],
            [f"Today's Low: ${price_low:.2f}", f"Dvidend Yield: {(100*dividend_yield):.2f}%", f"Beta: {beta}"],
        ]
    except:
        info_table = [ ['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0'] ]
        return info_table

    return info_table


@app.route('/', methods=['GET', 'POST'])
def index():

    global INPUT_TICKER
    global TICKER_INFO
    # Update based on the form submission
    if request.method == 'POST':
        INPUT_TICKER = request.form['input_value'].upper()
        TICKER_INFO = download(INPUT_TICKER, period='1y', interval='1d')
    
    return render_template('index.html', 
        candlestick_chart=generate_candlestick_chart(), 
        info_table=generate_info_table()
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
