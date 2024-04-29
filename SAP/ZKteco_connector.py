from zk import ZK, const

conn = None

class ZKteco_connector:
    
    def __init__(self, ip_address, port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False):
        conn = None
        # create ZK instance
        zk = ZK(ip_address, port, timeout, password, force_udp, ommit_ping)
        
        # # zk = ZK('169.254.92.150', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
        # try:
        #     # connect to device
        #     conn = zk.connect()
        #     # disable device, this method ensures no activity on the device while the process is run
        #     conn.disable_device()
        #     # another commands will be here!
        #     # Example: Get All Users
        #     attendances = conn.get_attendance()
        #     for attendance in attendances:
        #         print(attendance.uid)
        #     users = conn.get_users()
        #     for user in users:
        #         privilege = 'User'
        #         if user.privilege == const.USER_ADMIN:
        #             privilege = 'Admin'
        #         print(user.id)
        #         print ('+ UID #{}'.format(user.uid))
        #         print ('  Name       : {}'.format(user.name))
        #         print ('  Privilege  : {}'.format(privilege))
        #         print ('  Password   : {}'.format(user.password))
        #         print ('  Group ID   : {}'.format(user.group_id))
        #         print ('  User  ID   : {}'.format(user.user_id))

        #     # Test Voice: Say Thank You
        #     conn.test_voice()
        #     # re-enable device after all commands already executed
        #     conn.enable_device()
        # except Exception as e:
        #     print ("Process terminate : {}".format(e))
        # finally:
        #     if conn:
        #         conn.disconnect()
            
