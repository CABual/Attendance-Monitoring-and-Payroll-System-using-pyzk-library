from zk import ZK, const
from biometrics.models import Attendances, Employee

conn = None
# create ZK instance
zk = ZK('169.254.92.150', port=4370, timeout=5, password=0, force_udp=False, ommit_ping=False)
try:
    # connect to device
    conn = zk.connect()
    # disable device, this method ensures no activity on the device while the process is run
    conn.disable_device()
    # another commands will be here!
    # Example: Get All Users
    attendances = conn.get_attendance()
    user_id = []
    user_id_set = set(attendance.user_id for attendance in attendances)
    print(user_id_set)
    
    employee_list = []
    employee_list = set(attendance.user_id for attendance in attendances)
    # print(user_id_set)

    for employee in employee_list:
        new_employee = Employee(user_id="3123", name="ca")
        new_employee.save()
    # for attendance in attendances:
    #     new_attendance = Attendances(uid=attendance.uid,
    #                                     timestamp = attendance.timestamp,
    #                                     status = attendance.status,
    #                                     punch= attendance.punch, 
    #                                     employee =  )
    #     print(attendance.uid, attendance.user_id)
    users = conn.get_users()
    for user in users:
        privilege = 'User'
        if user.privilege == const.USER_ADMIN:
            privilege = 'Admin'
        print(user.uid)
        print ('+ UID #{}'.format(user.uid))
        print ('  Name       : {}'.format(user.name))
        print ('  Privilege  : {}'.format(privilege))
        print ('  Password   : {}'.format(user.password))
        print ('  Group ID   : {}'.format(user.group_id))
        print ('  User  ID   : {}'.format(user.user_id))

    # Test Voice: Say Thank You
    conn.test_voice()
    # re-enable device after all commands already executed
    conn.enable_device()
except Exception as e:
    print ("Process terminate : {}".format(e))
finally:
    if conn:
        conn.disconnect()