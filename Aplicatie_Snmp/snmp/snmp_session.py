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
'''
def get_value(host, oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               UsmUserData(userName='ROBERT',
                           authKey='cisco12345',
                           privKey='cambium12345',
                           authProtocol=usmHMACMD5AuthProtocol,
                           privProtocol=usmDESPrivProtocol
                           ), UdpTransportTarget((host, 161)), ContextData(), ObjectType(ObjectIdentity(oid)), ))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            print(varBind)
            # print(' = '.join([x.prettyPrint() for x in varBind]))
'''

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
    "Admin Status": '1.3.6.1.2.1.2.2.1.7',
    "Oper Status": '1.3.6.1.2.1.2.2.1.8',
    "Incoming Octets": '1.3.6.1.2.1.2.2.1.10',
    "Incoming Unicast Packets": '1.3.6.1.2.1.2.2.1.11',
    "Incoming Multicast Packets": '1.3.6.1.2.1.2.2.1.12',
    "Incoming Discarded Packets": '1.3.6.1.2.1.2.2.1.13',
    "Incoming Error Packets": '1.3.6.1.2.1.2.2.1.14',
    "Incoming Unknown Packets": '1.3.6.1.2.1.2.2.1.15',
    "Outgoing Octets": '1.3.6.1.2.1.2.2.1.16',
    "Outgoing Unicast Packets": '1.3.6.1.2.1.2.2.1.17',
    "Outgoing Multicast Packets": '1.3.6.1.2.1.2.2.1.18',
    "Outgoing Discarded Packets": '1.3.6.1.2.1.2.2.1.19',
    "Outgoing Error Packets": '1.3.6.1.2.1.2.2.1.20',
}

# x.get_value('1.3.6.1.4.1.9.9.109.1.1.1.1.10.1')
# values = x.get([oids.values()])

'''
for a, b in oids.items():
    get_value = x.get([b])
    for c, d in get_value.items():
        print(a, ':', d)
'''

temp_list = []
for values in interface_oids.values():
    temp_list.append(values)
print(temp_list)

def retrieve_interface_data(oids, count_oid='1.3.6.1.2.1.2.1.0'):
    z = x.get_bulk_auto(oids=oids, count_oid=count_oid)
    return z


x = retrieve_interface_data(temp_list)


for dict_list in x:
    temp_list_2 = []
    for value in dict_list.values():
        temp_list_2.append(value)
    times += 1
    print(temp_list_2)
