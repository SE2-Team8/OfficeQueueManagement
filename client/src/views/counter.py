import flet as ft
from repository.repo import BaseRepository

@ft.component
def ChoiceCounterView():
    counterIds =[]
    try:
        repo: BaseRepository = ft.context.page.repo
        counterIds = repo.get_num_counter()
    except Exception as e:
        ft.context.page.error(str(e))

    counterCards = [
        CounterCard(
            counter_id=counter,
            on_click= lambda e, cid=counter: 
                navigateTo(f"/counters/{cid}")
        )
        for counter in counterIds
    ]

    # display the counters in a grid
    return ft.View(
		route=ft.use_view_path(),
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		controls=[
            ft.Text("Choose what counter to serve", size=24, color=ft.Colors.SECONDARY, weight=ft.FontWeight.BOLD),
            ft.Row(
				controls=[
					ft.Container(expand=1),   # left spacer
					ft.GridView(
						controls=counterCards,
						runs_count=len(counterCards),	# nNumber of columns
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
def CounterCard(counter_id: int, on_click):
    return ft.Container(
        content=ft.Text(counter_id, color=ft.Colors.ON_PRIMARY, weight=ft.FontWeight.BOLD, size=40),
        on_click=on_click,
        bgcolor=ft.Colors.PRIMARY,
        border_radius=ft.BorderRadius.all(20),
        alignment=ft.Alignment.CENTER
    )


@ft.component
def CounterView():

    params = ft.use_route_params()
    counterId = params.get("counterId")
    customerCode, setCustomerCode = ft.use_state("")

    return ft.View(
		route=ft.use_view_path(),
		vertical_alignment=ft.MainAxisAlignment.CENTER,
		horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		controls=[
			ft.Text(f"Counter {counterId} :", color=ft.Colors.SECONDARY, weight=ft.FontWeight.BOLD),
            ft.Text(customerCode, color=ft.Colors.PRIMARY, weight=ft.FontWeight.BOLD),
			ft.Button(
                width = 200,
                height = 50,
				content="Next Customer",
				on_click=lambda e: callNextCustomer(counterId,setCustomerCode)
			)
	    ]
	)

def callNextCustomer(counterId, setCustomerCode):
    try:
        repo: BaseRepository = ft.context.page.repo
        nextCustomer = repo.post_next_customer(counterId)
        setCustomerCode(nextCustomer)
    except Exception as e:
        ft.context.page.error(str(e))

    

def navigateTo(url: str):
    try: 
        ft.context.page.navigate(url)
    except Exception as e:
        ft.context.page.error(str(e))