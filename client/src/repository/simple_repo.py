from repository.repo import BaseRepository

# simple repository that provides hard-coded results
class SimpleRepository(BaseRepository):
	def get_new_ticket(self, serviceId: str) -> str:
		return "12345678"
	
	def get_services_ids(self) ->list[str]:
		return ["A", "B", "C", "D"]