from .snmp_session import SnmpSession
from pysnmp import hlapi
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .snmp_session import generate_interfaces_data
x = SnmpSession(host='192.168.1.1',
                userName='ROBERT',
                authKey='cisco12345',
                privKey='cambium12345',
                authProtocol=hlapi.usmHMACMD5AuthProtocol,
                privProtocol=hlapi.usmDESPrivProtocol)

def startt():
    scheduler = BackgroundScheduler()
    scheduler.add_job(x.update_interface_data,  trigger='interval', seconds=10)
    print(generate_interfaces_data(x.retrieve_interface_data()[2]))
    scheduler.start()

