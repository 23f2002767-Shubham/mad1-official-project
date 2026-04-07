#“Start the engine”
'''
Docstring for placement_portal.run
It does ONLY this:

Creates the app

Runs it

❌ No routes
❌ No logic     
❌ No database
'''

"""Main entry point for Placement Portal Flask app"""

from app import create_app

app = create_app() # Create the Flask app instance using the factory function from app/__init__.py

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)




