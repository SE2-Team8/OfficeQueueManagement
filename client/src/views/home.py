import flet as ft

@ft.component
def HomeView():
    return ft.View(
        route=ft.use_view_path(),
        can_pop=False, # to be used on root view
        vertical_alignment=ft.MainAxisAlignment.CENTER,
		horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Text("Select a function", size=24),
            ft.Button(
                "Totem",
                on_click=lambda: ft.context.page.navigate("/totem"),
            ),
            # TODO: other buttons on_click
			ft.Button("Counter"),
			ft.Button("Screen"),
        ],
    )