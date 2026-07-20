"""UI styling module"""

DARK_THEME = """
QMainWindow {
    background-color: #1e1e1e;
    color: #ffffff;
}

QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
}

QLineEdit, QTextEdit, QComboBox, QSpinBox {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #404040;
    border-radius: 4px;
    padding: 5px;
    selection-background-color: #0d47a1;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 2px solid #0d7aff;
}

QPushButton {
    background-color: #0d47a1;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    margin: 2px;
}

QPushButton:hover {
    background-color: #0d7aff;
}

QPushButton:pressed {
    background-color: #0a3d91;
}

QPushButton:disabled {
    background-color: #404040;
    color: #808080;
}

QTableWidget, QTableWidgetItem {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #404040;
}

QTableWidget::item:selected {
    background-color: #0d47a1;
}

QHeaderView::section {
    background-color: #1a1a1a;
    color: #ffffff;
    padding: 5px;
    border: 1px solid #404040;
}

QMenuBar {
    background-color: #1e1e1e;
    color: #ffffff;
    border-bottom: 1px solid #404040;
}

QMenuBar::item:selected {
    background-color: #0d47a1;
}

QMenu {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #404040;
}

QMenu::item:selected {
    background-color: #0d47a1;
}

QLabel {
    color: #ffffff;
}

QProgressBar {
    border: 1px solid #404040;
    border-radius: 4px;
    background-color: #2d2d2d;
    height: 20px;
}

QProgressBar::chunk {
    background-color: #0d47a1;
}

QTabWidget {
    background-color: #1e1e1e;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #ffffff;
    padding: 8px 20px;
    border: 1px solid #404040;
}

QTabBar::tab:selected {
    background-color: #0d47a1;
}

QStatusBar {
    background-color: #2d2d2d;
    color: #ffffff;
    border-top: 1px solid #404040;
}

QGroupBox {
    color: #ffffff;
    border: 1px solid #404040;
    border-radius: 4px;
    margin-top: 10px;
    padding-top: 10px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 3px 0 3px;
}
"""

LIGHT_THEME = """
QMainWindow {
    background-color: #ffffff;
    color: #000000;
}

QWidget {
    background-color: #ffffff;
    color: #000000;
}

QLineEdit, QTextEdit, QComboBox, QSpinBox {
    background-color: #f5f5f5;
    color: #000000;
    border: 1px solid #cccccc;
    border-radius: 4px;
    padding: 5px;
    selection-background-color: #e3f2fd;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
    border: 2px solid #0d47a1;
}

QPushButton {
    background-color: #0d47a1;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    margin: 2px;
}

QPushButton:hover {
    background-color: #0d7aff;
}

QPushButton:pressed {
    background-color: #0a3d91;
}

QTableWidget, QTableWidgetItem {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #cccccc;
}

QTableWidget::item:selected {
    background-color: #e3f2fd;
}
"""

def get_theme_stylesheet(theme='dark'):
    """Get stylesheet for theme"""
    if theme.lower() == 'light':
        return LIGHT_THEME
    else:
        return DARK_THEME
