"""
SNMPv3: auth MD5, privacy DES
+++++++++++++++++++++++++++++

Send SNMP GET request using the following options:

* with SNMPv3, user 'usr-md5-des', MD5 authentication, DES encryption
* over IPv4/UDP
* to an Agent at demo.snmplabs.com:161
* for IF-MIB::ifInOctets.1 MIB object

Available authentication protocols:

#. usmHMACMD5AuthProtocol
#. usmHMACSHAAuthProtocol
#. usmHMAC128SHA224AuthProtocol
#. usmHMAC192SHA256AuthProtocol
#. usmHMAC256SHA384AuthProtocol
#. usmHMAC384SHA512AuthProtocol
#. usmNoAuthProtocol

Available privacy protocols:

#. usmDESPrivProtocol
#. usm3DESEDEPrivProtocol
#. usmAesCfb128Protocol
#. usmAesCfb192Protocol
#. usmAesCfb256Protocol
#. usmNoPrivProtocol

Functionally similar to:

| $ snmpget -v3 -l authPriv -u usr-md5-des -A authkey1 -X privkey1 demo.snmplabs.com IF-MIB::ifInOctets.1

snmp-server view  ALL-ACCESS iso included
snmp-server group GROUP1 v3 priv read ALL-ACCESS
snmp-server user ROBERT GROUP1 v3 auth md5 CISCO priv 3des CAMBIUM
snmp-server user ROBERT GROUP1 v3 auth  md5 cisco12345 priv des cambium12345
"""  #
from pysnmp import hlapi
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler


class SnmpSession:

    def __init__(self, host, userName, authKey, privKey, authProtocol, privProtocol):
        self.host = host
        self.username = userName
        self.authKey = authKey
        self.privKey = privKey
        self.authProtocol = authProtocol
        self.privProtocol = privProtocol

    def __construct_object_types(self, list_of_oids):
        object_types = []
        for oid in list_of_oids:
            object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
        return object_types

    def __cast(self, value):
        try:
            return int(value)
        except (ValueError, TypeError):
            try:
                return float(value)
            except (ValueError, TypeError):
                try:
                    return str(value)
                except (ValueError, TypeError):
                    pass
        return value

    def __fetch(self, handler, count):
        result = []
        for i in range(count):
            try:
                error_indication, error_status, error_index, var_binds = next(handler)
                if not error_indication and not error_status:
                    items = {}
                    for var_bind in var_binds:
                        items[str(var_bind[0])] = self.__cast(var_bind[1])
                    result.append(items)
                else:
                    raise RuntimeError('Got SNMP error: f{error_indication}')
            except StopIteration:
                break
        return result

    def get_value(self, oid):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            hlapi.getCmd(hlapi.SnmpEngine(),
                   hlapi.UsmUserData(userName=self.username,
                               authKey=self.authKey,
                               privKey=self.privKey,
                               authProtocol=self.authProtocol,
                               privProtocol=self.privProtocol),
                   hlapi.UdpTransportTarget((self.host, 161)),
                   hlapi.ContextData(),
                   hlapi.ObjectType(hlapi.ObjectIdentity(oid))))

        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                # print(varBind)
                print(' = '.join([x.prettyPrint() for x in varBind]))

    def get(self, oids):
        handler = hlapi.getCmd(hlapi.SnmpEngine(),
                  hlapi.UsmUserData(userName=self.username,
                              authKey=self.authKey,
                              privKey=self.privKey,
                              authProtocol=self.authProtocol,
                              privProtocol=self.privProtocol),
                  hlapi.UdpTransportTarget((self.host, 161)), hlapi.ContextData(),
                         *self.__construct_object_types(oids)
        )
        return self.__fetch(handler, 1)[0]

    def get_bulk(self, oids, count, start_from=0):
        handler = hlapi.bulkCmd(hlapi.SnmpEngine(),
                  hlapi.UsmUserData(userName=self.username,
                              authKey=self.authKey,
                              privKey=self.privKey,
                              authProtocol=self.authProtocol,
                              privProtocol=self.privProtocol),
                  hlapi.UdpTransportTarget((self.host, 161)), hlapi.ContextData(),
                                start_from, count,
                         *self.__construct_object_types(oids))
        return self.__fetch(handler, count)

    def get_bulk_auto(self, oids, count_oid, start_from=0):
        count = self.get([count_oid])[count_oid]
        return self.get_bulk(oids, count, start_from)

    def retrieve_interface_data(self, oids, count_oid='1.3.6.1.2.1.2.1.0'):
        z = self.get_bulk_auto(oids=oids, count_oid=count_oid)
        return z

    def __repr__(self):
        return self.username


