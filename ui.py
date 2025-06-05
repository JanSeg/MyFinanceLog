# ui.py

# =========================
# imports
# =========================
from PyQt5.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QSizePolicy, QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QCheckBox, QTextEdit, QDateEdit, QStackedWidget, QComboBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QDate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
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
        
        # call the parent constructor and set the window title, geometry, and style
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
        self.top_bar, self.main_btn, self.monthly_btn = self.create_top_bar()
        grid.addWidget(self.top_bar, 0, 0, 1, 2)
        
        
        # side bar
        self.side_bar = self.create_side_bar()
        grid.addWidget(self.side_bar, 1, 0, 1, 1)
        
        
        # main content area
        self.stacked_content = QStackedWidget()
        self.main_content = self.create_main_content()
        self.monthly_content = self.create_monthly_content()
        self.stacked_content.addWidget(self.main_content)       # index 0
        self.stacked_content.addWidget(self.monthly_content)    # index 1
        self.main_btn.clicked.connect(lambda: self.stacked_content.setCurrentIndex(0))
        self.monthly_btn.clicked.connect(lambda: self.stacked_content.setCurrentIndex(1))
        self.main_btn.click()
        grid.addWidget(self.stacked_content, 1, 1, 1, 1)
        
        
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
        
        return top_bar, main_btn, monthly_btn
    
    
    def create_side_bar(self) -> QWidget:
        """
        create side bar
        """
        
        # create side bar
        side_bar = QWidget()
        side_bar.setStyleSheet("background-color: darkgrey;")
        side_bar.setFixedWidth(300)
        
        # side bar layout
        side_layout = QVBoxLayout()
        side_layout.setContentsMargins(10, 10, 10, 10)
        side_layout.setSpacing(20)
        side_bar.setLayout(side_layout)
        
        # button for adding a new expense
        add_expense_btn = QPushButton("Add Expense")
        style_side_bar_btns(add_expense_btn)
        add_expense_btn.clicked.connect(lambda _: self.add_expense())
        side_layout.addWidget(add_expense_btn)
        
        
        return side_bar
    
    
    def create_main_content(self) -> QWidget:
        """
        create main content area
        """
        
        # create main content area
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
        self.expenses_table.scrollToBottom()
        
        # add table to main layout
        main_layout.addWidget(self.expenses_table, 1, 1, 1, 1)
        
        return main_content
    
    
    def _populate_expenses_table(self) -> None:
        """
        populate the expenses table with data from the database
        """
        
        # get expenses from the database
        # and set the number of rows in the table
        expenses = db.get_expenses()
        self.expenses_table.setRowCount(len(expenses))
        
        # set column for edit and delete buttons
        EDIT_COL_INDEX = len(db.Expense.fields) - 1
        DELETE_COL_INDEX = len(db.Expense.fields)
        
        # populate the table with expense data
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
            self.expenses_table.setCellWidget(row, DELETE_COL_INDEX, delete_btn)
        
        
        # resize columns to fit content
        self.expenses_table.resizeColumnsToContents()
        self.expenses_table.setColumnWidth(EDIT_COL_INDEX, 80)
        self.expenses_table.setColumnWidth(DELETE_COL_INDEX, 80)
        total_width = sum(self.expenses_table.columnWidth(i) for i in range(self.expenses_table.columnCount()))
        TABLE_PADDING = 30
        # self.expenses_table.setMinimumWidth(total_width + TABLE_PADDING)
        self.expenses_table.setMaximumWidth(total_width + TABLE_PADDING)
        # self.expenses_table.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

    
    def create_monthly_content(self) -> QWidget:    # the current version is just a placeholder, generated by Copilot
                                                    # method is not yet implemented
        """
        create monthly overview content area
        """
        
        # create monthly content area
        monthly_content = QWidget()
        monthly_content.setStyleSheet("background-color: white;")
        monthly_layout = QGridLayout()
        monthly_layout.setContentsMargins(10, 10, 10, 10)
        monthly_layout.setSpacing(10)
        monthly_content.setLayout(monthly_layout)

        # get expenses and calculate totals by category for selected month
        expenses = db.get_expenses()
        current_month = datetime.date.today().strftime("%Y-%m")
        category_totals = {}
        for expense in expenses:
            if str(expense.date).startswith(current_month):
                category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount

        # create pie chart
        fig = Figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        if category_totals:
            # append percentage ans total amount to labels
            values = list(category_totals.values())
            keys = list(category_totals.keys())
            total = sum(values)
            labels = [
                f"{key} {value / total * 100:.1f}%, {value:.2f}€"
                for key, value in zip(keys, values)
            ]
            # create pie chart with values and labels
            ax.pie(
                values,
                labels = labels,
                startangle = 90,
                wedgeprops = dict(width=0.3, edgecolor='w')
            )
            ax.set_title("Expenses by Category")
        else:
            ax.text(0.5, 0.5, "No data for this month", ha='center', va='center')

        # create canvas for the pie chart
        canvas = FigureCanvas(fig)
        monthly_layout.addWidget(canvas, 0, 0, 1, 1)

        return monthly_content

        
    
    # ========================
    # event handlers
    # ========================
    
    def add_expense(self) -> None:
        """
        pop up a dialog to add a new expense using the ExpenseDialog class
        call the add_expense method from db.py if confirmed
        call the refresh_table method to update the table
        """
        
        dialog = ExpenseDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            expense_data = dialog.get_expense_data()
            db.add_expense(expense_data)
            self.refresh_table()
    
    
    def edit_expense(self, expense_id) -> None:
        """
        pop up a dialog to edit an expense using the ExpenseDialog class
        call the edit_expense method from db.py if confirmed
        call the refresh_table method to update the table
        """
        
        expense = db.get_expense_by_id(expense_id)
        dialog = ExpenseDialog(self, expense)
        if dialog.exec_() == QDialog.Accepted:
            expense_data = dialog.get_expense_data()
            db.edit_expense(expense_id, expense_data)
            self.refresh_table()
        
    
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
# expense dialog class
# ========================

