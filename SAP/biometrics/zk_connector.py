from zk import ZK, const

class ZK :
    def __init__(self, ip, port, timeout, password, force_udp, ommit_ping):
        self.conn = None
        zk = ZK(ip, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
        try:
            self.conn = zk.connect()
        except Exception as e:
            print ("Process terminate : {}".format(e))
      