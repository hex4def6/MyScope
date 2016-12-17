from lantz import Feat
from lantz.messagebased import MessageBasedDriver

class LantzSignalGenerator(MessageBasedDriver):
    """Lantz Signal Generator.
    """

    DEFAULTS = {'COMMON': {'write_termination': '\n',
                           'read_termination': '\n'}}

    @Feat()
    def idn(self):
        return self.query('?IDN')


if __name__ == '__main__':
    with LantzSignalGenerator('TCPIP::localhost::5678::SOCKET') as inst:
        print('The identification of this instrument is : ' + inst.idn)

