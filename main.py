from pyfedappwrap.engine.runtime import FedDBEngine

from app import SpliceDriftApp

engine = FedDBEngine()
engine.register(SpliceDriftApp())

if __name__ == "__main__":
    engine.start()
    engine.wait_until_stop()
