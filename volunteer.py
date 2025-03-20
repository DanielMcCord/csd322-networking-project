from messages import *
from socket import *
import ssl

class Volunteer:
    """
    A class that repeatedly asks for work from the Coordinator, performs the
    work, and then reports the results to the Coordinator.
    """

    def __init__(self, coordinator_host: str, coordinator_port: int):
        """
        Constructs a Volunteer who will talk to the specified Coordinator
        server.
        """

        self.coordinator_host = coordinator_host
        self.coordinator_port = coordinator_port

    def connect(self) -> socket|None:
        """
        Connects to the Coordinator using TCP on IPv4 and returns the connection
        socket.
        """

        sock = socket(AF_INET, SOCK_STREAM)
        try:
            sock.connect((self.coordinator_host, self.coordinator_port))
        except ConnectionRefusedError:
            sock.close()
            return None
        return sock
    
    def get_work(self) -> GetWorkResponse|None:
        """
        Connects to the Coordinator, asks for work, and returns the response.
        """
        sock = self.connect()
        if not sock:
            return None
        sock.send(GetWorkRequest().serialize().encode())
        with sock.makefile('r') as response_file:
            response = Message.deserialize(response_file)

        sock.close()
        return response

    
    def do_work(self, get_work_response: GetWorkResponse) -> dict:
        """
        Performs the work denoted by get_work_response and returns the
        word-counts. This is a simple implementation that counts all words
        that have more than 5 characters. You don't need to modify this and can
        use it as is.
        """
    
        context = ssl.create_default_context()
        download_socket = socket(AF_INET, SOCK_STREAM)
        download_socket = context.wrap_socket(
            download_socket, server_hostname=get_work_response.host)
        
        port = 443
        download_socket.connect((gethostbyname(get_work_response.host), port))
        request = HTTPGetRequest(get_work_response.host, get_work_response.path)
        download_socket.send(request.serialize().encode())

        word_counts = dict()
        with download_socket.makefile('r') as f:
            while True:
                # Read a line from the socket
                line = f.readline()
                if len(line) == 0:
                    break
                words = line.split()
                for word in words:
                    if len(word) > 5:
                        word = word.lower()
                        word_counts[word] = word_counts.get(word, 0) + 1
        download_socket.close()
        sorted_words = dict(sorted(word_counts.items(),
                                   key=lambda item: item[1],
                                   reverse=True)[:20])
        print(sorted_words)
        return sorted_words
    
    def report_work(self, path: str, result: dict) -> WorkCompleteResponse|None:
        """
        Connects to the Coordinator and reports the results of a previously
        completed analysis of a play.
        """

        sock = self.connect()
        if not sock:
            return None
        sock.send(WorkCompleteRequest(path, result).serialize().encode())
        with sock.makefile('r') as response_file:
            response = Message.deserialize(response_file)

        sock.close()
        return response

    def keep_working_until_done(self):
        """
        Repeatedly asks for work from the Coordinator, performs the work, and
        reports the results. Continues until the Coordinator responds with no
        work or there's an error talking to the Coordinator.
        """
        

        while True:
            work = self.get_work()
            if not isinstance(work, GetWorkResponse) or work.host == '' or work.path == '':
                break
            result = self.do_work(work)
            if not self.report_work(work.path, result):
                break

    
if __name__ == '__main__':
    volunteer = Volunteer('localhost', 5791)
    volunteer.keep_working_until_done()
