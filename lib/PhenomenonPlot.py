import os

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

import geopandas as gpd
import cv2


class PhenomenonPlot:
    def __init__(self):
        self._shp_object = None
        self._data_phenomenon = None
        self._geoJSON_data = {}

    def SHP_Read(self, path: str):
        self._shp_object = gpd.read_file(path)

    def CSV_Read(self, path: str):
        self._data_phenomenon = pd.read_csv(path)

    def XLSX_Read(self, path: str):
        self._data_phenomenon = pd.read_excel(path)

    @staticmethod
    def _decode_color_ranges(color_palette):
        color_ranges = {}
        for _index_ in range(color_palette['color-list'].__len__()):
            if '-' in color_palette['range-list'][_index_]:
                tmp_range = color_palette['range-list'][_index_].split('-')
                color_ranges[color_palette['color-list'][_index_]] = {
                    'min': int(tmp_range[0]),
                    'max': int(tmp_range[1])
                }
            elif '<' in color_palette['range-list'][_index_]:
                tmp_range = color_palette['range-list'][_index_].split('<')
                color_ranges[color_palette['color-list'][_index_]] = {
                    'min': None,
                    'max': int(tmp_range[1])
                }
            elif '>' in color_palette['range-list'][_index_]:
                tmp_range = color_palette['range-list'][_index_].split('>')
                color_ranges[color_palette['color-list'][_index_]] = {
                    'min': int(tmp_range[1]),
                    'max': None
                }

        return color_ranges

    @staticmethod
    def _get_color_from_value(value, color_ranges):
        for _color_ in color_ranges.keys():
            if color_ranges[_color_]['min'] is None:
                if value < color_ranges[_color_]['max']:
                    return _color_
            elif color_ranges[_color_]['max'] is None:
                if value > color_ranges[_color_]['min']:
                    return _color_
            else:
                if value in range(color_ranges[_color_]['min'], color_ranges[_color_]['max']):
                    return _color_
        return 'black'

    def create_GeoJSON(self, commonColumn_csv: str, color_palette=None):
        if commonColumn_csv in self._data_phenomenon.keys():
            columnList = self._data_phenomenon[commonColumn_csv].to_list()
            eventList = self._data_phenomenon.keys().to_list()
            eventList.remove(commonColumn_csv)

            for _index_ in range(columnList.__len__()):
                self._geoJSON_data[columnList[_index_]] = {}
                for _event_ in eventList:
                    if color_palette is None and type(color_palette) is not dict:
                        self._geoJSON_data[columnList[_index_]][_event_] = {
                            'value': self._data_phenomenon[_event_][_index_],
                            'color': 'gray'
                        }
                    else:
                        color_ranges = self._decode_color_ranges(color_palette)
                        self._geoJSON_data[columnList[_index_]][_event_] = {
                            'value': self._data_phenomenon[_event_][_index_],
                            'color': self._get_color_from_value(self._data_phenomenon[_event_][_index_],
                                                                color_ranges)
                        }

    def plot_geoJSON_to_SHP(self, export_dir_path):
        pass
