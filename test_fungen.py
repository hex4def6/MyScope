from lantz.drivers.examples import LantzSignalGenerator

inst = LantzSignalGenerator('TCPIP::localhost::5678::SOCKET')
inst.initialize()
print(inst.idn)
inst.finalize()
