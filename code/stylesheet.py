stylesheet = """
    QWidget {
        background: #4d4d4d;
        selection-background-color: #6cc9ff;
        selection-color: #1a1a1a;
        color: #ececec;
    }

    QWidget:disabled {
        background: #333333;
        color: #4d4d4d;
    }

    QLabel {
        padding-left: 3px;
    }

    QTabWidget::pane {
        border: 1px solid #333333;
    }

    QTabBar::tab {
        background: #4d4d4d;
        border: transparent;
        padding-top: 3px;
        padding-bottom: 3px;
        padding-left: 10px;
        padding-right: 10px;
    }

    QTabBar::tab:selected, QTabWidget::tab:hover {
        background: #6cc9ff;
    }

    QTabBar::tab:selected {
        border-color: #6cc9ff;
        color: #1a1a1a;
    }

    QTabBar::tab:!selected {
        margin-top: 2px;
    }

    QTreeView::item:selected:active, QTreeView::item:selected:!active {
        background: #ff58b2;
        font: #1a1a1a;
    }

    QTreeView::item:hover {
        background: #ff9dd2;
    }

    QTreeView {
        color: #1a1a1a;
    }

    QTreeView, QTableView {
        border: transparent;
    }

    QHeaderView::section {
        background: #6cc9ff;
        border: 1px solid #20adff;
        color: #1a1a1a;
        padding-left: 3px;
    }

    QMenuBar::item:selected {
        background: #6cc9ff;
    }

    QMenuBar {
        border-bottom-color: transparent;
    }

    QToolBar {
        border: 1px solid #333333;
    }

    QPushButton {
        border: 1px solid #333333;
        padding: 3 8px;
        min-width: 40px;
    }

    QPushButton:pressed, QPushButton:checked, QPushButton:hover, QPushButton:!active,
    QToolButton:pressed, QToolButton:checked, QToolButton:hover {
        background: #808080;
        border: 3px solid #808080;
    }

    QPushButton:disabled, QToolButton:disabled {
        background: #ff7946;
        color: #1a1a1a;
    }

    QPushButton:hover, QPushButton:pressed, QPushButton:checked{
        color: #1a1a1a;
    }

    QLineEdit, QComboBox, QPlainTextEdit, QSpinBox {
        border: 1px solid #333333;
        padding-top: 3px;
        padding-bottom: 3px;
        padding-left: 2px;
    }

    QComboBox::drop-down {
        border-left: 1px solid #333333;
    }

    QComboBox::down-arrow, QSpinBox::down-arrow {
        image: url(code/resources/icons/downarrow.png);
    }

    QSpinBox::up-arrow {
        image: url(code/resources/icons/uparrow.png);
        width: 10px;
    }

    QSpinBox::down-arrow {
        width: 10px;
    }

    QComboBox::down-arrow:disabled, QSpinBox::down-arrow:disabled {
        image: url(code/resources/icons/downarrow-disabled.png);
    }

    QSpinBox::up-arrow:disabled {
        image: url(code/resources/icons/uparrow-disabled.png);
    }

    QComboBox::down-arrow:selected, QComboBox::down-arrow:hover,
    QSpinBox::down-arrow:selected, QSpinBox::down-arrow:hover {
        image: url(code/resources/icons/downarrow-selected.png);
    }

    QSpinBox::up-arrow:selected, QSpinBox::up-arrow:hover {
        image: url(code/resources/icons/uparrow-selected.png);
    }

    QSpinBox::up-button, QSpinBox::down-button {
        border-left: 1px solid #333333;
    }

    QScrollBar::handle:horizontal, QScrollBar::handle:vertical {
        border: 1px solid #333333;
        background: #666666;
    }

    QScrollBar::sub-page:vertical, QScrollBar::sub-page:horizontal,
    QScrollBar::add-page:vertical, QScrollBar::add-page:horizontal {
        background: #808080;
        color: #808080;
        border: transparent;
    }
"""