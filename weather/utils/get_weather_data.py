import requests
from django.conf import settings
from weather.models import WeatherData


def get_region_wise_data():
    region_list = ['UK', 'England', 'Wales', 'Scotland', 'Northern_Ireland', 'England_and_Wales', 'England_N',
                   'England_S', 'Scotland_N', 'Scotland_E', 'Scotland_W', 'England_E_and_NE', 'England_NW_and_N_Wales',
                   'Midlands', 'East_Anglia', 'England_SW_and_S_Wales', 'England_SE_and_Central_S']
    for region in region_list:
        process_region_data(region)


def process_region_data(region):
    print("--"*50)
    print(f"Processing '{region}' Region Data")
    region_urls = create_weather_urls(region)
    bulk_load_data = scrap_region_data(region_urls)
    created_records = WeatherData.insert_multiple_records(bulk_load_data)
    if created_records:
        print(f"Total {len(created_records)} records will be created for '{region}' region.")
    else:
        print(f"Zero records will be created for '{region}' region.")
    print("==" * 50)
    return created_records


def create_weather_urls(region) -> list:
    """
    Create weather URL based on region and weather parameter
    :return: List of weather urls.
    """
    weather_parameter = ['Tmax', 'Tmin', 'Tmean', 'Sunshine', 'Rainfall', 'Raindays1mm', 'AirFrost']
    # weather_parameter = ['Tmax']
    weather_urls = []
    for param in weather_parameter:
        weather_url = settings.WEATHER_URL
        weather_url = weather_url.replace('<region>', region)
        weather_url = weather_url.replace('<weather_parameter>', param)
        weather_urls.append(weather_url)
    return weather_urls


def scrap_region_data(region_urls):
    bulk_data = []
    for url in region_urls:
        resp = requests.get(url)
        weather_param = url.split("/")[-3]
        region = url.split("/")[-1].split(".")[0]
        processed_data = process_scarp_data(resp, region, weather_param)
        bulk_data.extend(processed_data)
    return bulk_data


def process_scarp_data(resp, region, weather_param):
    payload = []
    try:
        split_resp = resp.text.split("\n")[5:-1]
        input_name = split_resp.pop(0).split()
    except Exception as e:
        split_resp = ''
        input_name = []

    for line in split_resp:
        data = dict()
        data['region'] = region
        data['weather_parameter'] = weather_param
        field_data = line.split()
        if len(field_data) == 8:
            dummy_value = ['0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0']
            dummy_value.extend(field_data[6:])
            dummy_value.extend(['0.0', '0.0', '0.0'])
            field_data = field_data[:6]
            field_data.extend(dummy_value)
        for index, value in enumerate(field_data):
            if "." in value:
                data[input_name[index]] = float(value)
            elif value.isdigit():
                data[input_name[index]] = int(value)
            elif "-" in value:
                data[input_name[index]] = 0.0
        # We can also add a condition to check if record for region, weather_parameter and year is present.
        # If record is present then we will not add the record.
        # We can also add record for specific region, weather_parameter and year.
        payload.append(WeatherData(**data))
    return payload

