from quarry.net.auth import Profile
import msmcauth
from twisted.internet import reactor, defer
from quarry.net.client import ClientFactory, SpawningClientProtocol
from quarry.net.auth import ProfileCLI


class Protocol(SpawningClientProtocol):
    pass


class Factory(ClientFactory):
    protocol = Protocol


@defer.inlineCallbacks
def run(args):
    # Log in
    with open("login.txt") as f:
        auth = f.readlines()
        email = auth[0].strip("\n")
        pw = auth[1].strip("\n")
        token = auth[2].strip("\n")

    loginDetails = yield msmcauth.login(email, pw)

    profile = Profile.from_token(token, loginDetails.access_token, loginDetails.username, loginDetails.uuid)

    # Create factory
    factory = Factory(profile)

    # Connect!
    factory.connect(args.host, args.port)


def main(argv):
    parser = ProfileCLI.make_parser()
    parser.add_argument("host")
    parser.add_argument("-p", "--port", default=25565, type=int)
    args = parser.parse_args(argv)

    run(args)
    reactor.run()

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
