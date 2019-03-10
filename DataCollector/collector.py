class DataCollector:
	__init__(self, API, CollectorConfig):
		'''
		initialize api
		set root_folder
		'''

	def write_log(self, log_file_path, data):
		'''
		'''
		
	def pull_data(self, start, end):
		'''
		data = self.api.get_data(start, end)
		
		'''

	def new_collection(self, target_file_path, start, end):
		'''
		start = self.api.time_transformer(start)
		end = self.api.time_transformer(end)
			
		file.wirte_row([start, end])
		from start to end:
			data = self.api.get_data(time_n, time_n+1)
			if self.api.data_is_valid(data):
				file.write_log(message)
			else:		
				data = self.api.data_transformer(data)
				file.write_row(data)


		'''
	def old_collection(self, target_file_path):
		'''
			start = file.header
			end = file.header


		'''