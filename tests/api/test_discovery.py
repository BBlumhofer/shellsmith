import httpx
import pytest

import shellsmith
from shellsmith.clients import AsyncClient
from shellsmith.config import config
from shellsmith.utils import base64_encode

RFID = {"name": "RFIDTagString", "value": "WST_A_1"}


@pytest.fixture
def asset_link(workpiece_carrier_a1):
    """Links the carrier's RFID tag to its shell in the discovery service."""
    shell_id = base64_encode(workpiece_carrier_a1.id)
    url = f"{config.discovery_host}/lookup/shells/{shell_id}"
    httpx.post(url, json=[RFID]).raise_for_status()
    yield
    httpx.delete(url)


def test_lookup_shells(asset_link, workpiece_carrier_a1):
    found = shellsmith.lookup_shells([RFID])
    assert found["result"] == [workpiece_carrier_a1.id]


def test_lookup_shells_unknown_asset_id(asset_link):
    assert shellsmith.lookup_shells([{**RFID, "value": "WST_X_9"}])["result"] == []


@pytest.mark.asyncio
async def test_async_lookup_shells(asset_link, workpiece_carrier_a1):
    async with AsyncClient(host=config.discovery_host) as client:
        found = await client.lookup_shells([RFID])
    assert found["result"] == [workpiece_carrier_a1.id]
