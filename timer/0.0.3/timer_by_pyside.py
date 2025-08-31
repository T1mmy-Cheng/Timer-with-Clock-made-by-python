import sys
import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QSpinBox,
    QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox
)
from PySide6.QtCore import QTimer, QTime, Qt


class CountdownTimer(QWidget):
    Stop = False
    def __init__(self):
        super().__init__()
        self.remaining_secs = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)

        self._create_widgets()
        self._create_layouts()
        self._connect_signals()

    def _create_widgets(self):
        # Display
        self.display = QLabel("00:00:00")
        self.display.setStyleSheet("font-size: 48px; font-weight: bold;")
        self.display.setAlignment(Qt.AlignCenter)

        # Time input
        self.h_spin = QSpinBox(); self.h_spin.setRange(0, 23)
        self.m_spin = QSpinBox(); self.m_spin.setRange(0, 59)
        self.s_spin = QSpinBox(); self.s_spin.setRange(0, 59)

        # Buttons
        self.start_btn = QPushButton("Start")
        self.pause_btn = QPushButton("Pause")
        self.reset_btn = QPushButton("Reset")

        # Clock
        self.clock_display = QLabel()
        self.clock_display.setStyleSheet("font-size: 24px; color: gray;")
        self.clock_display.setAlignment(Qt.AlignCenter)
        self._update_clock()

    def _create_layouts(self):
        grid = QGridLayout()
        grid.addWidget(QLabel("Hours"), 0, 0); grid.addWidget(self.h_spin, 0, 1)
        grid.addWidget(QLabel("Minutes"), 1, 0); grid.addWidget(self.m_spin, 1, 1)
        grid.addWidget(QLabel("Seconds"), 2, 0); grid.addWidget(self.s_spin, 2, 1)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.reset_btn)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.clock_display)
        main_layout.addWidget(self.display)
        main_layout.addLayout(grid)
        main_layout.addLayout(btn_layout)

    def _connect_signals(self):
        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.reset_btn.clicked.connect(self.reset_timer)

    def start_timer(self):
        if self.Stop:
            self.timer.start(1000)
            self.start_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.Stop = False
            return
        else:
            self.pause_btn.setEnabled(True)
            self.remaining_secs = (
                self.h_spin.value() * 3600 +
                self.m_spin.value() * 60 +
                self.s_spin.value()
            )
            if self.remaining_secs > 0:
                self.update_display()
                self.timer.start(1000)
                self.start_btn.setEnabled(False)
            else:
                QMessageBox.warning(self, "Warning", "Set a time before starting.")

    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setEnabled(True)
            self.Stop = True
            self.pause_btn.setEnabled(False)

    def update_countdown(self):
        if self.remaining_secs > 0:
            self.remaining_secs -= 1
            self.update_display()
        else:
            self.timer.stop()
            self.start_btn.setEnabled(True)
            QMessageBox.information(self, "Done", "Countdown finished!")

    def update_display(self):
        t = QTime(0, 0).addSecs(self.remaining_secs)
        self.display.setText(t.toString("hh:mm:ss"))

    def reset_timer(self):
        self.timer.stop()
        self.h_spin.setValue(0)
        self.m_spin.setValue(0)
        self.s_spin.setValue(0)
        self.display.setText("00:00:00")
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)

    def _update_clock(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_display.setText(f"Time: {current_time}")
        QTimer.singleShot(1000, self._update_clock)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PySide6 Countdown Timer")
        self.setCentralWidget(CountdownTimer())
        self.resize(300, 200)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())