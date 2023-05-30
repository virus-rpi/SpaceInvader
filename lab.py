from mcstatus import JavaServer


def get_plugin_list(server_ip, server_port):
    # Create a MinecraftServer object
    server = JavaServer.lookup(f"{server_ip}:{server_port}")

    # Query the server for status
    status = server.status()

    # Retrieve the plugin information
    plugin_list = status.raw
    return plugin_list


# Usage
server_ip = 'localhost'
server_port = 25565

plugins = get_plugin_list(server_ip, server_port)
print(plugins)
