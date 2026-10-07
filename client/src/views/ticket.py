import flet as ft

@ft.component
def TicketView():

	# extract the ticketId from page route
	params = ft.use_route_params()
	ticketId = params.get("ticketId")

	return ft.View(
		route=ft.use_view_path(),
		vertical_alignment=ft.MainAxisAlignment.CENTER,
		horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		controls=[
			ft.Text(f"Your ticket code:"),
			ft.Text(f"{ticketId}", size=24)
		],
	)