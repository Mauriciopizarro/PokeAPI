import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from app.services import fetch_all_berries, get_all_berry_stats, get_berry_histogram


BERRIES_LIST = [
    {"name": "cheri", "url": "http://pokeapi/berry/1/"},
    {"name": "chesto", "url": "http://pokeapi/berry/2/"}
]

BERRIES_DATA = [
    {"name": "cheri", "growth_time": 3},
    {"name": "chesto", "growth_time": 5}
]

CALC_STATS_RESULT = {"mean": 4, "max": 5, "min": 3, "frequency": {3: 1, 5: 1}}
HISTOGRAM_RESULT = {"3": 1, "5": 1}


@pytest.fixture(autouse=True)
def init_cache():
    FastAPICache.init(InMemoryBackend(), prefix="test")


@pytest.fixture
def mock_httpx_get_success():
    with patch("app.services.httpx.get") as mock_get:

        mock_list = MagicMock()
        mock_list.json.return_value = {"results": BERRIES_LIST}
        mock_list.raise_for_status.return_value = None

        berry_mocks = [
            MagicMock(**{"json.return_value": d, "raise_for_status.return_value": None})
            for d in BERRIES_DATA
        ]

        mock_get.side_effect = [mock_list, *berry_mocks]
        yield mock_get

@pytest.fixture
def mock_httpx_get_empty():
    with patch("app.services.httpx.get") as mock_get:
        response = MagicMock()
        response.json.return_value = {"results": []}
        response.raise_for_status.return_value = None
        mock_get.return_value = response
        yield mock_get

@pytest.fixture
def mock_httpx_get_http_error():
    with patch("app.services.httpx.get") as mock_get:
        response = MagicMock()
        response.raise_for_status.side_effect = httpx.HTTPStatusError(
            message="Not Found", request=MagicMock(), response=MagicMock(status_code=404)
        )
        mock_get.return_value = response
        yield mock_get

@pytest.fixture
def mock_httpx_get_timeout():
    with patch("app.services.httpx.get") as mock_get:
        mock_get.side_effect = httpx.TimeoutException("Timeout")
        yield mock_get

@pytest.fixture
def mock_calculate_stats():
    with patch("app.services.calculate_stats") as mock_calc:
        mock_calc.return_value = CALC_STATS_RESULT
        yield mock_calc

@pytest.fixture
def mock_generate_histogram():
    with patch("app.services.generate_histogram") as mock_hist:
        mock_hist.return_value = HISTOGRAM_RESULT
        yield mock_hist

@pytest.fixture
def mock_fetch_all_berries():
    with patch("app.services.fetch_all_berries", new_callable=AsyncMock) as mock_fetch:
        mock_fetch.return_value = (
            [d["name"] for d in BERRIES_DATA],
            [d["growth_time"] for d in BERRIES_DATA]
        )
        yield mock_fetch

@pytest.mark.asyncio
async def test_fetch_all_berries_success(mock_httpx_get_success):
    berries, growth_times = await fetch_all_berries()
    assert berries == ["cheri", "chesto"]
    assert growth_times == [3, 5]
    assert mock_httpx_get_success.call_count == 3

@pytest.mark.asyncio
async def test_fetch_all_berries_empty_list(mock_httpx_get_empty):
    berries, growth_times = await fetch_all_berries()
    assert berries == []
    assert growth_times == []
    mock_httpx_get_empty.assert_called_once()

@pytest.mark.asyncio
async def test_fetch_all_berries_http_error(mock_httpx_get_http_error):
    with pytest.raises(httpx.HTTPStatusError):
        await fetch_all_berries()

@pytest.mark.asyncio
async def test_fetch_all_berries_timeout(mock_httpx_get_timeout):
    with pytest.raises(httpx.TimeoutException):
        await fetch_all_berries()

@pytest.mark.asyncio
async def test_get_all_berry_stats_success(mock_fetch_all_berries, mock_calculate_stats):
    result = await get_all_berry_stats()
    mock_fetch_all_berries.assert_awaited_once()
    mock_calculate_stats.assert_called_once_with(
        ["cheri", "chesto"], [3, 5], {3: 1, 5: 1}
    )
    assert result == CALC_STATS_RESULT

@pytest.mark.asyncio
async def test_get_berry_histogram_success(mock_fetch_all_berries, mock_generate_histogram):
    result = await get_berry_histogram()
    mock_fetch_all_berries.assert_awaited_once()
    mock_generate_histogram.assert_called_once_with([3, 5])
    assert result == HISTOGRAM_RESULT
