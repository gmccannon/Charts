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

# Sample stock data
ticker_info = download("AAPL", period='1y', interval='1d')
data = {
    'Date': MARKET_OPEN_DAYS,
    'Open': [ticker_info['Open'].iloc[i] for i in range(-1, -NUMER_OF_OPEN_DAYS - 1, -1)],
    'High': [ticker_info['High'].iloc[i] for i in range(-1, -NUMER_OF_OPEN_DAYS - 1, -1)],
    'Low': [ticker_info['Low'].iloc[i] for i in range(-1, -NUMER_OF_OPEN_DAYS - 1, -1)],
    'Close': [ticker_info['Close'].iloc[i] for i in range(-1, -NUMER_OF_OPEN_DAYS - 1, -1)],
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
        title='AAPL Candlestick Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False
    )

    # Convert the Plotly chart to HTML
    chart_html = fig.to_html(full_html=False)

    return chart_html

@app.route('/')
def index():
    # Generate Plotly candlestick chart
    candlestick_chart = generate_candlestick_chart()

    return render_template('index.html', candlestick_chart=candlestick_chart)

if __name__ == '__main__':
    app.run(debug=True)
