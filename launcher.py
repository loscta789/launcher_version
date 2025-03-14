import sys
import os
import webbrowser
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QProgressBar, QFrame
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QIcon,QPainter
from PyQt6.QtCore import Qt, QSize
import requests

class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        # Remove the title bar
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setFixedSize(1000, 600)  # Fixed size inspired by the Dofus launcher

        # 🌟 Main Layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # 🌟 Top Bar with tabs and control buttons at top-right
        self.top_bar_frame = QFrame(self)
        self.top_bar_frame.setFixedWidth(1000)
        self.top_bar_frame.setFixedHeight(55)
        self.top_bar_frame.setStyleSheet("background-color: black;  ")

        # Top bar content layout
        self.top_bar_layout = QVBoxLayout()

        # Row 1: Control buttons
        self.top_controls_layout = QHBoxLayout()
        self.top_controls_layout.addStretch()
        self.top_controls_layout.setSpacing(10)

        # Minimize button
        self.minimize_button = QPushButton("—", self)
        self.minimize_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minimize_button.setStyleSheet("color: white; font-size: 20px; border: none; background-color: transparent; font-weight: bold;")
        self.minimize_button.clicked.connect(self.showMinimized)
        self.top_controls_layout.addWidget(self.minimize_button)

        # Close button
        self.close_button = QPushButton("⨉", self)
        self.close_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_button.setStyleSheet("color: white; font-size: 20px; border: none; background-color: transparent; font-weight: bold;")
        self.close_button.clicked.connect(self.close)
        self.top_controls_layout.addWidget(self.close_button)

        self.top_bar_layout.addLayout(self.top_controls_layout)

        # Row 2: Tabs ("JEUX", "NEWS", etc.)
        self.top_tabs_layout = QHBoxLayout()
        self.top_tabs_layout.setSpacing(20)
        self.top_tabs_layout.setContentsMargins(0, 0, 20, 0)

        self.add_tab_button("JEUX")
        self.add_tab_button("NEWS")

        self.top_bar_layout.addLayout(self.top_tabs_layout)
        self.top_bar_frame.setLayout(self.top_bar_layout)
        self.main_layout.addWidget(self.top_bar_frame)

        # 🌟 Image display area under the top bar
        self.background_container = QFrame(self)
        # Leave the background_container transparent by default; its background will be set in set_background
        self.background_container.setStyleSheet("background: transparent;")
        self.main_layout.addWidget(self.background_container, stretch=1)

        # 🌟 Sidebar with icons (Logo, Discord, Website)
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setContentsMargins(10, 20, 10, 50)
        self.sidebar_frame = QFrame(self)
        self.sidebar_frame.setLayout(self.sidebar_layout)
        self.sidebar_frame.setFixedWidth(80)
        self.sidebar_frame.setFixedHeight(600)
        self.sidebar_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.7);")

        # Add icons with semi-transparent frame
        self.logo_button = self.add_icon_button("logo.png", None, selected=True)
        self.discord_button = self.add_icon_button("discord2-removebg-preview.png", "https://discord.com")
        self.website_button = self.add_icon_button(None, "https://example.com", text="W")
        self.sidebar_layout.addStretch()  # Add space at the bottom for balance

        self.main_layout.addWidget(self.sidebar_frame, alignment=Qt.AlignmentFlag.AlignLeft)

        # 🌟 Progress bar and Play button at the bottom
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(90, 20, 10, 5)
        self.bottom_layout.setSpacing(10)

        # Progress bar (visible by default)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(35)
        self.progress_bar.setFormat("%p%")  # Ensure it shows percentage
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text

        self.progress_bar.setStyleSheet("""
    QProgressBar {
        border: 2px solid white;
        border-radius: 5px;
        background-color: rgba(255, 255, 255, 30);
        text-align: center;  /* This centers the text inside the bar */
        color: white;  /* Ensure text is visible */
    }

    QProgressBar::chunk {
        background-color: #1E90FF;  /* Blue progress fill */
        border-radius: 5px;  /* Optional: rounded corners */
    }
""")

        self.bottom_layout.addWidget(self.progress_bar, stretch=1)

        # Play button
        self.play_button = QPushButton("PLAY", self)
        self.play_button.setEnabled(False)
        self.play_button.setFixedSize(QSize(180, 50))
        self.play_button.setStyleSheet("background-color: #1E90FF; color: white; font-size: 20px; font-weight: bold; border-radius: 8px; border: 2px solid white;")
        self.bottom_layout.addWidget(self.play_button)

        self.main_layout.addLayout(self.bottom_layout)
        self.setLayout(self.main_layout)

        # 🌟 Apply the background image after setting up all elements

        # 🌟 Version check at launch
        self.check_version()

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("thumbnail.jpg")
        if not pixmap.isNull():
            scaled = pixmap.scaled(self.width(), self.height() - 55, 
                                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                Qt.TransformationMode.SmoothTransformation)
            # Draw starting 55 pixels down from the top
            painter.drawPixmap(0, 55, scaled)
        super().paintEvent(event)

    def set_background(self, image_path):
        """ Définit une image de fond qui commence sous la barre du haut """
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            print(f"Erreur : Impossible de charger l'image {image_path}")
            return

        scaled_pixmap = pixmap.scaled(self.width(), self.height() - 55, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled_pixmap))
        self.setPalette(palette)

    def mousePressEvent(self, event):
        """Capture the initial mouse position when clicking."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        """Update the window position as it is dragged."""
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_position)
            self.drag_position = event.globalPosition().toPoint()
            event.accept()

    def add_icon_button(self, icon_path, url, text=None, selected=False):
        """Adds an icon button with hover effect."""
        button = QPushButton(self)
        button.setCursor(Qt.CursorShape.PointingHandCursor)

        if text:
            button.setText(text)
            button.setStyleSheet("color: white; font-size: 20px; font-weight: bold; border: none; background-color: transparent;")
        else:
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(40, 40))
            button.setFixedSize(QSize(60, 60))
            if selected:
                # Default background for selected (e.g., "logo.png")
                button.setStyleSheet("background-color: rgba(255, 255, 255, 0.2); border-radius: 10px; border: none;")
            else:
                button.setStyleSheet("background-color: transparent; border: none;")
        
        if url:
            button.clicked.connect(lambda: webbrowser.open(url))
        
        self.sidebar_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
        return button

    def add_tab_button(self, name):
        """Adds a button at the top for tabs (Jeux, News, etc.)"""
        button = QPushButton(name, self)
        button.setStyleSheet("color: white; font-size: 16px; font-weight: bold; border: none;")
        button.setFixedSize(QSize(100, 40))
        self.top_tabs_layout.addWidget(button)

    def check_version(self):
        local_version = "1.1"

        remote_version_url = "https://raw.githubusercontent.com/loscta789/launcher_version/refs/heads/main/version.txt?token=GHSAT0AAAAAADAAVY3FOKZABDKWTUBD7SG6Z6UK6HA"

        try:
            response = requests.get(remote_version_url, timeout=5)  # Fetch the latest version
            if response.status_code == 200:
                remote_version = response.text.strip()
                
                if remote_version != local_version:
                    print(f"A new version ({remote_version}) is available!")
                    self.progress_bar.setValue(0)  # 
                    # Trigger update logic here (download new version, notify user, etc.)
                else:
                    print("Your launcher is up-to-date.")

            else:
                print("Failed to check version. Server returned:", response.status_code)

        except requests.RequestException as e:
            print("Error checking for updates:", e)

        """Simulate a version check and enable the Play button if up-to-date."""
        self.play_button.setEnabled(True)
        self.play_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.progress_bar.setValue(100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = Launcher()
    launcher.show()

    launcher.check_version()# Simulate a version check at launch
    sys.exit(app.exec())
