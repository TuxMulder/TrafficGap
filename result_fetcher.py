import googlemaps
import ConfigParser
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import os
import storage

class RouteFetcher():
	def __init__(self):
		config = ConfigParser.ConfigParser()
		config.read('configs/googleApiKeys.ini')
		self.apiKey = config.get('Keys', 'directions')
		self.storage = Storage()
		
	def record_route_timings(self, start, end):
		gmaps = googlemaps.Client(key = self.apiKey)
		now = datetime.now()
		directions = gmaps.directions(start, end, mode = "driving", departure_time = now, traffic_model = "best_guess", avoid="tolls", alternatives = True)
		data = { 'query_time': str(now), 'start': start, 'end': end, 'directions_data': directions }
		
		self.storage.save_locally(data)

if __name__ == '__main__':
	config = ConfigParser.ConfigParser()
	config.read('configs/destinationPoints.ini')
	home = config.get('Settings', 'home')
	work = config.get('Settings', 'work')
	morning_travel_hours = "{}-{}".format(config.get('Settings', 'min_leave'), config.get('Settings', 'max_leave'))
	evening_travel_hours = "{}-{}".format(config.get('Settings', 'min_return'), config.get('Settings', 'max_return'))
	minute_frequency = '0, 10, 20, 30, 40, 50'
	work_days = '1, 2, 3, 4, 5'

	fetcher = RouteFetcher()
	
	job_scheduler = BlockingScheduler()
	job_scheduler.add_job(fetcher.record_route_timings, 'cron', args=[home, work], day=work_days, hour=morning_travel_hours, minute=minute_frequency)
	job_scheduler.add_job(fetcher.record_route_timings, 'cron', args=[work, home], day=work_days, hour=evening_travel_hours, minute=minute_frequency)

	print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

	try:
		job_scheduler.start()
	except (KeyboardInterrupt, SystemExit):
	    pass