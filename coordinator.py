from messages import *
import random
from socket import *

# This class is fully implemented for you and you should not need to make any
# modifications to it.
class WorkTracker:
    """
    A class that tracks the status of plays to download and analyze. This is
    used by the Coordinator server to assign work to Volunteers and to
    assimilate results from Volunteers.
    """

    def __init__(self):
        """
        Constructs a WorkTracker to analyze specific Shakespeare's plays.
        """

        self.play_download_host = "www.gutenberg.org"
        self.play_ids = []
        self.play_ids.append(1513)  # Romeo and Juliet
        self.play_ids.append(27761)  # Hamlet
        self.play_ids.append(23042)  # Tempest
        self.play_ids.append(1533)  # Macbeth
        self.play_ids.append(1531)  # Othello
        self.play_ids.append(1522)  # Julius Caesar
        self.play_ids.append(1526)  # Twelfth Night
        self.play_ids.append(1515)  # Merchant of Venice

        self.word_counts = dict()
        """
        A dictionary that maintains the aggregate word frequencies across the
        plays analyzed by Volunteers.
        key: word, value: count.
        """

        self.unstarted_paths = set()
        """
        Paths of plays that have not been assigned to any Volunteers yet.
        """
        for i in self.play_ids:
            self.unstarted_paths.add("/cache/epub/%s/pg%s.txt" % (i, i))

        self.started_paths = set()
        """
        Paths of plays that have been assigned to Volunteers but they haven't
        yet reported results for them yet.
        """

        self.finished_paths = set()
        """
        Paths of plays that have been analyzed by Volunteers and the reported
        results have been assimilated by the Coordinator.
        """

    def get_path_for_volunteer(self) -> str:
        """
        Returns the path to a play that a Volunteer looking for work should
        download from the webservice, analyze, and report results. If there is
        no work left, returns an empty path.
        """

        if len(self.unstarted_paths) > 0:
            # There are unstarted plays, so hand one of them out.
            path = random.choice(list(self.unstarted_paths))
            self.unstarted_paths.remove(path)
            self.started_paths.add(path)
        elif len(self.started_paths) > 0:
            print("There are no unstarted paths.")
            print("So handing out an already started (but not finished) path.")
            print("Just in case the other volunteer flakes.")
            path = random.choice(list(self.started_paths))
        else:
            # There's no work left.
            path = ""
        return path

    def process_result(self, path, word_counts: dict):
        """
        Processes the word-counts report from a Volunteer for the specified
        path's play by aggregating them into the overall word-counts across all
        analyzed plays.
        """

        if path in self.finished_paths:
            # This path has already been processed, so ignore it. Otherwise, it
            # would be processed multiple times and skew the results.
            return
        for [word, count] in word_counts.items():
            self.word_counts[word] = self.word_counts.get(word, 0) + int(count)
        self.started_paths.remove(path)
        self.finished_paths.add(path)

    def is_all_work_done(self) -> bool:
        """
        Return whether all the work is done.
        """

        return len(self.finished_paths) == len(self.play_ids)

    def get_word_counts_desc(self):
        """
        Returns the aggregate word-counts in descending order by count.
        """

        return dict(sorted(self.word_counts.items(),
                           key=lambda item: item[1], reverse=True))


class Coordinator:
    """
    A class that starts a Coordinator server, handles requests from Volunteers,
    and aggregates results reported by Volunteers.
    """

    def __init__(self):
        """
        Constructs a Coordinator that will manage the word-counts analysis of
        a set of Shakespeare's plays, relying on Volunteers to ask for and do
        work on each play.
        """

        self.work_tracker = WorkTracker()

        self.server_socket = socket(family=AF_INET, type=SOCK_STREAM)
        """
        Server socket that speaks TCP (transport) and IPv4 (network)
        """

    def start(self, port: int) -> int:
        """
        Starts the coordinator server on the specified port. If the specified
        port is 0 then picks an unused port. Returns the port that the server
        is listening on.
        """

        # Bind to a specific port
        self.server_socket.bind(('', port))

        # Listen for client knocking.
        backlog = 10
        self.server_socket.listen(backlog)

        self.server_socket.settimeout(.5)
        return self.server_socket.getsockname()[1]

    def accept_connections_until_all_work_done(self):
        """
        Allows Volunteers to repeatedly connect and execute the application
        layer protocol. When there's no work left to do then prints out the
        aggregated result and shuts down the server. This method blocks until
        there's no more work to do.
        """

        try:
            while True:
                connection_socket, addr = self.server_socket.accept()
                with connection_socket.makefile('rw') as file:
                    request = Message.deserialize(file)
                    if isinstance(request, GetWorkRequest):
                        if self.work_tracker.is_all_work_done():
                            resp = GetWorkResponse('', '')
                        else:
                            resp = GetWorkResponse(self.work_tracker.play_download_host, self.work_tracker.get_path_for_volunteer())
                    elif isinstance(request, WorkCompleteRequest):
                        self.work_tracker.process_result(request.path, request.word_counts)
                        resp = WorkCompleteResponse()
                    else:
                        continue
                    file.write(resp.serialize())

                connection_socket.close()
        except TimeoutError:
            pass

        self.server_socket.close()
        print(self.work_tracker.get_word_counts_desc())


if __name__ == '__main__':
    coordinator = Coordinator()
    port = coordinator.start(0)
    coordinator.accept_connections_until_all_work_done()
