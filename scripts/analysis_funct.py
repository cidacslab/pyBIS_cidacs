import sys
from os import path, system
from threading import Thread
import webbrowser
from PyQt5.QtWidgets import QFileDialog
import fiona

sys.path.append(path.join(path.dirname(__file__), 'SpatialSUSapp'))
dir_dbc = path.expanduser('~/datasus_dbc/')


def load_items(filename, frame):
    data = gpd.read_file(filename)
    combobox_s = [frame.comboBox, frame.comboBox_2, frame.comboBox_3]
    [combobox.clear() for combobox in combobox_s]
    [combobox.addItems(list(data.columns)) for combobox in combobox_s]


def get_shapefile(button):
    filename, _ = QFileDialog.getOpenFileName(button, 'Carregar Arquivo',
                                              f'{dir_dbc}',
                                              'File shp (*.shp)')
    # button.setEnabled(True)
    button.setText(filename)
    try:
        load_items(filename, frame)
    except fiona.errors.DriverError:
        pass


def get_csv(button, line):
    try:
        filename, _ = QFileDialog.getOpenFileName(
            button, 'Carregar Arquivo', f'{dir_dbc}', 'File csv (*.csv)'
        )
        line.setEnabled(True)
        line.setText(filename)
    except FileNotFoundError:
        pass


def trade_frame(layout, parent, frame):
    parent.setHidden(True)
    frame.setHidden(False)


def start_server(program):
    import index
    program.analysis = Thread(target=index.app.run_server, daemon=True)
    program.analysis.start()
    program.nav = Thread(target=webbrowser.open, args=('127.0.0.1:8050',),
                         daemon=True)
    program.nav.start()