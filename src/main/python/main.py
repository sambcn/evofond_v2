from fbs_runtime.application_context.PyQt5 import ApplicationContext
from fbs_runtime.platform import is_windows

from front.MainWindow import MainWindow

# import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    if is_windows():
        appctxt.app.setStyle("Fusion")
    window = MainWindow(appctxt)
    # window.resize(250, 150)
    window.show()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    # sys.exit(exit_code)