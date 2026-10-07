import flet as ft

from repository.repo import BaseRepository

@ft.component
def TotemView():
    # get the available services and build cards for them
	repo: BaseRepository = ft.context.page.repo
	serviceIds = repo.get_services_ids()
	serviceCards = [
        ServiceCard(
            service_name=service,
            on_click=lambda e, srv=service: 
				ft.context.page.navigate(f"services/{srv}/newTicket"),
        )
        for service in serviceIds
    ]

	# display the cards in a grid
	return ft.View(
		route=ft.use_view_path(),
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		controls=[
            ft.Text("Get a ticket for one of the below services", size=24),
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
        content=ft.Text(service_name, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, size=40),
        on_click=on_click,
        bgcolor=ft.Colors.BLUE,
        border_radius=ft.BorderRadius.all(20),
        alignment=ft.Alignment.CENTER
    )