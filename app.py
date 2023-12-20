from flask import Flask, render_template
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__)

# Sample stock data
data = {
    'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04'],
    'Open': [100, 105, 98, 102],
    'High': [110, 112, 100, 105],
    'Low': [95, 98, 92, 98],
    'Close': [105, 100, 95, 100],
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
        title='Stock Candlestick Chart',
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
