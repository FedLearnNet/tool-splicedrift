"""Local test runner — runs the app in TEST_MODE without Docker."""

from pyfedappwrap.engine.runtime import FedDBEngine

from app import SpliceDriftApp

engine = FedDBEngine(test_mode=True)
engine.register(SpliceDriftApp())

if __name__ == "__main__":
    engine.start()
    engine.wait_until_stop()
