from repository.repo import BaseRepository

# simple repository that provides semi-hard-coded results
class SimpleRepository(BaseRepository):
	last_ticket: int = 0

	def get_new_ticket(self, serviceId: str) -> str:
		self.last_ticket += 1
		return self.last_ticket
	
	def get_services_ids(self) ->list[str]:
		return ["A", "B", "C", "D"]