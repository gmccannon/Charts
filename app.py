from flask import Flask, render_template
import plotly.graph_objects as go
import pandas as pd
from yfinance import download
from datetime import datetime, timedelta
import pandas_market_calendars as mcal

app = Flask(__name__)

# Get today's date
TODAY = datetime.now().date()

# Get the NYSE calendar
NYSE = mcal.get_calendar('XNYS')

#get the date information by filtering non open days
CANDLE_PERIOD = 180
MARKET_OPEN_DAYS = [day.date().strftime('%Y-%m-%d') for day in NYSE.valid_days(end_date=TODAY, start_date=TODAY - timedelta(days=CANDLE_PERIOD))]
NUMER_OF_OPEN_DAYS = len(MARKET_OPEN_DAYS)

#sanmple ticker
INPUT_TICKER = "AAPL"

# Sample stock data
ticker_info = download(INPUT_TICKER, period='1y', interval='1d')
data = {
    'Date': MARKET_OPEN_DAYS,
    'Open': [ticker_info['Open'].iloc[i] for i in range(-NUMER_OF_OPEN_DAYS, 0, 1)],
    'High': [ticker_info['High'].iloc[i] for i in range(-NUMER_OF_OPEN_DAYS, 0, 1)],
    'Low': [ticker_info['Low'].iloc[i] for i in range(-NUMER_OF_OPEN_DAYS, 0, 1)],
    'Close': [ticker_info['Close'].iloc[i] for i in range(-NUMER_OF_OPEN_DAYS, 0, 1)],
}

df = pd.DataFrame(data)
df['Date'] = pd.to_datetime(df['Date'])


def generate_candlestick_chart():
    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                          open=df['Open'],
                                          high=df['High'],
                                          low=df['Low'],
                                          close=df['Close'])])

    # Customize the layout
    fig.update_layout(
        title=INPUT_TICKER + ' Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )

    # Convert the Plotly chart to HTML
    return fig.to_html(full_html=True)


def generate_info_table():
    info_table = [
        ['Row 1, Column 1', 'Row 1, Column 2'],
        ['Row 2, Column 1', 'Row 2, Column 2'],
        ['Row 3, Column 1', 'Row 3, Column 2'],
        ['Row 4, Column 1', 'Row 4, Column 2'],
        ['Row 5, Column 1', 'Row 5, Column 2'],
    ]
    return info_table


@app.route('/')
def index():
    return render_template('index.html', candlestick_chart=generate_candlestick_chart(), info_table=generate_info_table(), INPUT_TICKER=INPUT_TICKER)


if __name__ == '__main__':
    app.run(debug=True)
