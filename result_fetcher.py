import googlemaps
import ConfigParser
from datetime import datetime

class RouteFetcher():
	def __init__(self):
		config = ConfigParser.ConfigParser()
		config.read('configs/googleApiKeys.ini')
		self.apiKey = config.get('Keys', 'directions')
		
	def record_route_timings(self, start, destination):
		gmaps = googlemaps.Client(key = self.apiKey)
		now = datetime.now()
		timings = gmaps.directions(start, destination, mode = "driving", departure_time = now, traffic_model = "best_guess", avoid="tolls", alternatives = True)
		
		for timing in timings:
			print "{}{}".format(timing['summary'],timing['legs'][0]['duration_in_traffic'])

if __name__ == '__main__':
	fetcher = RouteFetcher()
	fetcher.record_route_timings("Location 1", "Location 2")

