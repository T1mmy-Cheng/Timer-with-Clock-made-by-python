import sys
from math import sin, cos, radians
import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QSpinBox,
    QVBoxLayout, QHBoxLayout, QGridLayout, QMessageBox, QStackedWidget
)
from PySide6.QtCore import QTimer, QTime, Qt
from PySide6.QtGui import QPainter, QPen, QColor


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
        self.analog_clock = AnalogClock()

    def _create_layouts(self):
        grid = QGridLayout()
        grid.addWidget(QLabel("Hours"), 0, 0); grid.addWidget(self.h_spin, 0, 1)
        grid.addWidget(QLabel("Minutes"), 1, 0); grid.addWidget(self.m_spin, 1, 1)
        grid.addWidget(QLabel("Seconds"), 2, 0); grid.addWidget(self.s_spin, 2, 1)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.reset_btn)
        self.pause_btn.setEnabled(False)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.analog_clock)
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
                self.pause_btn.setEnabled(False)
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
            self.pause_btn.setEnabled(False)
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
        QTimer.singleShot(1, self._update_clock)


class AnalogClock(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 200)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(1)

    def paintEvent(self, event):
        side = min(self.width(), self.height())
        now = datetime.datetime.now()
        second = now.second + now.microsecond / 1_000_000
        minute = now.minute + second / 60
        hour = now.hour % 12 + minute / 60

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        # Draw clock face
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("white"))
        painter.drawEllipse(-100, -100, 200, 200)

        # Draw hour marks
        painter.setPen(QPen(Qt.black, 2))
        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30)
        
        # Draw numbers 1 to 12
        painter.setPen(QPen(Qt.black, 2))
        font = painter.font()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)

        for i in range(1, 13):
            angle = radians(i * 30)  # Convert degrees to radians
            radius = 80  # Distance from center to number
            x = radius * sin(angle)
            y = -radius * cos(angle)  # Negative because Qt's y-axis goes down

            # Center the text at (x, y)
            rect_width = 20
            rect_height = 20
            painter.drawText(
                int(x - rect_width / 2),
                int(y - rect_height / 2),
                rect_width,
                rect_height,
                Qt.AlignCenter,
                str(i)
            )


        # Hour hand
        painter.save()
        painter.rotate(30 * hour)
        painter.setPen(QPen(Qt.black, 6))
        painter.drawLine(0, 0, 0, -50)
        painter.restore()

        # Minute hand
        painter.save()
        painter.rotate(6 * minute)
        painter.setPen(QPen(Qt.black, 4))
        painter.drawLine(0, 0, 0, -70)
        painter.restore()

        # Second hand (smooth!)
        painter.save()
        painter.rotate(6 * second)
        painter.setPen(QPen(QColor("orange"), 2))
        painter.drawLine(0, 0, 0, -90)
        painter.restore()

        # Center pivot
        painter.setBrush(QColor("orange"))
        painter.drawEllipse(-5, -5, 10, 10)


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