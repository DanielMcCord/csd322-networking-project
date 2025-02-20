"""Tests for messages.py."""

from io import *
from messages import *
import unittest

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

        deserialized = HTTPGetRequest.deserialize(StringIO(serialized))
        self.assertEqual(deserialized.host, "some-host")
        self.assertEqual(deserialized.path, "some-path")
    
    def test_invalid_deserialize(self):
        """
        Tests that an invalid message on the wire raises an exception when
        deserialized.
        """
        
        try:
           deserialized = HTTPGetRequest.deserialize(StringIO("bogus msg"))
           self.fail("Expected ValueError") 
        except(ValueError):
            pass

class TestGetWorkRequest(unittest.TestCase):

    def test_serialize_deserialize(self):
        request = GetWorkRequest()

        serialized = request.serialize()
        # TODO: validate

        deserialized = GetWorkRequest.deserialize(StringIO(serialized))
        # TODO: validate
    
    def test_invalid_deserialize(self):
        try:
           deserialized = GetWorkRequest.deserialize(StringIO("bogus msg"))
           self.fail("Expected ValueError") 
        except(ValueError):
            pass

class TestGetWorkResponse(unittest.TestCase):

    def test_serialize_deserialize(self):
        request = GetWorkResponse("some-host", "some-path")

        serialized = request.serialize()
        # TODO: validate

        deserialized = GetWorkResponse.deserialize(StringIO(serialized))
        # TODO: validate

    # TODO: also validate the case of no work left
    
    def test_invalid_deserialize(self):
        try:
           deserialized = GetWorkResponse.deserialize(StringIO("bogus msg"))
           self.fail("Expected ValueError") 
        except(ValueError):
            pass

class TestWorkCompleteRequest(unittest.TestCase):

    def test_serialize_deserialize(self):
        request = WorkCompleteRequest("path-to-play",
                                      {"romeo": 16, "juliet": 18, "rose": 7})

        serialized = request.serialize()
        # TODO: validate

        deserialized = WorkCompleteRequest.deserialize(StringIO(serialized))
        # TODO: validate
    
    def test_invalid_deserialize(self):
        try:
           deserialized = WorkCompleteRequest.deserialize(StringIO("bogus msg"))
           self.fail("Expected ValueError") 
        except(ValueError):
            pass

class TestWorkCompleteResponse(unittest.TestCase):

    def test_serialize_deserialize(self):
        request = WorkCompleteResponse()

        serialized = request.serialize()
        # TODO: validate

        deserialized = WorkCompleteResponse.deserialize(StringIO(serialized))
        # TODO: validate
    
    def test_invalid_deserialize(self):
        try:
           deserialized = WorkCompleteResponse.deserialize(StringIO("bogus msg"))
           self.fail("Expected ValueError") 
        except(ValueError):
            pass

if __name__ == '__main__':
    unittest.main()