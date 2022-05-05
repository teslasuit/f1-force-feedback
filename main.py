import f1_client
import ts_client

class F1TeslatuitForceFeedback:
    def start(self):
        self.f1_client = f1_client.F1Client()
        self.ts_client = ts_client.TsClient()

        self.f1_client.init()
        #self.ts_client.init("C:/Users/v.avdeev/Documents/Projects/teslasuit-studio/bin/Debug/teslasuit_api.dll")
        while True:
            self.f1_client.process()

ff = F1TeslatuitForceFeedback()
ff.start()
