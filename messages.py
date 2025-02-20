"""
Application layer messages for the Shakespear word-frequency distributed app.
Defines all relevant message types for the application.
For each message type defines its serialization into a human-readable ASCII
format that can be sent over the network.
Also defines the deserialization when receiving each message type from the
network.
"""

from io import *

class Message():
    """
    Base class for every app message type.
    """

    def serialize(self) -> str:
        """
        Returns a string corresponding to the human-readable ASCII message that
        can be sent over the network.
        The default base implementation intentionally raises an exception to
        ensure that each concrete message type implements this method.
        """

        raise NotImplementedError

class HTTPGetRequest(Message):
    """
    Message used by a Volunteer to request the text of a particular play from
    a web-service hosting Shakespeare's plays.
    This is fully defined for you as an example.
    """

    def __init__(self, host: str, path: str):
        """
        Creates an HTTPGetRequest for the specified host and path.
        """

        super().__init__()
        self.host = host
        self.path = path

    # Overrides super().serialize()
    def serialize(self) -> str:
        result = "GET %s HTTP/1.1\r\n" % (self.path)
        result += "Host: %s\r\n" % (self.host)
        result += "\r\n"
        return result 
    
    def deserialize(msg: TextIOBase) -> Message:
        """
        Parses the specified msg and returns an HTTPGetRequest (or raises a 
        ValueException if the msg is not a valid serialized HTTPGetRequest).
        This is a class method i.e. associated with the class rather than
        instances of the class. 
        """

        line = msg.readline()
        if line.startswith("GET "):
            [_, path, _] = line.split()
            line = msg.readline()
            [name, value] = line.split()
            if name == "Host:":
                return HTTPGetRequest(value, path)
        raise ValueError

class GetWorkRequest(Message):
    """
    Message sent by a Volunteer to the Coordinator to ask for work.
    """

    # TODO: override serialize().
    
    def deserialize(msg: TextIOBase) -> Message:
        """
        Parses the specified msg and returns a a GetWorkRequest (or raises a 
        ValueException if the msg is not a valid serialized GetWorkRequest).
        """

        # TODO: implement this.
        raise NotImplementedError

class GetWorkResponse(Message):
    """
    Message sent by the Coordinator to a Volunteer in response to the
    Volunteer's GetWorkRequest.
    """

    def __init__(self, host: str, path: str):
        """
        Constructs a response identifying a Shakespeare play (via the path) to
        download from a specified web-service (via the host). If either the path
        or the host is unspecified, then the response indicates that there is
        no work left to do.
        """
        self.host = host
        self.path = path


    # TODO: override serialize().
    
    def deserialize(msg: TextIOBase) -> Message:
        """
        Parses the specified msg and returns a a GetWorkResponse (or raises a 
        ValueException if the msg is not a valid serialized GetWorkResponse).
        """

        # TODO: implement this.
        raise NotImplementedError
    
class WorkCompleteRequest(Message):
    """
    Message sent by a Volunteer to the Coordinator to inform the Coordinator
    about the word-frequency data for a Shakespeare play that was previously
    assigned to the Volunteer in response to a GetWorkRequest.
    """

    def __init__(self, path: str, word_counts: dict):
        """
        Constructs a WorkCompleteRequest reporting the word-frequency result
        (dictionary with word as key and count as value) for the specified
        Shakespeare play (indentified by the path).
        """
        
        self.path = path
        self.word_counts = word_counts

    # TODO: override serialize().
    
    def deserialize(msg: TextIOBase) -> Message:
        """
        Parses the specified msg and returns a a WorkCompleteRequest (or raises a 
        ValueException if the msg is not a valid serialized WorkCompleteRequest).
        """

        # TODO: implement this.
        raise NotImplementedError
    
class WorkCompleteResponse(Message):
    """
    Message sent by the Coordinator to a Volunteer in response to a
    WorkCompleteRequest.
    """

    # TODO: override serialize().
    
    def deserialize(msg: TextIOBase) -> Message:
        """
        Parses the specified msg and returns a a WorkCompleteResponse (or
        raises a ValueException if the msg is not a valid serialized
        WorkCompleteResponse).
        """
        
        # TODO: implement this.
        raise NotImplementedError