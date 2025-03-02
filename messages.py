"""
Application layer messages for the Shakespeare word-frequency distributed app.
Defines all relevant message types for the application.
For each message type defines its serialization into a human-readable ASCII
format that can be sent over the network.
Also defines the deserialization when receiving each message type from the
network.
"""
from functools import cache
from io import *
from typing import Final
from abc import abstractmethod

ENDL: Final[str] = "\r\n"
"""
Line terminator.
"""


class Message:
    """
    Base class for every app message type.
    """

    @staticmethod
    @cache
    def prefixes() -> dict:
        """
        Returns a mapping of serialized message prefix strings to their corresponding classes.
        """

        return {
            "GET ": HTTPGetRequest,
            "ReqW": GetWorkRequest,
            "AsgW": GetWorkResponse,
            "SubW": WorkCompleteRequest,
            "AckW": WorkCompleteResponse
        }

    @abstractmethod
    def serialize(self) -> str:
        """
        Returns a string corresponding to the human-readable ASCII message that
        can be sent over the network.
        """

    @classmethod
    def deserialize(cls, msg: TextIOBase):
        """
        Parses the specified msg and returns its deserialized Message object (or
        raises a ValueError if the msg is not a valid serialization).
        """

        firstline = msg.readline()

        for prefix, subclass in cls.prefixes().items():
            if firstline.startswith(prefix):
                return subclass.parse(firstline, msg)
        raise ValueError(f"No recognized prefix found")

    @staticmethod
    @abstractmethod
    def parse(firstline: str, rest: TextIOBase):
        """
        Parses the specified firstline and rest (of message) as an instance of a
        specific subclass of Message. Returns the resulting Message object, or
        raises a ValueError on parsing failure.
        """


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

    # Override
    def serialize(self) -> str:
        return (f"GET {self.path} HTTP/1.1{ENDL}"
                f"Host: {self.host}{ENDL}"
                f"{ENDL}")

    @staticmethod
    def parse(firstline: str, rest: TextIOBase) -> Message:
        """
        Parses the specified firstline and rest (of message) and returns an
        HTTPGetRequest (or raises a ValueError if the msg is not a valid
        serialized HTTPGetRequest).
        """

        if not firstline.startswith("GET "): raise ValueError("Bad prefix")
        split = firstline.split()
        if len(split) != 3: raise ValueError("Incorrect number of elements")
        [_, path, _] = split
        split = rest.readline().split()
        if len(split) != 2: raise ValueError("Incorrect number of elements")
        [name, value] = split
        if not name == "Host:": raise ValueError("Unexpected field")
        return HTTPGetRequest(value, path)


class GetWorkRequest(Message):
    """
    Message sent by a Volunteer to the Coordinator to ask for work.
    """

    # Override
    def serialize(self) -> str:
        return (f"ReqW{ENDL}"
                f"{ENDL}")

    @staticmethod
    def parse(firstline: str, rest: TextIOBase) -> Message:
        """
        Parses the specified firstline and rest (of message) and returns a
        GetWorkRequest (or raises a ValueError if the msg is not a valid
        serialized GetWorkRequest).
        """

        if not firstline.startswith("ReqW"): raise ValueError("Bad prefix")
        return GetWorkRequest()


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

    # Override
    def serialize(self) -> str:
        return (f"AsgW{ENDL}"
                f"Host: {self.host}{ENDL}"
                f"Path: {self.path}{ENDL}"
                f"{ENDL}")

    @staticmethod
    def parse(firstline: str, rest: TextIOBase) -> Message:
        """
        Parses the specified firstline and rest (of message) and returns a
        GetWorkResponse (or raises a ValueError if the msg is not a valid
        serialized GetWorkResponse).
        """

        if not firstline.startswith("AsgW"): raise ValueError("Bad prefix")

        args = []
        for expected_name in ("Host:", "Path:"):
            split = rest.readline().split()
            if not split: raise ValueError("Incorrect number of elements")
            name, value = split[0], split[1] if len(split) > 1 else ""
            if name != expected_name: raise ValueError("Unexpected field")
            args.append(value)
        return GetWorkResponse(*args)


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
        Shakespeare play (identified by the path).
        """

        self.path = path
        self.word_counts = word_counts

    # Override
    def serialize(self) -> str:
        return (f"SubW{ENDL}"
                f"Path: {self.path}{ENDL}"
                f"Word-Counts:{ENDL}" +
                "".join(f"{word} {count}{ENDL}" for word, count in self.word_counts.items()) +
                f"{ENDL}")

    @staticmethod
    def parse(firstline: str, rest: TextIOBase) -> Message:
        """
        Parses the specified firstline and rest (of message) and returns a
        WorkCompleteRequest (or raises a ValueError if the msg is not a
        valid serialized WorkCompleteRequest).
        """

        if not firstline.startswith("SubW"): raise ValueError("Bad prefix")

        split = rest.readline().split()
        if len(split) != 2: raise ValueError("Incorrect number of elements")
        name, path = split[0], split[1]
        if not name == "Path:": raise ValueError("Unexpected field")

        split = rest.readline().split()
        if len(split) != 1: raise ValueError("Incorrect number of elements")
        name = split[0]
        if name != "Word-Counts:": raise ValueError("Unexpected field")

        word_counts = {}
        while len(split := rest.readline().split()) > 0:
            if len(split) != 2: raise ValueError("Incorrect number of elements")
            word_counts[split[0]] = int(split[1])
        return WorkCompleteRequest(path, word_counts)


class WorkCompleteResponse(Message):
    """
    Message sent by the Coordinator to a Volunteer in response to a
    WorkCompleteRequest.
    """

    # Override
    def serialize(self) -> str:
        return (f"AckW{ENDL}"
                f"{ENDL}")

    @staticmethod
    def parse(firstline: str, rest: TextIOBase) -> Message:
        """
        Parses the specified firstline and rest (of message) and returns a
        WorkCompleteResponse (or raises a ValueError if the msg is not a
        valid serialized WorkCompleteResponse).
        """

        if not firstline.startswith("AckW"): raise ValueError("Bad prefix")
        return WorkCompleteResponse()
