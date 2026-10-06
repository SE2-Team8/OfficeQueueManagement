import flet as ft

@ft.component
def TicketView():

    # extract the serviceId
    params = ft.use_route_params()
    service_id = params.get("serviceId")
	
    return ft.View(
        route=ft.use_view_path(),  
        appbar=ft.AppBar(title=ft.Text(f"Here is your ticket for service {service_id}!")),
        controls=[
            ft.Text("TICKET # PLACEHOLDER", size=24),
            ft.Button(
                content="GOT IT",
                on_click=lambda: ft.context.page.navigate("totem"),
			)
        ],
    )