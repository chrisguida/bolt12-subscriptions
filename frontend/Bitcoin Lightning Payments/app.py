from flask import Flask, render_template, request, jsonify
import qrcode
from io import BytesIO
import base64
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///merchoffers.db' # Example database URI
db = SQLAlchemy(app)

# Define the 0ffer model
class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    offer_data = db.Column(db.String(256), nullable=False)

@app.before_request
def create_tables():
    # This will ensure that the tables are created before the first request
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/qr-code')
def qr_code():
    # Hardcoded offer and URL
    merchant_offer = "merchant_offer_here"
    
    # URL to handle the subscription (the user will be redirected to this URL)
    subscription_url = f"http://localhost:5000/subscribe?merchant_offer={merchant_offer}"

    # Generate the QR code containing the merchant's offer and subscription URL
    qr_data = f"Merchant's Pubkey: {merchant_offer}\nTo Subscribe: {subscription_url}"


    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    # Save QR code to an in-memory bytes buffer
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Encode the QR code image as a base64 string
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Pass the base64 string to the template
    return render_template('qr_code.html', qr_code_data=img_base64)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    # Extract POST data (client's offer)
    data = request.json # Use `.form` for form-encoded data or `.json` for JSON data

    # Validate the data
    if not data or 'client_offer' not in data or 'merchan_offer' not in data:
        return jsonify({"error": "Invalid input, 'client_offer' and 'merchant_offer' are required"}), 400

     # Extract the fields
    offer = data['offer']

    # Store the offer in the database
    new_offer = Offer(offer_data=offer)
    db.session.add(new_offer)
    db.session.commit()

    return jsonify({"message": f"Subscription successful for client with offer {offer}!"}), 200

#@app.route('/generate-invoice/<int:subscription_id>', methods=['GET'])
#def generate_invoice(subscription_id):
    # Fetch the client's offer using the subscription ID
    #subscription = Subscription.query.get_or_404(subscription_id)
    
    # Generate the invoice (for this example, just return the data)
    #invoice_data = {
        #"merchant_offer": subscription.merchant_offer,
        #"client_offer": subscription.client_offer,
        #"invoice_amount": "1000 sats"  # Example amount
    #}

    # Return the invoice data (or generate a real invoice here)
    #return jsonify(invoice_data)


if __name__ == '__main__':
    app.run(debug=True)
