import flet as ft
from views.home import HomeView
from views.totem import TotemView
from views.ticket import TicketView

@ft.component
def App():
    return ft.Router(
        [
            ft.Route(path="", component=HomeView),
            ft.Route(path="totem", component=TotemView),
			ft.Route(path="services/:serviceId/newTicket", component=TicketView),
        ],
        manage_views=True,
    )

def main(page: ft.Page):
    page.render_views(App)

ft.run(main)