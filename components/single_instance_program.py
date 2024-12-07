import sys

from PySide6.QtCore import QSharedMemory

class SingleInstanceProgram:
    """Single Instance App Class with cleanup support."""

    def __init__(self, key: str) -> None:
        """Initialize class."""
        self.shared_memory = QSharedMemory(key)
        self.is_running = self.shared_memory.attach() or not self.shared_memory.create(1)

    def __enter__(self):
        """Enter the runtime context."""
        return self  # type: ignore

    def __exit__(self, exc_type: type, exc_value: Exception, traceback: type) -> None:
        """Exit the runtime context and perform cleanup."""
        if self.shared_memory.isAttached():
            self.shared_memory.detach()

if __name__ == '__main__':
    def test():
        SINGLE_INSTANCE = True
        SINGLE_INSTANCE_KEY = 'xtestesttest'

        import time
        from PySide6.QtWidgets import QApplication

        APP = QApplication()

        def initProgram() -> None:
            try:
                print('Running program...')
                while True:
                    print('Working...')
                    time.sleep(1)
            except Exception as err:
                print(err)
                QApplication.exit(0)
                sys.exit(0)

        def initEventLoop(app) -> None:
            exit_code = app.exec()  # Starts the Qt event loop
            sys.exit(exit_code)  # Exits with the status code returned from the Qt event loop

        if SINGLE_INSTANCE:
            # Prevent multiple instances of the program from running at the same time
            with SingleInstanceProgram(SINGLE_INSTANCE_KEY) as instance:
                if instance.is_running:
                    print('Another instance of this application is already running.')
                    QApplication.exit(0)
                    sys.exit(0)
                
                initProgram(), initEventLoop(APP)
        else:
            initProgram(), initEventLoop(APP)
    
    try:
        test()
    except Exception as err:
        print(err)

# python Components/single_instance_program.py