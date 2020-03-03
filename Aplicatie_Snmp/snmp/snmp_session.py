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
from pysnmp.hlapi import *
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

    def __init__(self, userName, authKey, privKey, authProtocol, privProtocol):
        self.username = userName
        self.authKey = authKey
        self.privKey = privKey
        self.authProtocol = authProtocol
        self.privProtocol = privProtocol

    def get_value(self, host, oid):
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(SnmpEngine(),
                   UsmUserData(userName=self.username,
                               authKey=self.authKey,
                               privKey=self.privKey,
                               authProtocol=self.authProtocol,
                               privProtocol=self.privProtocol
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

    def __repr__(self):
        return self.username


x = SnmpSession(userName='ROBERT',
                authKey='cisco12345',
                privKey='cambium12345',
                authProtocol=usmHMACMD5AuthProtocol,
                privProtocol=usmDESPrivProtocol)

x.get_value(host='192.168.1.1', oid='1.3.6.1.4.1.9.9.109.1.1.1.1.10.1')

# get_value('192.168.1.1', '1.3.6.1.4.1.9.9.109.1.1.1.1.10.1')  # CPU 5 Seconds
# get_value('192.168.1.1', '1.3.6.1.4.1.9.9.109.1.1.1.1.7.1')  # CPU 1 Minutes
# get_value('192.168.1.1', '1.3.6.1.4.1.9.9.109.1.1.1.1.8.1')  # CPU 5 Minutes
