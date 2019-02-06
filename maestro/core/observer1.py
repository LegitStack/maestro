import threading
import time

class Downloader(threading.Thread):

    def run(self):
        print('downloading')
        for i in range(1,5):
            self.i = i
            time.sleep(2)
            print(self.i)
        return 'hello world'

t = Downloader()
print(t.start())
