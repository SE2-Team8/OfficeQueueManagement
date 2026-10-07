import socket

import flet as ft
from repository.simple_repo import SimpleRepository
from views.home import HomeView
from views.totem import TotemView
from views.new_ticket import NewTicketView
from views.ticket import TicketView

def get_local_ip():
    """Retrieve the primary local IP address on the LAN."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connect to an arbitrary public IP (doesn't send actual data)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
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
			ft.Route(path="tickets/:ticketId", component=TicketView),
        ],
        manage_views=True,
    )

def main(page: ft.Page):
    page.repo = SimpleRepository()
    page.base_url = f"{get_local_ip()}:8000"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.render_views(App)

ft.run(main)