import pytest
import flet.testing as ftt

@pytest.mark.asyncio
async def test_counter_next_queue_empty(flet_app: ftt.FletTestApp):
    tester = flet_app.tester

    await tester.pump_and_settle()

    btn_counter = await tester.find_by_text("Counter")
    await tester.tap(btn_counter)

    await tester.pump_and_settle()

    await click_btn("1", tester)
    assert (await tester.find_by_text_containing("Counter 1")).count == 1
    assert (await tester.find_by_text("Next Customer")).count == 1
    await click_btn("Next Customer",tester)
    assert (await tester.find_by_text("No Customers in queue")).count == 1

    
async def click_btn(btn_name:str, tester):
    btn = await tester.find_by_text(btn_name)
    assert btn.count == 1 
    await tester.tap(btn)
    await tester.pump_and_settle()