x = SnmpSession(host='192.168.1.1',
                userName='ROBERT',
                authKey='cisco12345',
                privKey='cambium12345',
                authProtocol=hlapi.usmHMACMD5AuthProtocol,
                privProtocol=hlapi.usmDESPrivProtocol)

oids = {
    'hostname': '1.3.6.1.4.1.9.2.1.3.0',
    'iosVersion': '1.3.6.1.4.1.9.10.102.1.1.1.0',
    'CPU5Seconds': '1.3.6.1.4.1.9.9.109.1.1.1.1.10.1',
    'CPU1Minute': '1.3.6.1.4.1.9.9.109.1.1.1.1.7.1',
    'CPU5Minutes': '1.3.6.1.4.1.9.9.109.1.1.1.1.8.1',
    'ceva': '1.3.6.1.2.1.2.2.1.10'
}


interface_oids = {
    "Description": '1.3.6.1.2.1.2.2.1.2',
    "MTU": '1.3.6.1.2.1.2.2.1.4',
    "Speed": '1.3.6.1.2.1.2.2.1.5',
    "Admin_Status": '1.3.6.1.2.1.2.2.1.7',
    "Oper_Status": '1.3.6.1.2.1.2.2.1.8',
    "Incoming_Octets": '1.3.6.1.2.1.2.2.1.10',
    "Incoming_Unicast_Packets": '1.3.6.1.2.1.2.2.1.11',
    "Incoming_Multicast_Packets": '1.3.6.1.2.1.2.2.1.12',
    "Incoming_Discarded_Packets": '1.3.6.1.2.1.2.2.1.13',
    "Incoming_Error_Packets": '1.3.6.1.2.1.2.2.1.14',
    "Incoming_Unknown_Packets": '1.3.6.1.2.1.2.2.1.15',
    "Outgoing_Octets": '1.3.6.1.2.1.2.2.1.16',
    "Outgoing_Unicast_Packets": '1.3.6.1.2.1.2.2.1.17',
    "Outgoing_Multicast_Packets": '1.3.6.1.2.1.2.2.1.18',
    "Outgoing_Discarded_Packets": '1.3.6.1.2.1.2.2.1.19',
    "Outgoing_Error_Packets": '1.3.6.1.2.1.2.2.1.20',
}

y = x.retrieve_interface_data(interface_oids.values())


def generate_interfaces_data(dic1, dic2=None):
    if dic2 is None:
        dic2 = interface_oids

    new_dict = dict(zip(dic2.keys(), dic1.values()))

    if new_dict['Admin_Status'] == 2:
        new_dict['Admin_Status'] = 'Down'
    elif new_dict['Admin_Status'] == 1:
        new_dict['Admin_Status'] = 'Up'

    if new_dict['Oper_Status'] == 2:
        new_dict['Oper_Status'] = 'Down'
    elif new_dict['Oper_Status'] == 1:
        new_dict['Oper_Status'] = 'Up'

    if new_dict['Speed'] == 1000000000:
        new_dict['Speed'] = '1Gbps'

    elif new_dict['Speed'] == 10000000:
        new_dict['Speed'] = '10Mbps'
    return new_dict


Ethernet0 = generate_interfaces_data(y[0])
GigabitEthernet0 = generate_interfaces_data(y[1])
GigabitEthernet1 = generate_interfaces_data(y[1])
GigabitEthernet2 = generate_interfaces_data(y[3])
GigabitEthernet3 = generate_interfaces_data(y[4])
GigabitEthernet4 = generate_interfaces_data(y[5])
GigabitEthernet5 = generate_interfaces_data(y[6])
GigabitEthernet6 = generate_interfaces_data(y[7])

interfaces_data = [Ethernet0, GigabitEthernet0, GigabitEthernet1, GigabitEthernet2, GigabitEthernet3, GigabitEthernet4,
                   GigabitEthernet5, GigabitEthernet6,]

print(interfaces_data)