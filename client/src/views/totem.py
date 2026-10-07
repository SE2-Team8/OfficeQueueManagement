import flet as ft

from repository.repo import BaseRepository


def generate_code_and_move(service: str):
	try:
		repo: BaseRepository = ft.context.page.repo
		ticketCode = repo.get_new_ticket(service)
		ft.context.page.navigate(f"services/{service}/newTicket/{ticketCode}")
	except Exception as e:
			ft.context.page.error(str(e))

@ft.component
def TotemView():
    # get the available services and build cards for them
	try:
		repo: BaseRepository = ft.context.page.repo
		serviceIds = repo.get_services_ids()
	except Exception as e:
		ft.context.page.error(str(e))

	serviceCards = [
        ServiceCard(
            service_name=service,
            on_click=lambda e, srv=service: 
				generate_code_and_move(srv)
        )
        for service in serviceIds
    ]

	# display the cards in a grid
	return ft.View(
		route=ft.use_view_path(),
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		controls=[
            ft.Text("Get a ticket for one of the below services", size=24, color=ft.Colors.SECONDARY, weight=ft.FontWeight.BOLD),
            ft.Row(
				controls=[
					ft.Container(expand=1),   # left spacer
					ft.GridView(
						controls=serviceCards,
						runs_count=3,	# nNumber of columns
						spacing=10,	# horizontal space between cards
						run_spacing=10,	# vertical space between rows
						expand=6,
						align=ft.Alignment.CENTER
					),
					ft.Container(expand=1),   # right spacer
				],
				expand=True,
			)
        ],
	)


@ft.component
def ServiceCard(service_name: str, on_click):
    return ft.Container(
        content=ft.Text(service_name, color=ft.Colors.ON_PRIMARY, weight=ft.FontWeight.BOLD, size=40),
        on_click=on_click,
        bgcolor=ft.Colors.PRIMARY,
        border_radius=ft.BorderRadius.all(20),
        alignment=ft.Alignment.CENTER
    )