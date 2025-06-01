# main.py


# =========================
# imports
# =========================
import sys
import db
import ui
from db import Expense
from PyQt5.QtWidgets import QApplication



# =========================
# testing db.py
# =========================
db.create_table()
# test_expense1 = Expense(None, "2025-05-29", "general", "test", 123.45, 0, "")
# test_expense2 = Expense(None, "2025-05-30", "food", "test2", 67.89, 1, "test comment")
# test_expense3 = Expense(None, "2025-05-31", "transport", "test3", 45.67, 0, "another comment")
# db.add_expense(test_expense1)
# db.add_expense(test_expense2)
# db.add_expense(test_expense3)



# =========================
# testing ui.py
# =========================
app = QApplication(sys.argv)
window = ui.Window()
window.show()
sys.exit(app.exec_())