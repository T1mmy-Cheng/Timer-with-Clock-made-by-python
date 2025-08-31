# timer_by_pyside.py
# A countdown timer app with analog clock and dynamic, theme-based backgrounds
import sys
import os
import datetime
from math import sin, cos, radians
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QSpinBox, QVBoxLayout, QCheckBox,
    QHBoxLayout, QGridLayout, QMessageBox, QStackedWidget, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import QTimer, QTime, Qt, QSize
from PySide6.QtGui import QPainter, QPen, QColor, QIcon

class CountdownTimer(QWidget):
    is_paused = False

    def __init__(self):
        super().__init__()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)

        # Pages
        self.stack = QStackedWidget(self)
        self.main_page = QWidget()
        self.settings_page = Setting(self.stack, self.main_page, self)

        self.stack.addWidget(self.main_page)
        self.stack.addWidget(self.settings_page)

        self._create_widgets()
        self._create_main_layout()
        self._connect_signals()

        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)
        self.stack.setCurrentWidget(self.main_page)

    # ---------- UI Construction ----------
    def _create_widgets(self):
        self.display = QLabel("00:00:00")
        self.display.setStyleSheet("font-size: 48px; font-weight: bold; background: transparent;")
        self.display.setAlignment(Qt.AlignCenter)

        self.h_spin = QSpinBox(); self.h_spin.setRange(0, 23)
        self.m_spin = QSpinBox(); self.m_spin.setRange(0, 59)
        self.s_spin = QSpinBox(); self.s_spin.setRange(0, 59)

        self.start_btn = QPushButton("Start")
        self.pause_btn = QPushButton("Pause"); self.pause_btn.setEnabled(False)
        self.reset_btn = QPushButton("Reset")

        # Settings icon button
        self.setting_btn = QPushButton()
        icon_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setting.png")
        self.setting_btn.setIcon(QIcon(icon_file))
        self.setting_btn.setIconSize(QSize(32, 32))
        self.setting_btn.setFixedSize(50, 50)
        self.setting_btn.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                border-radius: 15px;
                border: 1px solid #565859;
            }
            QPushButton:hover { background-color: #999999; }
            QPushButton:pressed {
                background-color: #202020;
                border: 1px solid #2e2e2e;
            }
        """)

        self.clock_display = QLabel()
        self.clock_display.setStyleSheet("font-size: 24px; color: gray; background: transparent;")
        self.clock_display.setAlignment(Qt.AlignCenter)
        self._update_clock()

        self.analog_clock = AnalogClock()

    def _create_main_layout(self):
        grid = QGridLayout()
        grid.addWidget(QLabel("Hours"), 0, 0); grid.addWidget(self.h_spin, 0, 1)
        grid.addWidget(QLabel("Minutes"), 1, 0); grid.addWidget(self.m_spin, 1, 1)
        grid.addWidget(QLabel("Seconds"), 2, 0); grid.addWidget(self.s_spin, 2, 1)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.reset_btn)

        layout = QVBoxLayout(self.main_page)
        layout.addWidget(self.analog_clock)
        layout.addWidget(self.clock_display)
        layout.addWidget(self.display)
        layout.addLayout(grid)
        layout.addLayout(btn_layout)

        # Bottom-right settings button
        bottom_row = QHBoxLayout()
        bottom_row.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        bottom_row.addWidget(self.setting_btn)
        layout.addStretch()
        layout.addLayout(bottom_row)

    def _connect_signals(self):
        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.reset_btn.clicked.connect(self.reset_timer)
        self.setting_btn.clicked.connect(self.show_settings)


    # ---------- Core Functionality ----------
    def start_timer(self):
        if self.is_paused:
            self.timer.start(1000)
            self.start_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.is_paused = False
            return

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
            self.is_paused = True
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
        QTimer.singleShot(8, self._update_clock)

    def show_settings(self):
        self.stack.setCurrentWidget(self.settings_page)

    def apply_light_mode(self):
        light_style = """
            QWidget {
                background-color: white;
                color: black;
            }
            QLabel {
                background: transparent;
                color: black;
            }
            QPushButton {
                border: 1px solid grey;
                border-radius: 6px;
                padding: 4px 10px;
            }
            QPushButton:hover { background-color: #999999; }
            QPushButton:pressed {
                background-color: #555555;
                border: 1px solid #2a2d2e;
            }
            QSpinBox {
            color: black;
            }
            QSpinBox:Hover { background-color: #BBBBBB; }
            QSpinBox:Pressed { background-color: #DDDDDD; }
            QCheckBox {
                spacing: 6px;
                color: black;
                background-color: transparent;
            }

            QCheckBox::indicator {
                border-radius: 3px;
                width: 12px;
                height: 12px;
            }

            QCheckBox::indicator:checked {
                /* Leave this empty or minimal */
            }

            QCheckBox::indicator:unchecked {
                background-color: white;
                border: 1px solid #666666;
            }

            }
        """
        self.setStyleSheet(light_style)
        self.setting_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border-radius: 15px;
                border: 1px solid #565859;
            }
            QPushButton:hover { background-color: #999999; }
            QPushButton:pressed {
                background-color: #202020;
                border: 1px solid #2e2e2e;
            }
        """)
        self.settings_page.setStyleSheet(light_style)



    def apply_dark_mode(self):
        dark_style = """ 
            QWidget {
                background-color: #1E1E1E;
                color: white;
            }
            QLabel {
                background: transparent;
                color: white;
            }
            QPushButton {
                border: 1px solid grey;
                border-radius: 6px;
                padding: 4px 10px;
            }
            QPushButton:hover { background-color: #414647; }
            QPushButton:pressed {
                background-color: #131414;
                border: 1px solid #2a2d2e;
            }
            QSpinBox {
                selection-background-color: rgba(0, 0, 0, 0);
                selection-color: white;
            }
            QSpinBox:Hover { background-color: #414647; }
            QSpinBox:Pressed { background-color: #131414; }
            QCheckBox {
                spacing: 6px;
                color: white;
                background-color: transparent;
            }

            QCheckBox::indicator {
                /* Do NOT set background-color or border here */
                width: 14px;
                height: 14px;
            }

            QCheckBox::indicator:checked {
            }

            QCheckBox::indicator:unchecked {
                /* Leave this empty or minimal */
            }
        """
        self.setStyleSheet(dark_style)
        self.setting_btn.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                border: 1px solid #565859;
            }
            QPushButton:hover { background-color: #999999; }
            QPushButton:pressed {
                background-color: #202020;
                border: 1px solid #2e2e2e;
            }
        """)
        self.settings_page.setStyleSheet(dark_style)



# ---------- Analog Clock ----------
class AnalogClock(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 300)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(8) # Smooth for 120Hz movement

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

        # Draw rounded square background
        painter.setBrush(QColor("#000000"))  # Light gray or any theme color
        painter.setPen(QPen(Qt.black, 1))

        # QRectF(x, y, width, height), corner radius X and Y
        painter.drawRoundedRect(-100, -100, 200, 200, 45, 45)

        # Draw clock face
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor("white"))
        painter.drawEllipse(-90, -90, 180, 180)

        
        # Draw numbers 1 to 12
        painter.setPen(QPen(Qt.black, 2))
        font = painter.font()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)

        for i in range(1, 13):
            angle = radians(i * 30)  # Convert degrees to radians
            radius = 75  # Distance from center to number
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
        painter.setBrush(Qt.black)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(-2, -60, 3, 60, 1.5, 1.5)  # width=3, height=45
        painter.restore()

        # Minute hand
        painter.save()
        painter.rotate(6 * minute)
        painter.setBrush(Qt.black)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(-2, -75, 3, 80, 1.5, 1.5)  # width=3, height=75
        painter.restore()

        # Second hand (smooth!)
        painter.save()
        painter.rotate(6 * second)
        painter.setBrush(QColor("orange"))
        painter.setPen(Qt.NoPen)

        # Main second hand
        painter.drawRoundedRect(-1, -80, 2, 80, 1, 1)

        # Tail (extends downward from center)
        painter.drawRoundedRect(-1, -1, 2, 20, 1, 1)
        painter.restore()

        # Center pivot
        painter.setBrush(QColor("orange"))
        painter.drawEllipse(-4, -4, 8, 8)

class Setting(QWidget):
    def __init__(self, stack, main_page, timer_widget):
        super().__init__()
        self.stack = stack
        self.main_page = main_page
        self.timer_widget = timer_widget

        layout = QVBoxLayout(self)
        Setting_LO = QHBoxLayout()
        self.Setting_LB = QLabel("Settings")
        Setting_LO.addWidget(self.Setting_LB, alignment=Qt.AlignCenter) 
        layout.addLayout(Setting_LO)
        self.Setting_LB.setStyleSheet("font-size: 48px; font-weight: bold; background: transparent;")

        # Theme chooser
        self.DarkmodeCB = QCheckBox("Dark Mode")
        layout.addWidget(self.DarkmodeCB, alignment=Qt.AlignCenter)
        self.DarkmodeCB.setChecked(True)
        self.DarkmodeCB.stateChanged.connect(self.DM)

        # Apply and back buttons
        btn_layout = QHBoxLayout()
        self.back_btn = QPushButton("Back")
        btn_layout.addWidget(self.back_btn)
        layout.addLayout(btn_layout)
        self.back_btn.clicked.connect(self.go_back)

    def DM(self):
        global Dark_mode
        Dark_mode = self.DarkmodeCB.isChecked()
        if Dark_mode:
            self.timer_widget.apply_dark_mode()
        else:
            self.timer_widget.apply_light_mode()

    def go_back(self):
        self.stack.setCurrentWidget(self.main_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    timer_widget = CountdownTimer()
    window.setCentralWidget(timer_widget)
    window.setWindowTitle("Timer with Clock")
    window.resize(350, 600)
    window.show()
    sys.exit(app.exec())