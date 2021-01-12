import asyncio

storage = {}

def process_data(data):
    
    try:
        splited = data.split()
        command = splited[0]
#         assert isinstance(splited[1], str)
        if command == 'put':
            assert len(splited) == 4 or data == 'get *\n'
            processed_data = (splited[1], 
                              float(splited[2]), 
                              int(splited[3]))
            if processed_data[0] not in storage.keys():
                storage[processed_data[0]] = {processed_data[2]:
                                              processed_data[1]}
            else:
                storage[processed_data[0]][processed_data[2]] = processed_data[1]
            return 'ok\n\n'
        elif command == 'get':
            processed_data = ''
            assert len(splited) == 2
            if splited[1] == '*':
                for key in storage.keys():
                    values = storage[key]
                    for timestamp, value in values.items():
                        processed_data += (str(key) + ' ' +
                                           str(value) + ' ' + 
                                           str(timestamp) + '\n')
            else:
                key = splited[1]
                if key in storage.keys():
                    values = storage[key]
                    for timestamp, value in values.items():
                        processed_data += (str(key) + ' ' +
                                           str(value) + ' ' + 
                                           str(timestamp) + '\n')
            processed_data = 'ok\n' + processed_data + '\n'
            return processed_data
        else:
            return 'error\nwrong command\n\n'
    except Exception as e:
        return 'error\nwrong command\n\n'
        
class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())

def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
    return server
# run_server('127.0.0.1', 10001)
