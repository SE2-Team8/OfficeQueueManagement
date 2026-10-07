from abc import ABC, abstractmethod

class BaseRepository(ABC):

	@abstractmethod
	def get_new_ticket(self, serviceId: str) -> str:
		pass
	
	@abstractmethod
	def get_services_ids(self) ->list[str]:
		pass

	#TODO: add all needed repository methods for tickets, counters...