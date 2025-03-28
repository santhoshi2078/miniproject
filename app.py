from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client['roadside_assistance']  # Database name
assistance_requests_collection = db['assistance_requests']  # Assistance requests collection
service_providers_collection = db['service_providers']  # Service providers collection
contact_collection = db['contact_info']  # Contact info collection

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Service route
@app.route('/service')
def service():
    return render_template('service.html')

# About route
@app.route('/about')
def about():
    return render_template('about.html')

# Contact route (GET)
@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

# Contact form submission route (POST)
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    message = request.form['message']
    
    # Store contact info in MongoDB
    contact_collection.insert_one({
        'name': name,
        'email': email,
        'phone': phone,
        'message': message
    })
    
    # Redirect to confirmation page with user's name
    return redirect(url_for('contact_confirmation', name=name))


# Contact confirmation route
@app.route('/contact-confirmation/<name>')
def contact_confirmation(name):
    return render_template('contact_confirmation.html', name=name)

# Request assistance route (GET)
@app.route('/request-assistance')
def request_assistance():
    return render_template('request_assistance.html')

# Handle form submission and show service providers (POST)
@app.route('/service-providers', methods=['POST'])
def service_providers():
    # Extract data from the form
    name = request.form['name']
    email = request.form['Emailid']
    phone = request.form['phone']
    vehicle_type = request.form['vehicle_type']
    issue_description = request.form['issue_description']
    location = request.form['location']
    latitude = request.form['latitude']
    longitude = request.form['longitude']

    # Store the assistance request in MongoDB
    assistance_requests_collection.insert_one({
        'name': name,
        'email': email,
        'phone': phone,
        'vehicle_type': vehicle_type,
        'issue_description': issue_description,
        'location': location,
        'latitude': latitude,
        'longitude': longitude
    })

    # Fetch service providers based on the location from MongoDB
    providers = list(service_providers_collection.find({"location": location}))

    # Render the service providers list with their data
    return render_template('service_providers.html', location=location, providers=providers)

# Route to show provider details
@app.route('/provider-details/<id>')
def provider_details(id):
    try:
        provider = service_providers_collection.find_one({"_id": ObjectId(id)})
        if provider:
            return render_template('provider_details.html', provider=provider)
        else:
            return "Provider not found", 404
    except Exception as e:
        return str(e), 400

# Route to update map URL for a provider
@app.route('/update_map_url', methods=['POST'])
def update_map_url():
    # Get provider ID and map URL from the request
    provider_id = request.json.get('provider_id')
    map_url = request.json.get('map_url')

    # Update the map_url field in the MongoDB document
    result = service_providers_collection.update_one(
        {'_id': ObjectId(provider_id)},  # Find the provider by ID
        {'$set': {'map_url': map_url}}  # Update the map_url field
    )

    if result.modified_count > 0:
        return jsonify({'status': 'success', 'message': 'Map URL updated successfully!'})
    else:
        return jsonify({'status': 'failed', 'message': 'Failed to update map URL or provider not found.'})

if __name__ == '__main__':
    app.run(debug=True)