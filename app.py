from flask import Flask


# Create the app
app = Flask(__name__)

# Get routes for front-end
import views.routes

# Get routes for data
import api.data_routes

# Import greeting routes
import api.test_routes

# Run the app
app.run(host='18.224.31.100', port=8080, debug=False)