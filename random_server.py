# from twisted.internet import reactor
# from quarry.net.proxy import DownstreamFactory, Bridge
#
#
# class QuietBridge(Bridge):
#     quiet_mode = False
#
#     def packet_upstream_chat_message(self, buff):
#         buff.save()
#         chat_message = self.read_chat(buff, "upstream")
#         self.logger.info(" >> %s" % chat_message)
#
#         if chat_message.startswith("/quiet"):
#             # Switch mode
#             self.quiet_mode = not self.quiet_mode
#
#             action = self.quiet_mode and "enabled" or "disabled"
#             msg = "Quiet mode %s" % action
#             self.downstream.send_packet("chat_message",
#                                         self.write_chat(msg, "downstream"))
#
#         elif self.quiet_mode and not chat_message.startswith("/"):
#             # Don't let the player send chat messages in quiet mode
#             msg = "Can't send messages while in quiet mode"
#             self.downstream.send_packet("chat_message",
#                                         self.write_chat(msg, "downstream"))
#
#         else:
#             # Pass to upstream
#             buff.restore()
#             self.upstream.send_packet("chat_message", buff.read())
#
#     def packet_downstream_chat_message(self, buff):
#         chat_message = self.read_chat(buff, "downstream")
#         self.logger.info(" :: %s" % chat_message)
#
#         if self.quiet_mode and chat_message.startswith("<"):
#             # Ignore message we're in quiet mode and it looks like chat
#             pass
#
#         else:
#             # Pass to downstream
#             buff.restore()
#             self.downstream.send_packet("chat_message", buff.read())
#
#     def read_chat(self, buff, direction):
#         buff.save()
#         if direction == "upstream":
#             p_text = buff.unpack_string()
#             return p_text
#         elif direction == "downstream":
#             p_text = str(buff.unpack_chat())
#
#             # 1.7.x
#             if self.upstream.protocol_version <= 5:
#                 p_position = 0
#
#             # 1.8.x
#             else:
#                 p_position = buff.unpack('B')
#
#             if p_position in (0, 1):
#                 return p_text
#
#     def write_chat(self, text, direction):
#         if direction == "upstream":
#             return self.buff_type.pack_string(text)
#         elif direction == "downstream":
#             data = self.buff_type.pack_chat(text)
#
#             # 1.7.x
#             if self.downstream.protocol_version <= 5:
#                 pass
#
#             # 1.8.x
#             else:
#                 data += self.buff_type.pack('B', 0)
#
#             return data
#
#
# class QuietDownstreamFactory(DownstreamFactory):
#     bridge_class = QuietBridge
#     motd = "Random Server"
#
#
# def main(argv):
#     # Parse options
#     import argparse
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-a", "--listen-host", default="localhost", help="address to listen on")
#     parser.add_argument("-p", "--listen-port", default=25565, type=int, help="port to listen on")
#     parser.add_argument("-b", "--connect-host", default="93.186.198.18", help="address to connect to")
#     parser.add_argument("-q", "--connect-port", default=25565, type=int, help="port to connect to")
#     args = parser.parse_args(argv)
#
#     # Create factory
#     factory = QuietDownstreamFactory()
#     factory.connect_host = args.connect_host
#     factory.connect_port = args.connect_port
#
#     # Listen
#     factory.listen(args.listen_host, args.listen_port)
#     reactor.run()
#
#
#
# if __name__ == "__main__":
#    import sys
#    main(sys.argv[1:])
import json
from xmlrpc.client import ProtocolError
import requests
from twisted.python import failure

from twisted.internet import reactor
from quarry.types.uuid import UUID
from quarry.net.proxy import UpstreamFactory, Upstream, DownstreamFactory, Downstream, Bridge
from quarry.net import auth, crypto
from twisted.internet import reactor


class MyUpstream(Upstream):
    def packet_login_encryption_request(self, buff):
        p_server_id = buff.unpack_string()

        # 1.7.x
        if self.protocol_version <= 5:
            def unpack_array(b): return b.read(b.unpack('h'))
        # 1.8.x
        else:
            def unpack_array(b): return b.read(b.unpack_varint(max_bits=16))

        p_public_key = unpack_array(buff)
        p_verify_token = unpack_array(buff)

        if not self.factory.profile.online:
            raise ProtocolError("Can't log into online-mode server while using"
                                " offline profile")

        self.shared_secret = crypto.make_shared_secret()
        self.public_key = crypto.import_public_key(p_public_key)
        self.verify_token = p_verify_token

        # make digest
        digest = crypto.make_digest(
            p_server_id.encode('ascii'),
            self.shared_secret,
            p_public_key)

        # do auth
        # deferred = self.factory.profile.join(digest)
        # deferred.addCallbacks(self.auth_ok, self.auth_failed)

        url = "https://sessionserver.mojang.com/session/minecraft/join"

        payload = json.dumps({
            "accessToken": self.factory.profile.access_token,
            "selectedProfile": self.factory.profile.uuid.to_hex(False),
            "serverId": digest
        })
        headers = {
            'Content-Type': 'application/json'
        }

        r = requests.request(
            "POST", "https://sessionserver.mojang.com/session/minecraft/join", headers=headers, data=payload)

        if r.status_code == 204:
            self.auth_ok(r.text)
        else:
            self.auth_failed(failure.Failure(
                auth.AuthException('unverified', 'unverified username')))


