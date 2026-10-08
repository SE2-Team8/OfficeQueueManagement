import pytest
import flet.testing as ftt

@pytest.mark.asyncio
async def test_button_existence(flet_app: ftt.FletTestApp):
    tester = flet_app.tester

    await tester.pump_and_settle()

    btn_Totem = await tester.find_by_text("Totem")
    await tester.tap(btn_Totem)

    await tester.pump_and_settle()

    await click_btn("SHIPPING",tester)
    assert (await tester.find_by_text_containing(r"S\d+")).count == 1
    assert (await tester.find_by_key("qrcode")).count == 1
    await click_btn("GOT IT",tester)
    await click_btn("ACCOUNTS",tester)
    assert (await tester.find_by_text_containing(r"A\d+")).count == 1
    assert (await tester.find_by_key("qrcode")).count == 1
    await click_btn("GOT IT",tester)
    await click_btn("DEPOSIT",tester)
    assert (await tester.find_by_text_containing(r"D\d+")).count == 1
    assert (await tester.find_by_key("qrcode")).count == 1
    await click_btn("GOT IT",tester)

    
async def click_btn(btn_name:str, tester):

    btn = await tester.find_by_text(btn_name)
    assert btn.count == 1 
    await tester.tap(btn)
    await tester.pump_and_settle()
