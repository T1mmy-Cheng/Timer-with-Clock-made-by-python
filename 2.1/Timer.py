# timer_by_pyside.py
# A countdown timer app with analog clock and dynamic, theme-based backgrounds, and Stopwatch
import sys
import os
import datetime
import darkdetect
from math import sin, cos, radians
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QSpinBox, QVBoxLayout, QCheckBox,
    QHBoxLayout, QGridLayout, QMessageBox, QStackedWidget, QSpacerItem, QSizePolicy, QTextEdit
)
from PySide6.QtCore import QTimer, QTime, Qt, QSize, QElapsedTimer
from PySide6.QtGui import QPainter, QPen, QColor, QIcon

def get_dark_style():
    return """ 
            QWidget {
                background-color: #1E1E1E;
                color: #F3F3F3;
            }
            QLabel {
                background: transparent;
                color: #F3F3F3;
            }
            QPushButton {
                background-color: #2D2D2D;
                border: 1px solid #3A3A3A;
                border-radius: 6px;
                padding: 4px 10px;
            }
            QPushButton:hover { background-color: #3A3A3A; }
            QPushButton:disabled {background-color: #252525;
                                border: 1px solid #3A3A3A;
                                color: #A0A0A0;
                                }
            QPushButton:pressed {
                background-color: #252525;
                border: 1px solid #3A3A3A;
            }
            QSpinBox {
                selection-background-color: #3A3A3A;
                selection-color: #F3F3F3;
                padding-top: 1px;
                padding-right: 15px;
                padding-bottom: 1px;
            }
            QSpinBox:hover { background-color: #3A3A3A; }
            QSpinBox:pressed { background-color: #303030; }
            QCheckBox {
                spacing: 6px;
                color: #F3F3F3;
                background-color: transparent;
            }

            QCheckBox::indicator {
                width: 14px;
                height: 14px;
            }
            QCheckBox::indicator:checked {
            }

            QCheckBox::indicator:unchecked {
            }
            QTextEdit {
                background-color: #252525;
                color: #F3F3F3;
            }
        """

def get_light_style():
    return """
            QWidget {
                background-color: #F3F3F3;
                color: #171717;
            }
            QLabel {
                background: transparent;
                color: #171717;
            }
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 6px;
                padding: 4px 10px;
            }
            QPushButton:hover { background-color: #F0F0F0; }
            QPushButton:disabled {background-color: #F0F0F0;
                                border: 1px solid #CCCCCC;
                                }
            QPushButton:pressed {
                background-color: #E5E5E5;
                border: 1px solid #CCCCCC;
            }
            QSpinBox {
                background-color: #FFFFFF;
                color: #171717;
                padding-top: 1px;
                padding-right: 15px;
                padding-bottom: 1px;
                selection-background-color: #DDDDDD;
                selection-color: #171717;
            }
            QSpinBox:hover { background-color: #F0F0F0; }
            QSpinBox:pressed { background-color: #E5E5E5; }

            QCheckBox {
                spacing: 6px;
                color: #171717;
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
            QTextEdit {
                background-color: #F3F3F3;
                color: #171717;
            }
        """


class CountdownTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.is_paused = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_countdown)

        # Pages
        self.stack = QStackedWidget(self)
        self.main_page = QWidget()
        self.settings_page = Setting(self.stack, self.main_page, self)  # Pass self as timer_widget
        self.stopwatch_page = Stopwatch(self.stack, self.main_page, self.settings_page)

        self.stack.addWidget(self.main_page)
        self.stack.addWidget(self.stopwatch_page)
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
        self.pause_btn = QPushButton("Reset")
        self.pause = False

        # Settings icon button
        self.setting_btn = QPushButton()
        setting_icon_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setting.png")
        self.setting_btn.setIcon(QIcon(setting_icon_file))
        self.setting_btn.setIconSize(QSize(32, 32))
        self.setting_btn.setFixedSize(50, 50)
        self.setting_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D2D2D;
                border: 1px solid #3A3A3A;
                border-radius: 15px;
            }
            QPushButton:hover { background-color: #3A3A3A; }
            QPushButton:pressed {
                background-color: #252525;
                border: 1px solid #3A3A3A;
            }
        """)
        # Stop Watch icon button
        self.stopwatch_btn = QPushButton()
        stopwatch_icon_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stopwatch.png")
        self.stopwatch_btn.setIcon(QIcon(stopwatch_icon_file))
        self.stopwatch_btn.setIconSize(QSize(32, 32))
        self.stopwatch_btn.setFixedSize(50, 50)
        self.stopwatch_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D2D2D;
                border: 1px solid #3A3A3A;
                border-radius: 15px;
            }
            QPushButton:hover { background-color: #3A3A3A; }
            QPushButton:pressed {
                background-color: #252525;
                border: 1px solid #3A3A3A;
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

        layout = QVBoxLayout(self.main_page)
        layout.addWidget(self.analog_clock)
        layout.addWidget(self.clock_display)
        layout.addWidget(self.display)
        layout.addLayout(grid)
        layout.addLayout(btn_layout)

        # Bottom-right settings button
        bottom_row = QHBoxLayout()
        bottom_row.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        bottom_row.addWidget(self.stopwatch_btn)
        bottom_row.addWidget(self.setting_btn)
        layout.addStretch()
        layout.addLayout(bottom_row)

    def _connect_signals(self):
        self.start_btn.clicked.connect(self.start_timer)
        self.pause_btn.clicked.connect(self.pause_timer)
        self.setting_btn.clicked.connect(lambda: self.show_settings_from(self.main_page))
        self.stopwatch_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.stopwatch_page))


    # ---------- Core Functionality ----------
    def start_timer(self):
        if self.pause:
            self.timer.start(1000)
            self.start_btn.setEnabled(False)
            self.pause = False
            self.pause_btn.setText("Pause")
            return
        
        self.remaining_secs = (
            self.h_spin.value() * 3600 +
            self.m_spin.value() * 60 +
            self.s_spin.value() - 1
        )
        if self.remaining_secs >= 0:
            self.update_display()
            self.timer.start(1000)
            self.start_btn.setEnabled(False)
            self.pause_btn.setText("Pause")
        else:
            QMessageBox.warning(self, "Warning", "Set a time before starting.")

    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pause = True
            self.start_btn.setEnabled(True)
            self.start_btn.setText("Continue")
            self.pause_btn.setText("Reset")

        elif self.pause_btn.text() == "Reset" and not self.timer.isActive():
            self.reset_timer()

    def update_countdown(self):
        if self.remaining_secs > 0:
            self.remaining_secs -= 1
            self.update_display()
        else:
            self.remaining_secs -= 1
            self.update_display()
            self.timer.stop()
            self.start_btn.setEnabled(True)
            self.pause_btn.setEnabled(False)
            QMessageBox.information(self, "Done", "Countdown finished!")

    def update_display(self):
        t = QTime(0, 0).addSecs(self.remaining_secs + 1)
        self.display.setText(t.toString("hh:mm:ss"))

    def reset_timer(self):
        self.timer.stop()
        self.h_spin.setValue(0)
        self.m_spin.setValue(0)
        self.s_spin.setValue(0)
        self.display.setText("00:00:00")
        self.start_btn.setEnabled(True)
        self.start_btn.setText("Start")
        self.pause = False

    def _update_clock(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_display.setText(f"Time: {current_time}")
        QTimer.singleShot(8, self._update_clock)  # Update every second

    def show_settings_from(self, from_page):
        self.settings_page.previous_page = from_page
        self.stack.setCurrentWidget(self.settings_page)

    def apply_light_mode(self):
        self.setStyleSheet(get_light_style())
        self.settings_page.setStyleSheet(get_light_style())
        self.stopwatch_page.setStyleSheet(get_light_style())
        self.stopwatch_page.apply_light_mode()  # Apply to stopwatch-specific widgets
        icon_style = """
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 15px;
            }
            QPushButton:hover { background-color: #F0F0F0; }
            QPushButton:pressed {
                background-color: #E5E5E5;
                border: 1px solid #CCCCCC;
            }
        """
        self.setting_btn.setStyleSheet(icon_style)
        self.stopwatch_btn.setStyleSheet(icon_style)

    def apply_dark_mode(self):
        self.setStyleSheet(get_dark_style())
        self.settings_page.setStyleSheet(get_dark_style())
        self.stopwatch_page.setStyleSheet(get_dark_style())
        self.stopwatch_page.apply_dark_mode()  # Apply to stopwatch-specific widgets
        icon_style = """
            QPushButton {
                background-color: #2D2D2D;
                border: 1px solid #3A3A3A;
                border-radius: 15px;
            }
            QPushButton:hover { background-color: #3A3A3A; }
            QPushButton:pressed {
                background-color: #252525;
                border: 1px solid #3A3A3A;
            }
        """
        self.setting_btn.setStyleSheet(icon_style)
        self.stopwatch_btn.setStyleSheet(icon_style)


# ---------- Analog Clock ----------
class AnalogClock(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 300)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(8)  # Smooth for 120Hz movement

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
        self.previous_page = main_page  # Default

        layout = QVBoxLayout(self)
        Setting_LO = QHBoxLayout()
        self.Setting_LB = QLabel("⚙️ Settings")
        Setting_LO.addWidget(self.Setting_LB, alignment=Qt.AlignCenter) 
        layout.addLayout(Setting_LO)
        self.Setting_LB.setStyleSheet("font-size: 48px; font-weight: bold; background: transparent;")

        # Theme chooser
        self.DarkmodeCB = QCheckBox("Dark Mode")
        layout.addWidget(self.DarkmodeCB, alignment=Qt.AlignCenter)
        if darkdetect.isDark():
            self.DarkmodeCB.setChecked(True)
        else:
            self.DarkmodeCB.setChecked(False)
        self.DarkmodeCB.stateChanged.connect(self.DM)

        # Apply and back buttons
        btn_layout = QHBoxLayout()
        self.back_btn = QPushButton("Back")
        btn_layout.addWidget(self.back_btn)
        layout.addLayout(btn_layout)
        self.back_btn.clicked.connect(self.go_back)

    def DM(self):
        if self.DarkmodeCB.isChecked():
            self.timer_widget.apply_dark_mode()
        else:
            self.timer_widget.apply_light_mode()
            
    def go_back(self):
        self.stack.setCurrentWidget(self.previous_page)

class Stopwatch(QWidget):
    def __init__(self, stack, main_page, settings_page):
        super().__init__()
        self.stack = stack
        self.main_page = main_page
        self.settings_page = settings_page

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.elapsed_timer = QElapsedTimer()
        self.accumulated = 0
        self.is_running = False
        self.last_lap_time = 0
        self.laps = []

        self.clock_display = QLabel()
        self.clock_display.setStyleSheet("font-size: 24px; color: gray; background: transparent;")
        self.clock_display.setAlignment(Qt.AlignCenter)
        self._update_clock()

        self.display = QLabel("00:00:00:000")
        self.display.setStyleSheet("font-size: 48px; font-weight: bold; background: transparent;")
        self.display.setAlignment(Qt.AlignCenter)

        self.laps_display_title = QLabel(f"{"Lap":<11}{"Time":15}{"Total"}    ")
        self.laps_display_title.setStyleSheet("font-size: 24px; font-weight: bold; background: transparent;")
        self.laps_display_title.setAlignment(Qt.AlignCenter)

        self.start_btn = QPushButton("Start")
        self.pause_btn = QPushButton("Reset")
        self.lap_btn = QPushButton("Lap")
        self.lap_btn.setEnabled(False)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.lap_btn)

        self.laps_display = QTextEdit()
        self.laps_display.setReadOnly(True)
        self.laps_display.setFixedHeight(350)  # Fixed height for scrollbar

        layout = QVBoxLayout(self)
        layout.addWidget(self.clock_display)
        layout.addWidget(self.display)
        layout.addLayout(btn_layout)
        layout.addWidget(self.laps_display_title)
        layout.addWidget(self.laps_display)

        self.start_btn.clicked.connect(self.start)
        self.pause_btn.clicked.connect(self.pause)
        self.lap_btn.clicked.connect(self.record_lap)

        self.main_timer_btn = QPushButton()
        timer_icon_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "3158183.png")
        self.main_timer_btn.setIcon(QIcon(timer_icon_file))
        self.main_timer_btn.setIconSize(QSize(32, 32))
        self.main_timer_btn.setFixedSize(50, 50)
        self.main_timer_btn.setStyleSheet("""
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

        self.setting_btn = QPushButton()
        setting_icon_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "setting.png")
        self.setting_btn.setIcon(QIcon(setting_icon_file))
        self.setting_btn.setIconSize(QSize(32, 32))
        self.setting_btn.setFixedSize(50, 50)
        self.setting_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D2D2D;
                border: 1px solid #3A3A3A;
                border-radius: 15px;
            }
            QPushButton:hover { background-color: #3A3A3A; }
            QPushButton:pressed {
                background-color: #252525;
                border: 1px solid #3A3A3A;
            }
        """)

        nav_layout = QHBoxLayout()
        nav_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        nav_layout.addWidget(self.main_timer_btn)
        nav_layout.addWidget(self.setting_btn)

        layout.addStretch()
        layout.addLayout(nav_layout)

        self.main_timer_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.main_page))
        self.setting_btn.clicked.connect(lambda: self.stack.parent().show_settings_from(self))

    def start(self):
        if not self.is_running:
            self.elapsed_timer.start()
            self.timer.start(8)  # Update every 8ms for smooth milliseconds
            self.is_running = True
            self.start_btn.setEnabled(False)
            self.lap_btn.setEnabled(True)
            self.pause_btn.setText("Pause")

    def pause(self):
        if self.is_running:
            self.accumulated += self.elapsed_timer.elapsed()
            self.timer.stop()
            self.is_running = False
            self.start_btn.setEnabled(True)
            self.lap_btn.setEnabled(False)
            self.pause_btn.setText("Reset")
        
        elif self.is_running == False and self.pause_btn.text() == "Reset":
            self.reset()

    def reset(self):
        self.timer.stop()
        self.elapsed_timer.invalidate()
        self.accumulated = 0
        self.display.setText("00:00:00:000")
        self.is_running = False
        self.start_btn.setEnabled(True)
        self.lap_btn.setEnabled(False)
        self.laps_display.clear()
        self.laps = []
        self.last_lap_time = 0

    def update_display(self):
        if self.is_running:
            elapsed_ms = self.accumulated + self.elapsed_timer.elapsed()
        else:
            elapsed_ms = self.accumulated
        t = QTime(0, 0).addMSecs(elapsed_ms)
        self.display.setText(t.toString("hh:mm:ss:zzz"))

    def record_lap(self):
        if not self.is_running:
            return
        if self.is_running:
            current_ms = self.accumulated + self.elapsed_timer.elapsed()
        else:
            current_ms = self.accumulated
        diff_ms = current_ms - self.last_lap_time
        lap_num = len(self.laps) + 1
        diff_time = QTime(0, 0).addMSecs(diff_ms).toString("hh:mm:ss:zzz")
        total_time = QTime(0, 0).addMSecs(current_ms).toString("hh:mm:ss:zzz")
        line = f"Lap {lap_num:<18}+{diff_time:<25}{total_time}"
        self.laps_display.append(line)
        self.laps.append(current_ms)
        self.last_lap_time = current_ms

    def _update_clock(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_display.setText(f"Time: {current_time}")
        QTimer.singleShot(1000, self._update_clock)  # Update every second

    def apply_light_mode(self):
        icon_style = """
            QPushButton {
                background-color: #FFFFFF;
                border: 1px solid #E0E0E0;
                border-radius: 15px;
            }
            QPushButton:hover { background-color: #F0F0F0; }
            QPushButton:pressed {
                background-color: #E5E5E5;
                border: 1px solid #CCCCCC;
            }
        """
        self.main_timer_btn.setStyleSheet(icon_style)
        self.setting_btn.setStyleSheet(icon_style)

    def apply_dark_mode(self):
        icon_style = """
            QPushButton {
                background-color: #2D2D2D;
                border: 1px solid #3A3A3A;
                border-radius: 15px;
            }
            QPushButton:hover { background-color: #3A3A3A; }
            QPushButton:pressed {
                background-color: #252525;
                border: 1px solid #3A3A3A;
            }
        """
        self.main_timer_btn.setStyleSheet(icon_style)
        self.setting_btn.setStyleSheet(icon_style)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("app_icon.ico"))  # Global icon
    window = QMainWindow()
    timer_widget = CountdownTimer()
    window.setCentralWidget(timer_widget)
    window.setWindowTitle("Timer with Clock")
    window.resize(350, 630)
    window.setMaximumSize(350, 630)
    window.setMinimumSize(350, 630)
    window.setWindowIcon(QIcon("3158183.ico"))
    window.show()
    if darkdetect.isDark():
        timer_widget.apply_dark_mode()
    else:
        timer_widget.apply_light_mode()
    sys.exit(app.exec())