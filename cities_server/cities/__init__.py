"""CityAPI package initializer."""
import flask

# app is a single object used by all the code modules in this package
app = flask.Flask(__name__)

app.config.from_object('cities.config')

#import destinations.views
import cities.nlp
import cities.api
import cities.model


