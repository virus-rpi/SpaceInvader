from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory

# Configuration variables
MINECRAFT_SERVER_IP = "localhost"
MINECRAFT_SERVER_PORT = 25565
PROXY_LISTENER_IP = "localhost"
PROXY_LISTENER_PORT = 25566


class MinecraftProxyProtocol(Protocol):
    def __init__(self):
        self.server_transport = None

    def connectionMade(self):
        print("Client connected:", self.transport.getPeer())

        # Connect to the Minecraft server
        server_factory = MinecraftServerFactory(self)
        reactor.connectTCP(MINECRAFT_SERVER_IP, MINECRAFT_SERVER_PORT, server_factory)

    def dataReceived(self, data):
        print("Received from client:", data)

        # Forward data to the Minecraft server
        if self.server_transport is not None:
            self.server_transport.write(data)

    def serverPacketReceived(self, data):
        print("Received from server:", data)

        # Forward data to the client
        self.transport.write(data)

    def connectionLost(self, reason):
        print("Client disconnected:", self.transport.getPeer())
        if self.server_transport is not None:
            self.server_transport.loseConnection()

    # Called when the connection to the Minecraft server is established
    def serverConnectionMade(self, server_transport):
        print("Connected to Minecraft server:", server_transport.getPeer())
        self.server_transport = server_transport

    # Called when the connection to the Minecraft server is lost
    def serverConnectionLost(self, reason):
        if self.server_transport is not None:
            print("Disconnected from Minecraft server:", self.server_transport.getPeer())
            self.server_transport = None
        self.transport.loseConnection()


class MinecraftProxyFactory(Factory):
    protocol = MinecraftProxyProtocol


class MinecraftServerProtocol(Protocol):
    def connectionMade(self):
        print("Connected to Minecraft server:", self.transport.getPeer())

        # Associate the server transport with the proxy protocol
        self.factory.proxy_protocol.serverConnectionMade(self.transport)

    def dataReceived(self, data):
        print("Received from server:", data)

        # Forward data to the proxy protocol
        if self.factory.proxy_protocol is not None:
            self.factory.proxy_protocol.serverPacketReceived(data)

    def connectionLost(self, reason):
        print("Disconnected from Minecraft server:", self.transport.getPeer())
        if self.factory.proxy_protocol is not None:
            self.factory.proxy_protocol.serverConnectionLost(reason)


class MinecraftServerFactory(Factory):
    protocol = MinecraftServerProtocol

    def __init__(self, proxy_protocol):
        self.proxy_protocol = proxy_protocol

    def startedConnecting(self, connector):
        print("Connecting to Minecraft server...")

    def clientConnectionFailed(self, connector, reason):
        print("Connection to Minecraft server failed:", reason)
        self.proxy_protocol.serverConnectionLost(reason)

    def buildProtocol(self, addr):
        protocol_instance = self.protocol()
        protocol_instance.factory = self
        return protocol_instance

    def clientConnectionLost(self, connector, reason):
        if self.proxy_protocol is not None:
            self.proxy_protocol.serverConnectionLost(reason)


if __name__ == '__main__':
    proxy_factory = MinecraftProxyFactory()
    reactor.listenTCP(PROXY_LISTENER_PORT, proxy_factory, interface=PROXY_LISTENER_IP)
    print("Minecraft proxy server started on", PROXY_LISTENER_IP + ":" + str(PROXY_LISTENER_PORT))
    reactor.run()
