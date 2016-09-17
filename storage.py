import json

class Storage():
	def __init__(self):
		pass

	def save_locally(data):
		with open('data/results.json', 'a') as out_file:
			out_file.write(json.dumps(data))

	def save_dynamoDB(data):
		