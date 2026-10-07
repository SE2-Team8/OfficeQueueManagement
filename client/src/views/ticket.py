import base64
from io import BytesIO

import flet as ft
import qrcode
from repository.repo import BaseRepository


@ft.component
def TicketView():

	# extract the serviceId from page
	params = ft.use_route_params()
	serviceId = params.get("serviceId")

	# get the ticket from the service
	repo: BaseRepository = ft.context.page.repo

	# TODO: change this to create a QR code to an URL and not to the code
	ticketCode = repo.get_new_ticket(serviceId)
	ticketQR_base64 = generate_qrcode_base64(ticketCode)

	# display the ticket code, along a qr code and a button to go back
	return ft.View(
		route=ft.use_view_path(),
		vertical_alignment=ft.MainAxisAlignment.CENTER,
		horizontal_alignment=ft.CrossAxisAlignment.CENTER,
		controls=[
			ft.Text(f"Here is your ticket for service {serviceId}!"),
			ft.Text(f"{ticketCode}", size=24),
			ft.Image(src=ticketQR_base64, width=200, height=200),
			ft.Button(
				content="GOT IT",
				on_click=lambda: ft.context.page.navigate("totem"),
			)
		],
	)

def generate_qrcode_base64(data: str):

	# generate qrcode and save it to a buffer
	img = qrcode.make(data)
	buffer = BytesIO()
	img.save(buffer, format="PNG")
	
	# save the buffer bytes as base64 chars
	qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
	
	return qr_base64