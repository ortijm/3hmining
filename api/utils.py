# -*- coding: utf-8 -*-
import re
import json
import time

from datetime import datetime, date, timedelta

def get_x_y_values(data):
    x_values = []
    y_values = []
    y2_values, y3_values, y4_values, y5_values, y6_values, y7_values, y8_values, y9_values, y10_values = [], [], [], [], [], [], [], [], []
    for item in data:
        if item['ColumnName'] == 'x':
            x_values = item['Values']
        elif item['ColumnName'] == 'y':
            y_values = item['Values']
        elif item['ColumnName'] == 'y2':
            y2_values = item['Values']
        elif item['ColumnName'] == 'y3':
            y3_values = item['Values']
        elif item['ColumnName'] == 'y4':
            y4_values = item['Values']
        elif item['ColumnName'] == 'y5':
            y5_values = item['Values']
        elif item['ColumnName'] == 'y6':
            y6_values = item['Values']
        elif item['ColumnName'] == 'y7':
            y7_values = item['Values']
        elif item['ColumnName'] == 'y8':
            y8_values = item['Values']
        elif item['ColumnName'] == 'y9':
            y9_values = item['Values']
        elif item['ColumnName'] == 'y10':
            y10_values = item['Values']

    def is_time_format(input):
        try:
            time.strptime(input, '%H:%M:%S')
            return True
        except ValueError:
            return False

    def join_tupla(x, y, y2, y3, y4, y5, y6, y7, y8, y9, y10):
        if is_time_format(x):
            yesterday = date.today() - timedelta(1)
            full_temporary_date = yesterday.strftime('%m/%d/%y ') + x
            # change to timespan the hour
            x = time.mktime(datetime.strptime(full_temporary_date, '%m/%d/%y %H:%M:%S').timetuple())
        tupla = {'x': x, 'y': y}
        if y2:
            tupla.update({'y2': y2})
        if y3:
            tupla.update({'y3': y3})
        if y4:
            tupla.update({'y4': y4})
        if y5:
            tupla.update({'y5': y5})
        if y6:
            tupla.update({'y6': y6})
        if y7:
            tupla.update({'y7': y7})
        if y8:
            tupla.update({'y8': y8})
        if y9:
            tupla.update({'y9': y9})
        if y10:
            tupla.update({'y10': y10})
        return tupla

    return map(join_tupla, x_values, y_values, y2_values, y3_values, y4_values, y5_values, y6_values, y7_values, y8_values, y9_values, y10_values)


def get_geo_values(data, extra):
    if not data or not extra:
        return {}
    output = {}
    output['global'] = {'lat': extra.get('position').get('lat'), 'lon': extra.get('position').get('lon')}

    excav_values = []
    tons_values = []
    queue_time_values = []
    performance_values = []
    elevation_values = []
    lat_values = []
    lon_values = []
    snippet_values = []
    title_values = []

    for item in data:
        if item['ColumnName'] == 'tons':
            tons_values = item['Values']
        elif item['ColumnName'] == 'Rendimiento':
            performance_values = item['Values']
        elif item['ColumnName'] == 'excav':
            excav_values = item['Values']
        elif item['ColumnName'] == 'TiempoCola':
            queue_time_values = item['Values']
        elif item['ColumnName'] == 'Elevacion':
            elevation_values = item['Values']
        elif item['ColumnName'] == 'lat':
            lat_values = item['Values']
        elif item['ColumnName'] == 'lon':
            lon_values = item['Values']
        elif item['ColumnName'] == 'snippet':
            snippet_values = item['Values']
        elif item['ColumnName'] == 'title':
            title_values = item['Values']

    def add_item(excav, tons, queue_time, performance, elevation, lat_value, lon_value, snippet, title):
        if lat_value and lon_value:
            lat = float(lat_value)
            lon = float(lon_value)
        elif excav in extra['shovels']:
            lat = extra['shovels'][excav].get('lat')
            lon = extra['shovels'][excav].get('lon')
        else:
            lat = extra['position'].get('lat')
            lon = extra['position'].get('lon')

        if not title:
            title = '{}: {} Tons'.format(excav, tons)

        if not snippet:
            snippet = 'Tiempo cola: {} Minutos \nRed Op: {} Ton/Hrs'.format(queue_time, performance)

        return {'lat': lat, 'lon': lon, 'title': title, 'snippet': snippet}

    output['items'] = map(add_item, excav_values, tons_values, queue_time_values, performance_values, elevation_values, lat_values, lon_values, snippet_values, title_values)
    return output


def get_table_values(data, extra):
    output = []
    for item in data:
        subtitles = re.search('.*(_SUB\d*)$', item['ColumnName'])
        headers = re.search('.*(_HEAD\d*)$', item['ColumnName'])
        if subtitles and subtitles.group(1):
            pattern = re.compile(r'_SUB\d*$')
            column_name = pattern.sub('', item['ColumnName'])
            item.update({'ColumnName': column_name, 'type': 'sub'})
        elif headers and headers.group(1):
            pattern = re.compile(r'_HEAD\d*$')
            column_name = pattern.sub('', item['ColumnName'])
            item.update({'ColumnName': column_name, 'type': 'head'})

        output.append(item)
    return output


def get_graph_data(type, bridge_response, extra):
    if type == 'LineChart' or type == 'BarChart':
        data = json.loads(bridge_response.response)
        return get_x_y_values(data)
    if type == 'MineData':
        data = json.loads(bridge_response.response)
        return get_geo_values(data, extra)
    if type == 'Table':
        data = json.loads(bridge_response.response)
        return get_table_values(data, extra)
    else:
        return json.loads(bridge_response.response)
