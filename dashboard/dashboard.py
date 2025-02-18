import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import requests

# Initialize Dash app
app = dash.Dash(__name__)

# Fetch summary statistics from Flask backend
summary_stats = requests.get('http://127.0.0.1:5000/summary').json()

# Fetch fraud trends data from Flask backend
fraud_trends = requests.get('http://127.0.0.1:5000/fraud_trends').json()
fraud_trends_df = pd.DataFrame(fraud_trends)

# Create summary boxes
summary_boxes = html.Div([
    html.Div([
        html.H3('Total Transactions'),
        html.P(summary_stats['total_transactions'])
    ]),
    html.Div([
        html.H3('Total Fraud Cases'),
        html.P(summary_stats['total_fraud_cases'])
    ]),
    html.Div([
        html.H3('Fraud Percentage'),
        html.P(f"{summary_stats['fraud_percentage']:.2f}%")
    ])
])

# Create line chart for fraud trends
line_chart = dcc.Graph(
    id='fraud_trends',
    figure=px.line(fraud_trends_df, x='purchase_time', y='fraud_cases', title='Fraud Cases Over Time')
)

# Layout of the dashboard
app.layout = html.Div([
    summary_boxes,
    line_chart
])

if __name__ == '__main__':
    app.run_server(debug=True)
