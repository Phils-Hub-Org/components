import psutil
from PySide6.QtCore import QThread, Signal

class ProcessDetectorThread(QThread):
    process_started = Signal(object)  # Signal for a new process
    process_terminated = Signal(object)  # Signal for a terminated process
    
    def __init__(self) -> None:
        super().__init__()
        self.processInterrupted = False
        self.processes = {}  # Dictionary to store process pid -> (Process object, Process name)
    
    def run(self) -> None:
        tracked_pids = {p.pid for p in psutil.process_iter()}

        while not self.processInterrupted:
            # Get the current running processes
            current_pids = {p.pid for p in psutil.process_iter()}
            new_pids = current_pids - tracked_pids
            terminated_pids = tracked_pids - current_pids

            # Emit signal for newly launched processes and store process object and name
            for pid in new_pids:
                try:
                    process = psutil.Process(pid)
                    process_name = process.name()
                    self.processes[pid] = (process, process_name)  # Store process object and name
                    self.process_started.emit(process)
                    QThread.msleep(1000)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue

            # Emit signal for terminated processes and use stored data for the process name
            for pid in terminated_pids:
                if pid in self.processes:
                    # Retrieve the process name from the stored data
                    process_name = self.processes[pid][1]
                    self.process_terminated.emit(process_name)
                    del self.processes[pid]  # Remove the terminated process from the dictionary

            # Update the tracked process list
            tracked_pids = current_pids

            QThread.msleep(1000)
    
    def exitProcessDetectorLoop(self) -> None:
        self.processInterrupted = True

if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    app = QApplication()

    process_detector_thread = ProcessDetectorThread()
    process_detector_thread.process_started.connect(lambda process: print(f'New process detected: {process.name()} (PID: {process.pid})'))
    process_detector_thread.process_terminated.connect(lambda process_name: print(f'Process terminated: <<{process_name}>>'))
    process_detector_thread.finished.connect(lambda: print('Process detector thread finished'))
    process_detector_thread.start()

    app.exec()