class ExpenseDialog(QDialog):
    """
    dialog for adding or editing an expense
    """
    def __init__(self, parent=None, expense=None):
        """
        initialize the dialog with input fields for expense data
        """
        
        # call the parent constructor and set up window
        super().__init__(parent)
        self.setWindowTitle("Edit Expense" if expense else "Add Expense")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)
        
        # date input field
        layout.addWidget(QLabel("Date:"))
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        layout.addWidget(self.date_input)
        layout.addSpacing(10)
        
        # category input field
        layout.addWidget(QLabel("Category:"))
        self.category_input = QComboBox()
        categories = db.get_categories()
        self.category_input.addItems(categories)
        self.category_input.setEditable(True)
        layout.addWidget(self.category_input)
        layout.addSpacing(10)
        
        # name input field
        layout.addWidget(QLabel("Name:"))
        self.name_input = QLineEdit()
        layout.addWidget(self.name_input)
        layout.addSpacing(10)
        
        # amount input field
        layout.addWidget(QLabel("Amount (€):"))
        self.amount_input = QLineEdit()
        layout.addWidget(self.amount_input)
        layout.addSpacing(10)
        
        # fixed checkbox
        self.fixed_checkbox = QCheckBox("Fixed")
        self.fixed_checkbox.setChecked(False)
        layout.addWidget(self.fixed_checkbox)
        layout.addSpacing(10)
        
        # comment input field
        layout.addWidget(QLabel("Comment:"))
        self.comment_input = QTextEdit()
        # smaller the size of comment input field
        self.comment_input.setFixedHeight(100)
        layout.addWidget(self.comment_input)
        layout.addSpacing(10)
        
        # buttons
        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Save")
        self.cancel_btn = QPushButton("Cancel")
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        
        
        # populate fields if editing an expense
        if expense:
            self.date_input.setDate(QDate.fromString(expense.date, "yyyy-MM-dd"))
            self.category_input.setCurrentText(expense.category)
            self.name_input.setText(str(expense.name))
            self.amount_input.setText(str(expense.amount))
            self.fixed_checkbox.setChecked(bool(expense.fixed))
            self.comment_input.setText(str(expense.comment))
        else:
            # set default values for adding a new expense
            self.date_input.setDate(QDate.currentDate())
            self.category_input.setCurrentText("please select a category")
            self.name_input.setText("")
            self.amount_input.setText("0.00")
            self.fixed_checkbox.setChecked(False)
            self.comment_input.setText("")
    
       
    def get_expense_data(self) -> dict:
        """
        get the data from the input fields and return it as a dictionary
        """
        
        return {
            "date": self.date_input.text(),
            "category": self.category_input.currentText(),
            "name": self.name_input.text(),
            "amount": float(self.amount_input.text()),
            "fixed": 1 if self.fixed_checkbox.isChecked() else 0,
            "comment": self.comment_input.toPlainText()
        }



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


def style_side_bar_btns(button) -> None:
    """
    style the side bar buttons
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
    
    