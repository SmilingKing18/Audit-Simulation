from flask import Flask, render_template, request, jsonify
import time
from simulation import generate_invoices

app = Flask(__name__)

# Generate invoices when the server starts
invoices = generate_invoices()

@app.route('/')
def index():
    # Render the main page with a list of invoices
    return render_template('index.html', invoices=invoices)

@app.route('/select_invoice', methods=['POST'])
def select_invoice():
    data = request.json
    invoice_round = data.get('round')
    # Find the invoice by its round number
    invoice = next((inv for inv in invoices if inv['round'] == invoice_round), None)
    if invoice:
        # Record the time when the invoice is opened
        if invoice['open_time'] is None:
            invoice['open_time'] = time.time()
        return jsonify(invoice)
    else:
        return jsonify({'error': 'Invoice not found'}), 404

@app.route('/record_response', methods=['POST'])
def record_response():
    data = request.json
    invoice_round = data.get('round')
    response_text = data.get('response')
    rating = data.get('rating')
    invoice = next((inv for inv in invoices if inv['round'] == invoice_round), None)
    if invoice:
        if invoice['response'] is None:
            invoice['response'] = response_text
            invoice['response_time'] = time.time()
            invoice['relationship_rating'] = rating
            duration = invoice['response_time'] - invoice['open_time'] if invoice['open_time'] else None
            # Here you can also write this data to a file or database
            return jsonify({'message': 'Response recorded', 'duration': duration})
        else:
            return jsonify({'error': 'Response already recorded'}), 400
    else:
        return jsonify({'error': 'Invoice not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
