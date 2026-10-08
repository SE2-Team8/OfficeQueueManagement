import pytest
import flet.testing as ftt

@pytest.mark.asyncio
async def test_button_existence(flet_app: ftt.FletTestApp):
    tester = flet_app.tester

    await tester.pump_and_settle()

    assert (await tester.find_by_text("Totem")).count == 1
    assert (await tester.find_by_text("Counter")).count == 1
    assert (await tester.find_by_text("Screen")).count == 1
    