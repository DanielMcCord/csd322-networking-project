"""Tests for messages.py."""

import unittest

from messages import *


class TestMessage(unittest.TestCase):

    def test_invalid_deserialize(self):
        try:
            Message.deserialize(StringIO("bogus msg"))
            self.fail("Expected ValueError")
        except ValueError:
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
        expected_serialized = ("GET some-path HTTP/1.1\r\n"
                               "Host: some-host\r\n"
                               "\r\n")
        self.assertEqual(serialized, expected_serialized)

        deserialized = Message.deserialize(StringIO(serialized))
        self.assertIsInstance(deserialized, HTTPGetRequest)
        self.assertEqual(deserialized.host, "some-host")
        self.assertEqual(deserialized.path, "some-path")


class TestGetWorkRequest(unittest.TestCase):

    def test_serialize_deserialize(self):
        request = GetWorkRequest()

        serialized = request.serialize()
        expected_serialized = ("ReqW\r\n"
                               "\r\n")
        self.assertEqual(serialized, expected_serialized)

        deserialized = Message.deserialize(StringIO(serialized))
        self.assertIsInstance(deserialized, GetWorkRequest)


class TestGetWorkResponse(unittest.TestCase):

    def test_serialize_deserialize(self):
        request = GetWorkResponse("some-host", "some-path")

        serialized = request.serialize()
        expected_serialized = ("AsgW\r\n"
                               "Host: some-host\r\n"
                               "Path: some-path\r\n"
                               "\r\n")
        self.assertEqual(serialized, expected_serialized)

        deserialized = Message.deserialize(StringIO(serialized))
        self.assertIsInstance(deserialized, GetWorkResponse)
        self.assertEqual(deserialized.host, "some-host")
        self.assertEqual(deserialized.path, "some-path")

    def test_serialize_deserialize_no_work_left(self):
        request = GetWorkResponse("", "")

        serialized = request.serialize()
        expected_serialized = ("AsgW\r\n"
                               "Host: \r\n"
                               "Path: \r\n"
                               "\r\n")
        self.assertEqual(serialized, expected_serialized)

        deserialized = Message.deserialize(StringIO(serialized))
        self.assertIsInstance(deserialized, GetWorkResponse)
        self.assertEqual(deserialized.host, "")
        self.assertEqual(deserialized.path, "")


class TestWorkCompleteRequest(unittest.TestCase):

    def test_serialize_deserialize(self):
        request = WorkCompleteRequest("path-to-play",
                                      {"romeo": 16, "juliet": 18, "rose": 7})

        serialized = request.serialize()
        expected_serialized = ("SubW\r\n"
                               "Path: path-to-play\r\n"
                               "Word-Counts:\r\n"
                               "romeo 16\r\n"
                               "juliet 18\r\n"
                               "rose 7\r\n"
                               "\r\n")
        self.assertEqual(serialized, expected_serialized)

        deserialized = Message.deserialize(StringIO(serialized))
        self.assertIsInstance(deserialized, WorkCompleteRequest)
        self.assertEqual(deserialized.path, "path-to-play")
        self.assertEqual(deserialized.word_counts, {"romeo": 16, "juliet": 18, "rose": 7})


class TestWorkCompleteResponse(unittest.TestCase):

    def test_serialize_deserialize(self):
        request = WorkCompleteResponse()

        serialized = request.serialize()
        expected_serialized = ("AckW\r\n"
                               "\r\n")
        self.assertEqual(serialized, expected_serialized)

        deserialized = Message.deserialize(StringIO(serialized))
        self.assertIsInstance(deserialized, WorkCompleteResponse)


if __name__ == '__main__':
    unittest.main()
