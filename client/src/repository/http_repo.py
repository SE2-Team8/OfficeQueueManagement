import os

from repository.repo import BaseRepository
import requests

# repository that gets results from querying a web server
class HTTPRepository(BaseRepository):
	def __init__(self, remote_host):
		if not remote_host:
			raise ValueError(f"Invalid remote host: {remote_host}")
		
		self.remote_host = remote_host

	def get_new_ticket(self, serviceId: str) -> str:
		response = requests.post(
			f"http://{self.remote_host}/tickets",
			json={"service_tag": f"{serviceId}"},
			timeout=10, # TODO: remove timeout?
		)
		response.raise_for_status()
		data = response.json()
		# print(data)
		return data['code']
	
	def get_services_ids(self) -> list[str]:
		response = requests.get(f"http://{self.remote_host}/tickets/services")
		response.raise_for_status()  # raises for 4xx/5xx
		data = response.json()
		# print(data)
		return [item['tag_name'] for item in data]

	def get_num_counter(self) -> list[int]:
		response = requests.get(f"http://{self.remote_host}/counters/")
		response.raise_for_status()
		data = response.json()
		return[item['id']for item in data]

	def post_next_customer(self, counterId):
		response = requests.post(f"http://{self.remote_host}/counters/{counterId}/next")
		response.raise_for_status()
		if response.status_code == 204:
			return "No customer in queue"
		data = response.json()
		return data["ticket_code"]
	