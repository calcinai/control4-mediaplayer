import socket
import random
import select


def send_udp_command(command, host, port, timeout=10):
    COUNTER = "0s2a" + str(random.randint(10, 99))
    COMMAND = COUNTER + " " + command + " \r\n"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    sock.setblocking(False)
    sock.sendto(bytes(COMMAND, "utf-8"), (host, port))

    received = ""
    ready = select.select([sock], [], [], 1)
    if ready[0]:
        received = str(sock.recv(1024), "utf-8")
        sock.close()

    return received


class Control4Amp(object):
    def __init__(self, host, port, timeout):
        self._host = host
        self._port = port
        self._timeout = timeout

    @property
    def is_available(self) -> bool:
        """Indicate if the amp is currently available."""

        try:
            send_udp_command("c4.amp", self._host, self._port, self._timeout)
        except TimeoutError:
            return False

        # Maybe should it in some way, probably.
        # Just a guess that we use this payload (in lieu of a real ping)
        return True


class Control4AmpInput(object):
    # Represents an input of a Control 4 Matrix Amp

    def __init__(self, amp, channel, name, gain, digital=False):
        self._amp = amp
        self._channel = channel
        self._name = name
        self._gain = gain
        self._digital = digital

    @property
    def amp(self):
        return self._amp


class Control4AmpChannel(object):
    # Represents a channel of a Control 4 Matrix Amp

    def __init__(self, amp, channel):
        self._amp = amp
        self._channel = channel
        self._source = 1
        self._volume = 0
        self._balance = 0

    @property
    def amp(self):
        return self._amp

    @property
    def channel(self):
        return self._channel

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value):
        self._source = value
        send_udp_command("c4.amp.out 0" + str(self._channel) + " 0" + str(self._source), self._host, self._port)

    @source.deleter
    def source(self):
        del self._source

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        self._source = value
        send_udp_command("c4.amp.balance 0" + str(self._channel) + " " + str(self._balance), self._host, self._port)

    @balance.deleter
    def balance(self):
        del self._balance

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value):
        self._volume = value
        new_volume = int(float(self._volume) * 100) + 160
        new_volume = hex(new_volume)[2:]
        send_udp_command("c4.amp.chvol 0" + str(self._channel) + " " + new_volume, self._host, self._port)

    @volume.deleter
    def volume(self):
        del self._volume

    def turn_on(self):
        return send_udp_command("c4.amp.out 0" + str(self._channel) + " 0" + str(self._source), self._host, self._port)

    def turn_off(self):
        return send_udp_command("c4.amp.out 0" + str(self._channel) + " 00", self._host, self._port)
