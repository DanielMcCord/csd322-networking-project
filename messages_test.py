"""Tests for messages.py."""

from io import *
from messages import *
import unittest

class TestMessage(unittest.TestCase):

    def test_invalid_deserialize(self):
        try:
           deserialized = Message.deserialize(StringIO("bogus msg"))
           self.fail("Expected ValueError") 
        except(ValueError):
            pass

class TestHTTPGetRequest(unittest.TestCase):

    def test_serialize_deserialize(self):
        """
        Tests that a message object is serialized and deserialized as expected,
        and that serialize followed by deserialize (round-tripping) returns an
        equal object.
        """

        request = HTTPGetRequest("some-host", "some-path")

        serialized = request.serialize()
        expected_serialized = "GET some-path HTTP/1.1\r\n"
        expected_serialized += "Host: some-host\r\n"
        expected_serialized += "\r\n"
        self.assertEqual(serialized, expected_serialized)

        deserialized = Message.deserialize(StringIO(serialized))
        self.assertIsInstance(deserialized, HTTPGetRequest)
        self.assertEqual(deserialized.host, "some-host")
        self.assertEqual(deserialized.path, "some-path")

class TestGetWorkRequest(unittest.TestCase):

    def test_serialize_deserialize(self):
        request = GetWorkRequest()

        serialized = request.serialize()
        if serialized != "REQWORK":
            self.fail()

        deserialized = GetWorkRequest.deserialize(StringIO(serialized))
        self.assertIsInstance(deserialized, GetWorkRequest)
        # TODO: validate

class TestGetWorkResponse(unittest.TestCase):

    def test_serialize_deserialize(self):
        request = GetWorkResponse("some-host", "some-path")

        serialized = request.serialize()
        # TODO: validate

        deserialized = GetWorkResponse.deserialize(StringIO(serialized))
        self.assertIsInstance(deserialized, GetWorkResponse)
        # TODO: validate

    # TODO: also validate the case of no work left

class TestWorkCompleteRequest(unittest.TestCase):

    def test_serialize_deserialize(self):
        request = WorkCompleteRequest("path-to-play",
                                      {"romeo": 16, "juliet": 18, "rose": 7})

        serialized = request.serialize()
        # TODO: validate

        deserialized = WorkCompleteRequest.deserialize(StringIO(serialized))
        self.assertIsInstance(deserialized, WorkCompleteRequest)
        # TODO: validate

class TestWorkCompleteResponse(unittest.TestCase):

    def test_serialize_deserialize(self):
        request = WorkCompleteResponse()

        serialized = request.serialize()
        # TODO: validate

        deserialized = WorkCompleteResponse.deserialize(StringIO(serialized))
        self.assertIsInstance(deserialized, WorkCompleteResponse)
        # TODO: validate

if __name__ == '__main__':
    unittest.main()