# ui.py

# =========================
# imports
# =========================
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import db


# =========================
# UI class
# =========================
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyFinanceLog")
        self.setGeometry(100, 100, 1500, 750)
        self.setStyleSheet("background-color: white;")


        # create the main layout
        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setSpacing(0)
        self.setLayout(grid)
        
        
        # top bar
        self.top_bar = self.create_top_bar()
        grid.addWidget(self.top_bar, 0, 0, 1, 2)
        
        
        # side bar
        self.side_bar = self.create_side_bar()
        grid.addWidget(self.side_bar, 1, 0, 1, 1)
        
        
        # main content area
        self.main_content = self.create_main_content()
        grid.addWidget(self.main_content, 1, 1, 1, 1)
        
        
    # ========================
    # class methods
    # ========================
        
    def create_top_bar(self) -> QWidget:
        """"
        create top bar with logo and navigation buttons
        """
        # create top bar
        top_bar = QWidget()
        top_bar.setStyleSheet("background-color: lightgrey;")
        top_bar_height = 100
        top_bar.setFixedHeight(top_bar_height)
        
        # top bar layout
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(5, 5, 5, 5)
        top_layout.setSpacing(10)
        top_bar.setLayout(top_layout)
        
        # logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/MyFinanceLog_logo.png")
        logo_pixmap = logo_pixmap.scaledToHeight(top_bar_height)
        logo_label.setPixmap(logo_pixmap)
        
        # buttons
        main_btn = QPushButton("Main")
        monthly_btn = QPushButton("Monthly Overview")
        style_top_bar_btns(main_btn)
        style_top_bar_btns(monthly_btn)
        
        # add widgets to top layout
        top_layout.addWidget(logo_label)
        top_layout.addSpacing(150)
        top_layout.addWidget(main_btn)
        top_layout.addWidget(monthly_btn)
        top_layout.addStretch()
        
        return top_bar
    
    
    def create_side_bar(self) -> QWidget:
        """
        create side bar
        """
        side_bar = QWidget()
        side_bar.setStyleSheet("background-color: darkgrey;")
        side_bar.setFixedWidth(300)
        
        return side_bar
    
    
    def create_main_content(self) -> QWidget:
        """
        create main content area
        """
        main_content = QWidget()
        main_content.setStyleSheet("background-color: white;")
        
        # create layout for main content
        main_layout = QGridLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(30)
        main_content.setLayout(main_layout)
        
        # create title label
        title_label = QLabel("Recent Expenses")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(title_label, 0, 1, 1, 1)
        
        # placeholder
        placeholder = QLabel("spacing")
        main_layout.addWidget(placeholder, 1, 0, 1, 1)
        
        # create table with expenses
        self.expenses_table = QTableWidget()
        
        # format and column names
        self.expenses_table.setEditTriggers(QTableWidget.NoEditTriggers)  # make table read-only
        expenses = db.get_expenses()
        self.expenses_table.setRowCount(len(expenses))
        self.expenses_table.setColumnCount(len(db.Expense.fields) + 1)
        column_names = db.get_column_names()
        self.expenses_table.setHorizontalHeaderLabels(column_names + ["Edit", "Delete"])
        self.expenses_table.setStyleSheet("""
            QTableWidget {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        
        # populate table with expenses and buttons
        for row, expense in enumerate(expenses):
            for col, field in enumerate(db.Expense.fields[1:]):
                
                # get value from expense object
                value = getattr(expense, field)
                
                # format value based on field type
                if field == "date":
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignCenter)
                elif field == "amount":
                    item = QTableWidgetItem(f"{value:.2f}€")
                    item.setTextAlignment(Qt.AlignRight)
                elif field == "fixed":
                    item = QTableWidgetItem("Fixed" if value else "Variable")
                    item.setTextAlignment(Qt.AlignCenter)
                else:
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignLeft)
                
                # set item flags to prevent editing
                self.expenses_table.setItem(row, col, item)
            
            # create edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, expense_id=expense.id: self.edit_expense(expense_id))
            style_edit_btns(edit_btn)
            self.expenses_table.setCellWidget(row, len(db.Expense.fields) - 1, edit_btn)
            
            # create delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda _, expense_id=expense.id: self.delete_expense(expense_id))
            style_delete_btns(delete_btn)
            self.expenses_table.setCellWidget(row, len(db.Expense.fields), delete_btn)
        
        
        # add table to main layout
        main_layout.addWidget(self.expenses_table, 1, 1, 1, 1)
        
        
        return main_content
    
    
    # ========================
    # event handlers
    # ========================

    def delete_expense(self, expense_id):
        reply = QMessageBox.question(
            self,
            "Delete Expense",
            "Are you sure you want to delete this expense?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            # Hier deine Löschlogik, z.B.:
            db.delete_expense(expense_id)
            self.refresh_table()



# ========================
# design functions
# ========================

def style_top_bar_btns(button):
    button.setStyleSheet("""
        QPushButton {
            background-color: #888888;
            color: white;
            border-radius: 8px;
            padding: 6px 22px;
            font-size: 17px;
            min-width: 70px;
            max-width: 150px;
            min-height: 25px;
            max-height: 50px;
            border: 2px solid #555555;
        }
        QPushButton:hover {
            background-color: #555555;
            border: 2px solid #aaaaaa;
        }
        QPushButton:pressed {
            background-color: #888888;
        }
    """)


def style_edit_btns(button):
    button.setStyleSheet("""
        QPushButton {
            background-color: #00CD00;
            color: black;
            border-radius: 8px;
            padding: 6px 22px;
            font-size: 13px;
            min-width: 10px;
            max-width: 40px;
            min-height: 10px;
            max-height: 50px;
            border: 2px solid #555555;
        }
        QPushButton:hover {
            background-color: #00FF00;
            border: 2px solid #aaaaaa;
        }
        QPushButton:pressed {
            background-color: #888888;
        }
    """)


def style_delete_btns(button):
    button.setStyleSheet("""
        QPushButton {
            background-color: #CD0000;
            color: black;
            border-radius: 8px;
            padding: 6px 22px;
            font-size: 13px;
            min-width: 10px;
            max-width: 40px;
            min-height: 10px;
            max-height: 50px;
            border: 2px solid #555555;
        }
        QPushButton:hover {
            background-color: #FF0000;
            border: 2px solid #aaaaaa;
        }
        QPushButton:pressed {
            background-color: #888888;
        }
    """)
    
    