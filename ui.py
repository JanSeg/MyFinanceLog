# ui.py

# =========================
# imports
# =========================
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import db


# =========================
# UI class
# =========================
class Window(QWidget):
    """
    Main application window for MyFinanceLog.

    This class sets up the main layout, including the top bar, side bar,
    and the main content area with the expenses table.
    """
    
    def __init__(self) -> None:
        """
        initialize the main window and set up the layout.
        """
        super().__init__()
        self.setWindowTitle("MyFinanceLog")
        self.setGeometry(100, 100, 1450, 750)
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
        TOP_BAR_HEIGHT = 100
        top_bar.setFixedHeight(TOP_BAR_HEIGHT)
        
        # top bar layout
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(5, 5, 5, 5)
        top_layout.setSpacing(10)
        top_bar.setLayout(top_layout)
        
        # logo
        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/MyFinanceLog_logo.png")
        logo_pixmap = logo_pixmap.scaledToHeight(TOP_BAR_HEIGHT)
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
        main_layout.setSpacing(10)
        main_content.setLayout(main_layout)
        
        # create title label
        title_label = QLabel("Recent Expenses")
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 10px;
        """)
        title_label.setContentsMargins(0, 18, 0, 9)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label, 0, 1, 1, 1)
        
        # placeholder
        # placeholder_left = QLabel("spacing")
        # placeholder_right = QLabel("spacing")
        placeholder_bottom = QLabel("spacing")
        placeholder_bottom.setStyleSheet("color: transparent;")
        # main_layout.addWidget(placeholder_left, 1, 0, 1, 1)
        # main_layout.addWidget(placeholder_right, 1, 2, 1, 1)
        main_layout.addWidget(placeholder_bottom, 2, 1, 1, 1)
        
        # create table with expenses
        self.expenses_table = QTableWidget()
        
        # format and column names
        self.expenses_table.setEditTriggers(QTableWidget.NoEditTriggers)  # make table read-only
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
        
        self._populate_expenses_table()
        
        # add table to main layout
        main_layout.addWidget(self.expenses_table, 1, 1, 1, 1)
        
        return main_content
    
    
    def _populate_expenses_table(self) -> None:
        """
        populate the expenses table with data from the database
        """
        expenses = db.get_expenses()
        self.expenses_table.setRowCount(len(expenses))
        
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
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                elif field == "fixed":
                    item = QTableWidgetItem("Fixed" if value == 1 else "Variable")
                    item.setTextAlignment(Qt.AlignCenter)
                elif field == "comment":
                    # truncate long comments and add a tooltip with full text
                    if len(value) > 50:
                        item = QTableWidgetItem(value[:40] + "...")
                        item.setToolTip(value)
                    else:
                        item = QTableWidgetItem(value)
                else:
                    item = QTableWidgetItem(str(value))
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                
                # set item flags to prevent editing
                self.expenses_table.setItem(row, col, item)
            
            
            # create edit button
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda _, expense_id=expense.id: self.edit_expense(expense_id))
            style_edit_btns(edit_btn)
            
            # create a widget to center the edit button
            edit_widget = QWidget()
            edit_layout = QHBoxLayout(edit_widget)
            edit_layout.addWidget(edit_btn)
            edit_layout.setContentsMargins(0, 0, 0, 0)
            edit_layout.setAlignment(Qt.AlignCenter)

            # add the edit button
            EDIT_COL_INDEX = len(db.Expense.fields) - 1
            self.expenses_table.setCellWidget(row, EDIT_COL_INDEX, edit_btn)
            
            
            # create delete button
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda _, expense_id=expense.id: self.delete_expense(expense_id))
            style_delete_btns(delete_btn)
            
            # create a widget to center the delete button
            delete_widget = QWidget()
            delete_layout = QHBoxLayout(delete_widget)
            delete_layout.addWidget(delete_btn)
            delete_layout.setContentsMargins(0, 0, 0, 0)
            delete_layout.setAlignment(Qt.AlignCenter)

            # add the delete button
            DELETE_COL_INDEX = len(db.Expense.fields)
            self.expenses_table.setCellWidget(row, DELETE_COL_INDEX, delete_btn)
        
        
        # resize columns to fit content
        self.expenses_table.resizeColumnsToContents()
        self.expenses_table.setColumnWidth(EDIT_COL_INDEX, 80)
        self.expenses_table.setColumnWidth(DELETE_COL_INDEX, 80)
        total_width = sum(self.expenses_table.columnWidth(i) for i in range(self.expenses_table.columnCount()))
        # self.expenses_table.setMinimumWidth(total_width + 25)
        self.expenses_table.setMaximumWidth(total_width + 30)
        # self.expenses_table.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        
    
    # ========================
    # event handlers
    # ========================
    
    def edit_expense(self, expense_id) -> None:
        """
        pop up a dialog to edit an expense
        call the edit_expense method from db.py if confirmed
        call the refresh_table method to update the table
        """
        reply = QMessageBox.question(
            self,
            "Edit Expense",
            
            # pop up with 
        )
    

    def delete_expense(self, expense_id) -> None:
        """
        pop up a confirmation dialog to delete an expense
        call the delete_expense method from db.py if confirmed
        call the refresh_table method to update the table
        """
        reply = QMessageBox.question(
            self,
            "Delete Expense",
            "Are you sure you want to delete this expense?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            db.delete_expense(expense_id)
            self.refresh_table()
    
    
    def refresh_table(self) -> None:
        """
        refresh the expenses table
        """
        self._populate_expenses_table()  
    



# ========================
# design functions
# ========================

def style_top_bar_btns(button) -> None:
    """
    style the top bar buttons for the navigation
    """
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


def style_edit_btns(button) -> None:
    """
    style the edit buttons in the expenses table
    """
    button.setStyleSheet("""
        QPushButton {
            background-color: #00CD00;
            color: black;
            border-radius: 8px;
            padding: 3px 6px;
            font-size: 13px;
            min-width: 45px;
            max-width: 45px;
            min-height: 12px;
            max-height: 12px;
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


def style_delete_btns(button) -> None:
    """
    style the delete buttons in the expenses table 
    """
    button.setStyleSheet("""
        QPushButton {
            background-color: #CD0000;
            color: black;
            border-radius: 8px;
            padding: 3px 6px;
            font-size: 13px;
            min-width: 45px;
            max-width: 45px;
            min-height: 12px;
            max-height: 12px;
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
    
    