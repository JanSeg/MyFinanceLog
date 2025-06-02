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
test_expense1 = Expense(None, "2025-05-29", "general", "test", 123.45, 0, "")
test_expense2 = Expense(None, "2025-05-30", "food", "test2", 67.89, 1, "test comment")
test_expense3 = Expense(None, "2025-05-31", "transport", "test3", 45.67, 0, "another long comment, lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
test_expense4 = Expense(None, "2025-06-01", "entertainment", "test4", 89.99, 0, "short comment")
test_expense5 = Expense(None, "2025-06-02", "utilities", "test5", 150.00, 1, "another comment")
test_expense6 = Expense(None, "2025-06-03", "health", "test6", 200.00, 0, "yet another comment")
test_expense7 = Expense(None, "2025-06-04", "education", "test7", 300.00, 1, "final comment")
test_expense8 = Expense(None, "2025-06-05", "miscellaneous", "test8", 50.00, 0, "misc comment")
test_expense9 = Expense(None, "2025-06-06", "travel", "test9", 400.00, 1, "travel comment")
test_expense10 = Expense(None, "2025-06-07", "clothing", "test10", 75.00, 0, "clothing comment")

db.add_expense(test_expense1)
db.add_expense(test_expense2)
db.add_expense(test_expense3)
db.add_expense(test_expense4)
db.add_expense(test_expense5)
db.add_expense(test_expense6)
db.add_expense(test_expense7)
db.add_expense(test_expense8)
db.add_expense(test_expense9)
db.add_expense(test_expense10)


# =========================
# testing ui.py
# =========================
app = QApplication(sys.argv)
window = ui.Window()
window.show()
sys.exit(app.exec_())