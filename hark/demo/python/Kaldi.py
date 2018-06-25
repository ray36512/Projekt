import KaldiReceiver
import json
import subprocess
import time

import os
import os.path

class KaldiDecoderDetector:
    def __init__(self, kaldiport=10500, options=["--config=kaldi_conf/online.conf"], path=""):
        self.options = list(options)
        self.runKaldi(path, jconfs=self.options)
        time.sleep(10)
        self.proxy = KaldiReceiver.KaldiReceiver(port=kaldiport)

    def runKaldi(self, path, jconfs):
        cmd = "{}kaldidecoder {}".format(path, " ".join(jconfs))

        self.proc = subprocess.Popen(cmd, shell=True)
        print "waiting for kaldi..."

    def mainloop(self, interval):
        self.outfilehandle = open("kaldi_out.txt", "w")
        while True:
            # invoke if kaldi is dead
            self.proxy.getResult()
            result = self.proxy.parseResult()
            resultdump = json.dumps(result)
            print resultdump
            self.outfilehandle.write(('%d, %f, %s\n' % (result["SOURCEID"], result["AZIMUTH"], result["SENTENCE"])))
        #self.outfilehandle.close()



if __name__ == "__main__":
    obj = KaldiDecoderDetector()
    obj.mainloop(0.01)
