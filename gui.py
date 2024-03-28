from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLineEdit,
    QPushButton,
    QLabel,
    QGroupBox,
    QComboBox,
    QGridLayout,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtCore import Slot
from PySide6.QtGui import QIntValidator, QDoubleValidator
import numpy as np
from signal_generator import SignalGenerator
from spectrogram import compute_spectrogram
from plot import MplCanvas, MplImage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal Generator")
        self.controls_widget = ControlsWidget(self)

        self.signal_plot = MplCanvas(self, xlabel="n", ylabel="Amplitude", title="Signal")
        self.spectrogram_img = MplImage(self, xlabel="n", ylabel="Frequency", title="Spectrogram")
        plot_layout = QVBoxLayout()
        plot_layout.addWidget(self.signal_plot)
        plot_layout.addWidget(self.signal_plot.toolbar)
        plot_layout.addWidget(self.spectrogram_img)
        plot_layout.addWidget(self.spectrogram_img.toolbar)

        dummy_layout = QHBoxLayout()
        dummy_layout.addWidget(self.controls_widget)
        dummy_layout.addLayout(plot_layout)
        dummy_layout.setStretch(1,1)

        main_dummy_widget = QWidget()
        main_dummy_widget.setLayout(dummy_layout)
        self.setCentralWidget(main_dummy_widget)

    def append_data(self, x_data: list[int], y_data: list[int]):
        self.signal_plot.append_data(x_data, y_data)

    def compute_spectrogram(self, window_type, window_size, overlap):
        _, y_data = self.signal_plot.data()
        spectrogram_data = compute_spectrogram(y_data, overlap, window_size, window_type)
        extent_x = (0, len(y_data))
        extent_y = (0, self.controls_widget.signal_gen.sample_rate / 2)
        self.spectrogram_img.update_data(np.abs(spectrogram_data), extent_x, extent_y)
    
    def clear(self):
        self.signal_plot.clear()
        self.spectrogram_img.clear()
        

class ControlsWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent = parent

        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.generate_clicked)
        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_clicked)
        self.spectrogram_button = QPushButton("Compute\nSpectrogram")
        self.spectrogram_button.clicked.connect(self.compute_spectrogram)

        self.phase_edit = QLineEdit("1")
        self.freq_edit = QLineEdit("1")
        self.sample_rate_edit = QLineEdit("100")
        self.bit_depth_edit = QLineEdit("5")
        self.size_edit = QLineEdit("10000")

        self.fm_depth_edit = QLineEdit("5")
        self.fm_period_edit = QLineEdit("5000")

        self.overlap_edit = QLineEdit("50")
        self.window_size_edit = QLineEdit("256")
        self.window_type_combo = QComboBox()
        self.window_type_combo.addItems(["Rectangular","Hamming","Hann"])
        self.window_type_combo.setCurrentText("Hamming")

        signal_params_box = QGroupBox("Signal parameters:")
        signal_params_grid = QGridLayout()
        signal_params_grid.addWidget(QLabel("Phase:"), 0, 0, 1, 1)
        signal_params_grid.addWidget(self.phase_edit, 1, 0, 1, 1)
        signal_params_grid.addWidget(QLabel("Frequency:"), 0, 1, 1, 1)
        signal_params_grid.addWidget(self.freq_edit, 1, 1, 1, 1)
        signal_params_grid.addWidget(QLabel("Sample Rate"), 2, 0, 1, 1)
        signal_params_grid.addWidget(self.sample_rate_edit, 3, 0, 1, 1)
        signal_params_grid.addWidget(QLabel("Bit Depth:"), 2, 1, 1, 1)
        signal_params_grid.addWidget(self.bit_depth_edit, 3, 1, 1, 1)
        signal_params_box.setLayout(signal_params_grid)
        #signal_params_grid.addWidget(QWidget(), 4, 0, 1, 2)

        modulator_params_box = QGroupBox("FM parameters")
        modulator_params_grid = QGridLayout()
        modulator_params_grid.addWidget(QLabel("Modulation Depth:"), 0, 0, 1, 1)
        modulator_params_grid.addWidget(self.fm_depth_edit, 1, 0, 1, 1)
        modulator_params_grid.addWidget(QLabel("Modulation Period:"), 0, 1, 1, 1)
        modulator_params_grid.addWidget(self.fm_period_edit, 1, 1, 1, 1)
        modulator_params_box.setLayout(modulator_params_grid)
        #controls_grid_layout.addWidget(QWidget(), 7, 0, 1, 2)

        spectrogram_params_box = QGroupBox("Spectrogram")
        spectrogram_params_grid = QGridLayout()
        spectrogram_params_grid.addWidget(QLabel("Window Overlap(%):"), 0, 0, 1, 1)
        spectrogram_params_grid.addWidget(self.overlap_edit, 1, 0, 1, 1)
        spectrogram_params_grid.addWidget(QLabel("Window Size:"), 0, 1, 1, 1)
        spectrogram_params_grid.addWidget(self.window_size_edit, 1, 1, 1, 1)
        spectrogram_params_grid.addWidget(QLabel("Window Type:"), 2, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
        spectrogram_params_grid.addWidget(self.window_type_combo, 2, 1, 1, 1)
        spectrogram_params_box.setLayout(spectrogram_params_grid)

        buttons_grid = QGridLayout()
        buttons_grid.addWidget(QLabel("Generated Points Count:"), 0, 0, 1, 1, Qt.AlignmentFlag.AlignRight)
        buttons_grid.addWidget(self.size_edit, 0, 1, 1, 1)
        buttons_grid.addWidget(self.clear_button, 1, 0, 1, 1)
        buttons_grid.addWidget(self.generate_button, 1, 1, 1, 1)
        buttons_grid.addWidget(self.spectrogram_button, 2, 1, 1, 1)

        
        main_layout = QVBoxLayout()
        main_layout.addWidget(signal_params_box)
        main_layout.addWidget(modulator_params_box)
        main_layout.addWidget(spectrogram_params_box)
        main_layout.addLayout(buttons_grid)
        main_layout.addWidget(QWidget())
        main_layout.setStretch(4, 1)
        self.setLayout(main_layout)
        self.signal_gen = SignalGenerator()
    


    @Slot()
    def generate_clicked(self):
        try:
            phase       = float(self.phase_edit.text())
            freq        = float(self.freq_edit.text())
            sample_rate = float(self.sample_rate_edit.text())
            bit_depth   = int(self.bit_depth_edit.text())
            size        = int(self.size_edit.text())
            fm_depth    = float(self.fm_depth_edit.text())
            fm_period   = int(self.fm_period_edit.text())
        except ValueError:
            self._msg_input_error()
            return

        self.signal_gen.set_params(None, freq, sample_rate, bit_depth, fm_depth, fm_period)
        x_data, y_data = self.signal_gen.get_samples(size)
        self._parent.append_data(x_data, y_data)
        print("Generate clicked")
    
    @Slot()
    def clear_clicked(self):
        self.signal_gen.reset()
        self._parent.clear()
        print("Clear clicked")

    @Slot()
    def compute_spectrogram(self):
        try:
            overlap = float(self.overlap_edit.text()) / 100
            window_size = int(self.window_size_edit.text())
            window_type = str(self.window_type_combo.currentText()).lower()
        except ValueError:
            self._msg_input_error()
            return
        self._parent.compute_spectrogram(window_type, window_size, overlap)

    def _msg_input_error(self):
        msg_box = QMessageBox()
        msg_box.setText("Invalid input")
        msg_box.setWindowTitle("Error")
        msg_box.exec()
