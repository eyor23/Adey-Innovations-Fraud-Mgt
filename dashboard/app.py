from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load the dataset
data = pd.read_csv(r'C:\Users\user\Desktop\Kifiya\Adey-Innovations-Fraud-Mgt\data\preprocessed_data.csv')

# Calculate summary statistics
def get_summary_statistics():
    total_transactions = len(data)
    total_fraud_cases = len(data[data['class'] == 1])
    fraud_percentage = total_fraud_cases / total_transactions * 100
    return {
        'total_transactions': total_transactions,
        'total_fraud_cases': total_fraud_cases,
        'fraud_percentage': fraud_percentage
    }

# API endpoint to get summary statistics
@app.route('/summary')
def summary():
    summary_stats = get_summary_statistics()
    return jsonify(summary_stats)

# API endpoint to get fraud trends over time
@app.route('/fraud_trends')
def fraud_trends():
    fraud_trends_data = data[data['class'] == 1].groupby('purchase_time').size().reset_index(name='fraud_cases')
    return fraud_trends_data.to_json(orient='records')

if __name__ == "__main__":
    app.run(debug=True)
