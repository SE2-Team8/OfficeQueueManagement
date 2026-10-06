import flet as ft

@ft.component
def HomeView():
    return ft.View(
        route=ft.use_view_path(),
        can_pop=False, # to be used on root view
        controls=[
            ft.Text("Select a function", size=24),
            ft.Button(
                "Totem",
                on_click=lambda: ft.context.page.navigate("/totem"),
            ),
        ],
    )