import lib.PhenomenonPlot as pp

# ------------------------------------- #
# ---------- FLAGS
# ------------------------------------- #

COLOR_PALETTE_CASES = {
    "color-list": ['blue', 'lightblue', 'yellow', 'orange', 'red'],
    "range-list": ['0-25', '26-50', '51-75', '76-100', '>100']
}

COLOR_PALETTE_DEATH = {
    "color-list": ['blue', 'lightblue', 'yellow', 'orange', 'red'],
    "range-list": ['0-5', '6-10', '11-15', '16-20', '>20']
}

SHP_FILE_PATH = 'data/shp/tunisia/Tunisia_region.shp'
CSV_FILE_PATH = 'data/csv/tunisia/new_cases.csv'

COMMON_COLUMN = 'REGION'

EXPORT_DIR_PATH = 'output/tunisia/cases/'

# ------------------------------------- #
# ---------- MAIN CODE
# ------------------------------------- #

casesTun = pp.PhenomenonPlot()
casesTun.SHP_Read(SHP_FILE_PATH)
casesTun.CSV_Read(CSV_FILE_PATH)
casesTun.create_GeoJSON(COMMON_COLUMN, color_palette=COLOR_PALETTE_CASES)
casesTun.plot_geoJSON_to_SHP(EXPORT_DIR_PATH,
                             plotName='tunisia_new_cases',
                             title='Tunisia - New Cases',
                             figsize=(7.2, 12.8),
                             linewidth=1.25)
