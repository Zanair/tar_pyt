import asyncio
import random
import argparse
import sys
import signal
import os
import datetime


class Parameters:  # global configuration parameters and data
    delay = 0  # delay in seconds, converted from user input
    config_file = False  # if loading from config file, not yet implemented
    banner_length = 0  # size string to send each period
    max_clients = 0  # maximum number of connections,  subsequent attempts are denied
    listen_port = 0  # port
    verbose = False  # terminal output enabled
    connections = []  # list of current connections and related data


class Connection:
    number = 0
    time = 0  # total seconds connected
    bytes = 0  # total bytes sent
    socket = ''  # string of connection ID info


p = Parameters()


def log_msg(verbose, message):  # prints verbose terminal output
    if verbose:
        print(message)


async def handler(_reader, writer):  # establishes new connections and asynchronously maintains them
    try:
        sock = writer.get_extra_info('socket')
        c = Connection()
        if sock is not None:
            c.socket = str(sock.getpeername())
            if len(p.connections) >= p.max_clients:  # if new connection and max clients already reached
                log_msg(p.verbose, str('Attempted connection from: ' + str(c.socket) + ', at maximum clients'))
                sock.close()  # close connection
                return
            log_msg(p.verbose, str('Connected: ' + str(c.socket) + '   Client [' + str(c.number) + '/' +
                                   str(p.max_clients) + ']'))
            p.connections.append(c)
            c.number = len(p.connections) + 1
        while True:
            await asyncio.sleep(p.delay)
            writer.write(b'%x\r\n' % random.randint(0, 2 ** p.banner_length))  # write random data of configured size
            c.time += p.delay
            c.bytes += p.banner_length
            await writer.drain()
    except ConnectionResetError:  # on client disconnect
        log_msg(p.verbose, str('Disconnected: ' + str(c.socket) + '   Time connected: ' + str(
            datetime.timedelta(seconds=c.time)) + '   Bytes sent: ' + str(
            c.bytes)))
        p.connections.remove(c)
        pass


def stdin_read():  # reads console input non-blocking
    data = sys.stdin.readline()
    if 'log' == data.strip():  # when prompted print all connections and thier information
        print(
            str('[' + str(len(p.connections)) + '/' + str(p.max_clients) + ']').center(os.get_terminal_size().columns))
        if len(p.connections) != 0:
            for x in range(len(p.connections)):
                print('[' + str(x) + '/' + str(p.max_clients) + ']   ' + p.connections[
                    x].socket + '   Time connected: ' + str(
                    datetime.timedelta(seconds=p.connections[x].time)) + '   Bytes sent: ' + str(
                    p.connections[x].bytes))


async def main():

    signal.signal(signal.SIGINT, lambda x, y: sys.exit(0))  # allows clean exit on keyboard interrupt

    parser = argparse.ArgumentParser(description='Python tar pit, type "log" for current connection statistics')
    parser.add_argument('-d', default=10000, help='Message millisecond delay [10000]')
    parser.add_argument('-f', action='store_true', help='Set and load config file [Not yet implemented]')
    parser.add_argument('-l', default=32, help='Maximum banner line length (3-255) [32]')
    parser.add_argument('-m', default=4096, help='Maximum number of clients [4096]')
    parser.add_argument('-p', default=2222, help='Listening port')
    parser.add_argument('-v', action='store_true', help='Print diagnostics to standard output')
    arguments = parser.parse_args()

    p.delay = int(arguments.d) / 1000
    p.config_file = bool(arguments.f)
    p.banner_length = int(arguments.l)
    p.max_clients = int(arguments.m)
    p.listen_port = int(arguments.p)
    p.verbose = bool(arguments.v)

    if (p.banner_length < 3) or (p.banner_length > 255):
        sys.exit('Banner length must be between 3 and 255')
    if p.max_clients > 4096:
        sys.exit('Maximum clients must be less than 4096')

    print('Starting Tar_Pyt')
    print('Delay: ' + str(arguments.d) + ' milliseconds')
    print('Max Banner LengthL: ' + str(p.banner_length))
    print('Max Clients: ' + str(p.max_clients))
    print('Port: ' + str(p.listen_port))
    print('Verbose: ' + str(p.verbose))

    server = await asyncio.start_server(handler, '0.0.0.0', p.listen_port)  # start server
    loop = asyncio.get_event_loop()
    loop.add_reader(sys.stdin, stdin_read)
    async with server:
        try:
            await server.serve_forever()
        except KeyboardInterrupt:
            server.close()


asyncio.run(main())
