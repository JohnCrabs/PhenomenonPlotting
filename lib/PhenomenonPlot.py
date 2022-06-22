import os

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd

import geopandas as gpd
import cv2

import lib.file_manipulation as file_manip


class PhenomenonPlot:
    def __init__(self):
        self._shp_object = None
        self._data_phenomenon = None
        self._geoJSON_data = {}
        self._legend = []

    def SHP_Read(self, path: str):
        self._shp_object = gpd.read_file(path)

    def CSV_Read(self, path: str):
        self._data_phenomenon = pd.read_csv(path)

    def XLSX_Read(self, path: str):
        self._data_phenomenon = pd.read_excel(path)

    def _decode_color_ranges(self, color_palette):
        color_ranges = {}
        self._legend = []
        for _index_ in range(color_palette['color-list'].__len__()):
            self._legend.append(patches.Patch(color=color_palette['color-list'][_index_],
                                              label=color_palette['range-list'][_index_]))
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
                if value in range(color_ranges[_color_]['min'] - 1, color_ranges[_color_]['max'] + 1):
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

    def plot_geoJSON_to_SHP(self, export_dir_path, plotName='plot', title='', figsize=(12, 12), linewidth=2.0):
        row_list = list(self._geoJSON_data.keys())
        column_list = list(self._geoJSON_data[row_list[0]].keys())

        file_manip.checkAndCreateFolders(export_dir_path)

        # Create color_dict
        for _column_ in column_list:
            color_list = []
            for _row_ in row_list:
                color_list.append(self._geoJSON_data[_row_][_column_]['color'])
            fig, ax = plt.subplots(figsize=figsize)
            ax.set_aspect('equal')
            self._shp_object.plot(ax=ax, color=color_list)
            self._shp_object.boundary.plot(ax=ax, color='black', linestyle='--', linewidth=linewidth)
            plt.title(title + ' - ' + _column_, fontsize=20)
            plt.legend(handles=self._legend,
                       loc='upper center',
                       bbox_to_anchor=(0.5, -0.05),
                       fancybox=True,
                       shadow=True,
                       ncol=3,
                       fontsize=15)

            fig.tight_layout()

            export_path = export_dir_path + plotName + '_' + _column_
            print('Export fig at: ', export_path)
            plt.savefig(export_path)
            plt.close()
