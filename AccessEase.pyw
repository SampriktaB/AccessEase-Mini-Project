"""
AccessEase - Native Windowed Desktop Application (.pyw)
This file opens directly with NO background black terminal window when double-clicked.
"""

from desktop_app import AccessEaseDesktopApp

if __name__ == "__main__":
    app = AccessEaseDesktopApp()
    app.mainloop()
