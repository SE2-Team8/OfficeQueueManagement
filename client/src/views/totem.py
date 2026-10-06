import flet as ft

@ft.component
def TotemView():
    return ft.View(
        route=ft.use_view_path(),
        # some services (hard-coded, super temporary)
        controls=[
            ft.Text("Select a service", size=24),
            ft.Button(
                "Service A",
                on_click=lambda: ft.context.page.navigate("services/A/newTicket"),
            ),
            ft.Button(
				"Service B",
				on_click=lambda: ft.context.page.navigate("services/B/newTicket"),
			),
            ft.Button(
				"Service C",
				on_click=lambda: ft.context.page.navigate("services/C/newTicket"),
			),
                        
        ],
    )