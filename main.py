import os
import sys
import time

# Adding Teslasuit Python API to path before using
ts_api_path = os.environ['TESLASUIT_PYTHON_API_PATH']
sys.path.append(ts_api_path)

import f1_client
import ts_client

class F1TeslatuitForceFeedback:
    def start(self):
        self.f1_client = f1_client.F1Client()
        self.ts_client = ts_client.TsClient()
        self.f1_client.init()
        self.f1_client.set_event_callback(self.ts_client.process_ff_events)
        self.ts_client.init()
        while True:
            self.f1_client.process()

ff = F1TeslatuitForceFeedback()
ff.start()