class MyDownstream(Downstream):
    def packet_login_encryption_response(self, buff):
        if self.login_expecting != 1:
            raise ProtocolError("Out-of-order login")

        # 1.7.x
        if self.protocol_version <= 5:
            def unpack_array(b): return b.read(b.unpack('h'))
        # 1.8.x
        else:
            def unpack_array(b): return b.read(b.unpack_varint(max_bits=16))

        p_shared_secret = unpack_array(buff)
        p_verify_token = unpack_array(buff)

        shared_secret = crypto.decrypt_secret(
            self.factory.keypair,
            p_shared_secret)

        verify_token = crypto.decrypt_secret(
            self.factory.keypair,
            p_verify_token)

        self.login_expecting = None

        if verify_token != self.verify_token:
            raise ProtocolError("Verify token incorrect")

        # enable encryption
        self.cipher.enable(shared_secret)
        self.logger.debug("Encryption enabled")

        # make digest
        digest = crypto.make_digest(
            self.server_id.encode('ascii'),
            shared_secret,
            self.factory.public_key)

        # do auth
        remote_host = None
        if self.factory.prevent_proxy_connections:
            remote_host = self.remote_addr.host

        # deferred = auth.has_joined(
        #     self.factory.auth_timeout,
        #     digest,
        #     self.display_name,
        #     remote_host)
        # deferred.addCallbacks(self.auth_ok, self.auth_failed)

        r = requests.get('https://sessionserver.mojang.com/session/minecraft/hasJoined',
                         params={'username': self.display_name, 'serverId': digest, 'ip': remote_host})

        if r.status_code == 200:
            self.auth_ok(r.json())
        else:
            self.auth_failed(failure.Failure(
                auth.AuthException('invalid', 'invalid session')))


class MyUpstreamFactory(UpstreamFactory):
    protocol = MyUpstream

    connection_timeout = 10


class MyBridge(Bridge):
    upstream_factory_class = MyUpstreamFactory

    def make_profile(self):
        """
        Support online mode
        """

        # follow: https://kqzz.github.io/mc-bearer-token/

        accessToken = 'eyJhbGciOiJIUzI1NiJ9.eyJ4dWlkIjoiMjUzNTQyNTA4NjkyNjA1MCIsImFnZyI6IkNoaWxkIiwic3ViIjoiYmU4ZDQzNmQtYjExMS00MDAyLWIxYzEtM2U1NjA0OWI1MTQxIiwibmJmIjoxNjY1NTAwMTU2LCJhdXRoIjoiWEJPWCIsInJvbGVzIjpbXSwiaXNzIjoiYXV0aGVudGljYXRpb24iLCJleHAiOjE2NjU1ODY1NTYsImlhdCI6MTY2NTUwMDE1NiwicGxhdGZvcm0iOiJVTktOT1dOIiwieXVpZCI6IjQyYjg3M2NiNWMzNzZkYTFhODVhMjllYWZhOTY1NmM3In0.-8O8YswP0lxrHubQ0GQ_Qjkioj49IhkLtRguWacK3Jk'

        url = "https://api.minecraftservices.com/minecraft/profile"
        headers = {'Authorization': 'Bearer ' + accessToken}
        response = requests.request("GET", url, headers=headers)
        result = response.json()
        myUuid = UUID.from_hex(result['id'])
        myUsername = result['name']
        return auth.Profile('(skip)', accessToken, myUsername, myUuid)


class MyDownstreamFactory(DownstreamFactory):
    protocol = MyDownstream
    bridge_class = MyBridge
    motd = "Proxy Server"


def main(argv):
    # Parse options
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a1", "--listen-host1", default="127.0.0.1",
                        help="address to listen on")
    parser.add_argument("-p1", "--listen-port1", default=25565,
                        type=int, help="port to listen on")
    parser.add_argument("-b", "--connect-host",
                        default="79.242.76.72", help="address to connect to")
    parser.add_argument("-q", "--connect-port", default=25565,
                        type=int, help="port to connect to")
    args = parser.parse_args(argv)

    # Create factory
    factory = MyDownstreamFactory()
    factory.connect_host = args.connect_host
    factory.connect_port = args.connect_port

    # Listen
    factory.listen(args.listen_host1, args.listen_port1)
    reactor.run()


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])