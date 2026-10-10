import socket
import sys

import flet as ft
from repository.http_repo import HTTPRepository
from repository.simple_repo import SimpleRepository
from views.home import HomeView
from views.totem import TotemView
from views.new_ticket import NewTicketView
from views.counter import ChoiceCounterView, CounterView
# from views.ticket import TicketView

def get_local_ip():
	"""Retrieve the primary local IP address on the LAN."""
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		# Connect to an arbitrary public IP (doesn't send actual data)
		s.connect(("8.8.8.8", 80))
		ip = s.getsockname()[0]
	except Exception:
		raise Exception("Not possible to determine machine ip address")
	finally:
		s.close()
	return ip

@ft.component
def App():
	return ft.Router(
		[
			ft.Route(path="", component=HomeView),
			ft.Route(path="totem", component=TotemView),
			ft.Route(path="services/:serviceId/newTicket/:ticketId", component=NewTicketView),
			ft.Route(path="counters", component= ChoiceCounterView),
			ft.Route(path="counters/:counterId", component = CounterView)
			# ft.Route(path="tickets/:ticketId", component=TicketView), # deprecated (ticket page is from server)
		],
		manage_views=True,
	)

def main(page: ft.Page):
	# get remote server url as first argument
	args = sys.argv[1:]
	if args and args[0]:
		server_url = args[0]
	# if no argument is provided, assume remote server is running on the same machine as the client on the 8000 port
	else:
		server_url = f"{get_local_ip()}:8000"
	print(f"Remote server base url: {server_url}")

	# configure server url and repository for the whole app
	page.server_url = server_url
	page.repo = HTTPRepository(server_url)
	# page.repo = SimpleRepository()
	
	# some UI tweaks
	page.theme_mode = ft.ThemeMode.LIGHT
	# render app
	page.render_views(App)



ft.run(main)