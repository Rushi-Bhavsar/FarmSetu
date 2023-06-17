from weather.utils.get_weather_data import *
from requests.models import Response


def test_dry_run(mocker):

    assert 1 == 1


def test_process_region_data_success(mocker):
    mock_region_urls = ['https//:urls.nsakn.nsa']
    mock_bulk_data = [{'name': 'dummy data', 'value': 10}, {'name': 'dummy data2', 'value': 11}]
    mocker.patch('weather.utils.get_weather_data.create_weather_urls', return_value=mock_region_urls)
    mocker.patch('weather.utils.get_weather_data.scrap_region_data', return_value=mock_bulk_data)
    mocker.patch('weather.utils.get_weather_data.WeatherData.insert_multiple_records', return_value=mock_bulk_data)
    records_created = process_region_data('UK')
    assert type(records_created) is list
    assert len(records_created) == len(mock_bulk_data)


def test_process_region_data_fail(mocker):
    mock_region_urls = ['https//:urls.nsakn.nsa']
    mock_bulk_data = [{'name': 'dummy data', 'value': 10}, {'name': 'dummy data2', 'value': 11}]
    mocker.patch('weather.utils.get_weather_data.create_weather_urls', return_value=mock_region_urls)
    mocker.patch('weather.utils.get_weather_data.scrap_region_data', return_value=mock_bulk_data)
    mocker.patch('weather.utils.get_weather_data.WeatherData.insert_multiple_records', return_value=0)
    records_created = process_region_data('UK')
    assert type(records_created) is not list
    assert records_created == 0


def test_create_weather_urls_success():
    region = 'UK'
    region_urls = create_weather_urls(region)
    assert type(region_urls) is list
    assert len(region_urls) == 7, f"This should be equal to the number of weather parameter present for a region."


def test_scrap_region_data_success(mocker):
    region_urls = ['https://anddjsnfsd.ksjdf/erjhfk/ejdjs/jfhj/Tmax/hhdsf/fdsjlf/UK.txt']
    mock_bulk_data = [{'name': 'dummy data', 'value': 10}, {'name': 'dummy data2', 'value': 11}]
    mocker.patch('weather.utils.get_weather_data.requests.get', return_value=None)
    mocker.patch('weather.utils.get_weather_data.process_scarp_data', return_value=mock_bulk_data)
    bulk_data = scrap_region_data(region_urls)
    assert bulk_data is not None
    assert len(bulk_data) == len(mock_bulk_data)


def test_scrap_region_data_fail(mocker):
    region_urls = []
    bulk_data = scrap_region_data(region_urls)
    assert type(bulk_data) is list
    assert bulk_data == []
    assert len(bulk_data) == 0


def test_process_scrap_data_success(mocker):
    dummy_text = "Areal values from HadUK-Grid 1km gridded climate data from land surface network\nSource: " \
                 "Met Office National Climate Information Centre\nMonthly, seasonal and annual mean of daily maximum " \
                 "air temperature for England\nAreal series, starting in 1884\nLast updated 01-Jun-2023 10:46\nyear" \
                 "    jan    feb    mar    apr    may    jun    jul    aug    sep    oct    nov    dec     win     " \
                 "spr     sum     aut     ann\n1884    8.2    7.6    9.6   10.7   15.9   18.4   20.3   22.2   18.4   " \
                 "12.6    8.2    6.4     ---   12.06   20.30   13.05   13.22\n1885    4.6    8.4    8.0   11.7   " \
                 "12.8   18.5   21.0   18.0   16.3   10.3    8.1    6.1    6.40   10.84   19.16   11.53   " \
                 "11.98\n1886    4.3    3.4    6.8   11.3   14.4   4.62   10.84   "
    resp_obj = mocker.MagicMock(spec=Response, text=dummy_text)
    region = 'UK'
    param = 'Tmax'
    data = process_scarp_data(resp_obj, region, param)
    assert data != []
    assert type(data[0]) is WeatherData


def test_process_scrap_data_fail(mocker):
    dummy_text = ""
    resp_obj = mocker.MagicMock(spec=Response, text=dummy_text)
    region = 'UK'
    param = 'Tmax'
    data = process_scarp_data(resp_obj, region, param)
    assert data == []
