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
# test_expense3 = Expense(None, "2025-05-31", "transport", "test3", 45.67, 0, "another long comment, lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
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