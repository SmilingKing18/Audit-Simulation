from flask import Flask, render_template, request, jsonify
import time
from simulation import generate_invoices

app = Flask(__name__)

# Generate invoices when the server starts
invoices = generate_invoices()

@app.route('/')
def index():
    return render_template('index.html', invoices=invoices)

@app.route('/select_invoice', methods=['POST'])
def select_invoice():
    data = request.json
    invoice_round = data.get('round')
    invoice = next((inv for inv in invoices if inv['round'] == invoice_round), None)
    if invoice:
        if invoice['open_time'] is None:
            invoice['open_time'] = time.time()
        return jsonify(invoice)
    else:
        return jsonify({'error': 'Invoice not found'}), 404

# This endpoint now only records the response (without rating)
@app.route('/record_response', methods=['POST'])
def record_response():
    data = request.json
    invoice_round = data.get('round')
    response_text = data.get('response')
    invoice = next((inv for inv in invoices if inv['round'] == invoice_round), None)
    if invoice:
        if invoice['response'] is None:
            invoice['response'] = response_text
            invoice['response_time'] = time.time()
            duration = invoice['response_time'] - invoice['open_time'] if invoice['open_time'] else None
            return jsonify({'message': 'Response recorded', 'duration': duration})
        else:
            return jsonify({'error': 'Response already recorded'}), 400
    else:
        return jsonify({'error': 'Invoice not found'}), 404

# New endpoint to record the rating separately.
@app.route('/record_rating', methods=['POST'])
def record_rating():
    data = request.json
    invoice_round = data.get('round')
    rating = data.get('rating')
    invoice = next((inv for inv in invoices if inv['round'] == invoice_round), None)
    if invoice:
        if invoice['response'] is None:
            return jsonify({'error': 'Response not recorded yet'}), 400
        if invoice['relationship_rating'] is None:
            invoice['relationship_rating'] = rating
            return jsonify({'message': 'Rating recorded'})
        else:
            return jsonify({'error': 'Rating already recorded'}), 400
    else:
        return jsonify({'error': 'Invoice not found'}), 404

# New endpoint to refresh (regenerate) invoices.
@app.route('/refresh_invoices', methods=['POST'])
def refresh_invoices():
    global invoices
    invoices = generate_invoices()
    return jsonify({'message': 'Invoices refreshed'})

# New endpoint to display all invoice data.
@app.route('/data')
def data():
    return render_template('data.html', invoices=invoices)

if __name__ == '__main__':
    app.run(debug=True)
