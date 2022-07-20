import time

class TimerError(Exception):
    print("Erro no controlador")

class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()
        print("aqui")
        t.stop()

    def stop(self):
        #Para o timer e report o
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        #elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        #print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        print("aqui agora")
        time.sleep(5)
        t.start()

t = Timer()
t.start()
#t.stop()  # A few seconds later

