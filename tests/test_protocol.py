"""
Unit tests for protocol layer (Message, MessageCodec, MessageTypes).
"""
import unittest
import json
from server.protocol import Message, MessageType, MessageCodec


class TestMessage(unittest.TestCase):
    """Test suite for Message class"""

    def test_message_creation(self):
        """Test basic message creation"""
        msg = Message(type=MessageType.SYSTEM, data={'text': 'Hello'})

        self.assertEqual(msg.type, MessageType.SYSTEM)
        self.assertEqual(msg.data['text'], 'Hello')
        self.assertIsNotNone(msg.timestamp)
        self.assertIsNone(msg.session_id)

    def test_message_with_session(self):
        """Test message creation with session ID"""
        msg = Message(
            type=MessageType.COMMAND,
            data={'text': 'look'},
            session_id='test-session-123'
        )

        self.assertEqual(msg.session_id, 'test-session-123')

    def test_message_to_dict(self):
        """Test message serialization to dict"""
        msg = Message(
            type=MessageType.AUTH_SUCCESS,
            data={'player_id': '12345'},
            session_id='session-1'
        )

        msg_dict = msg.to_dict()

        self.assertEqual(msg_dict['type'], 'AUTH_SUCCESS')
        self.assertEqual(msg_dict['data']['player_id'], '12345')
        self.assertEqual(msg_dict['session_id'], 'session-1')
        self.assertIn('timestamp', msg_dict)

    def test_message_from_dict(self):
        """Test message deserialization from dict"""
        msg_dict = {
            'type': 'ROOM_DESCRIPTION',
            'data': {'text': 'A dark room'},
            'timestamp': 1234567890.0,
            'session_id': 'sess-123',
            'metadata': {'key': 'value'}
        }

        msg = Message.from_dict(msg_dict)

        self.assertEqual(msg.type, MessageType.ROOM_DESCRIPTION)
        self.assertEqual(msg.data['text'], 'A dark room')
        self.assertEqual(msg.timestamp, 1234567890.0)
        self.assertEqual(msg.session_id, 'sess-123')
        self.assertEqual(msg.metadata['key'], 'value')

    def test_message_get_method(self):
        """Test convenience get method"""
        msg = Message(
            type=MessageType.COMMAND,
            data={'text': 'north', 'direction': 'n'}
        )

        self.assertEqual(msg.get('text'), 'north')
        self.assertEqual(msg.get('direction'), 'n')
        self.assertIsNone(msg.get('missing'))
        self.assertEqual(msg.get('missing', 'default'), 'default')

    def test_message_set_method(self):
        """Test convenience set method"""
        msg = Message(type=MessageType.SYSTEM, data={})

        msg.set('text', 'Updated')
        msg.set('count', 42)

        self.assertEqual(msg.data['text'], 'Updated')
        self.assertEqual(msg.data['count'], 42)


class TestMessageCodec(unittest.TestCase):
    """Test suite for MessageCodec class"""

    def test_encode_json(self):
        """Test JSON encoding"""
        msg = Message(
            type=MessageType.COMMAND,
            data={'text': 'look'}
        )

        encoded = MessageCodec.encode_json(msg)

        self.assertIsInstance(encoded, bytes)
        self.assertTrue(encoded.endswith(b'\n'))

        # Should be valid JSON
        decoded_dict = json.loads(encoded.decode('utf-8'))
        self.assertEqual(decoded_dict['type'], 'COMMAND')
        self.assertEqual(decoded_dict['data']['text'], 'look')

    def test_decode_json(self):
        """Test JSON decoding"""
        json_data = json.dumps({
            'type': 'SYSTEM',
            'data': {'text': 'Welcome'},
            'timestamp': 1234567890.0
        }).encode('utf-8')

        msg = MessageCodec.decode_json(json_data)

        self.assertEqual(msg.type, MessageType.SYSTEM)
        self.assertEqual(msg.data['text'], 'Welcome')
        self.assertEqual(msg.timestamp, 1234567890.0)

    def test_encode_text_room_description(self):
        """Test text encoding for room description"""
        msg = Message(
            type=MessageType.ROOM_DESCRIPTION,
            data={'text': 'A dark forest'}
        )

        encoded = MessageCodec.encode_text(msg)

        self.assertEqual(encoded, b'A dark forest\r\n')

    def test_encode_text_prompt(self):
        """Test text encoding for prompt"""
        msg = Message(
            type=MessageType.PROMPT,
            data={'text': '<100hp 50m>'}
        )

        encoded = MessageCodec.encode_text(msg)

        self.assertEqual(encoded, b'<100hp 50m>\r\n')

    def test_encode_text_error(self):
        """Test text encoding for error"""
        msg = Message(
            type=MessageType.ERROR,
            data={'text': 'Invalid command'}
        )

        encoded = MessageCodec.encode_text(msg)

        self.assertEqual(encoded, b'ERROR: Invalid command\r\n')

    def test_encode_text_adds_crlf(self):
        """Test that text encoding always adds CRLF"""
        msg = Message(
            type=MessageType.SYSTEM,
            data={'text': 'No newline'}
        )

        encoded = MessageCodec.encode_text(msg)

        self.assertTrue(encoded.endswith(b'\r\n'))

    def test_decode_text_empty(self):
        """Test decoding empty text"""
        msg = MessageCodec.decode_text(b'')

        self.assertEqual(msg.type, MessageType.INPUT)
        self.assertEqual(msg.data['text'], '')

    def test_decode_text_command(self):
        """Test decoding regular command"""
        msg = MessageCodec.decode_text(b'look\r\n')

        self.assertEqual(msg.type, MessageType.COMMAND)
        self.assertEqual(msg.data['text'], 'look')

    def test_decode_text_json_payload(self):
        """Test decoding JSON message"""
        json_msg = {'type': 'SYSTEM', 'data': {'text': 'Hello'}}
        data = json.dumps(json_msg).encode('utf-8')

        msg = MessageCodec.decode_json(data)

        self.assertEqual(msg.type, MessageType.SYSTEM)
        self.assertEqual(msg.data['text'], 'Hello')

    def test_decode_text_logon_payload(self):
        """Test decoding logon command with JSON payload"""
        payload = {
            'accountId': 'acc123',
            'characterId': 'char456',
            'characterName': 'TestChar'
        }
        data = f'logon {json.dumps(payload)}\r\n'.encode('utf-8')

        msg = MessageCodec.decode_text(data)

        self.assertEqual(msg.type, MessageType.CHAR_LOGON)
        self.assertEqual(msg.data['accountId'], 'acc123')
        self.assertEqual(msg.data['characterId'], 'char456')
        self.assertEqual(msg.data['characterName'], 'TestChar')

    def test_is_json_true(self):
        """Test is_json detection for valid JSON"""
        json_data = b'{"key": "value"}'
        self.assertTrue(MessageCodec.is_json(json_data))

        json_data_with_whitespace = b'  {"key": "value"}  '
        self.assertTrue(MessageCodec.is_json(json_data_with_whitespace))

    def test_is_json_false(self):
        """Test is_json detection for non-JSON"""
        self.assertFalse(MessageCodec.is_json(b'look'))
        self.assertFalse(MessageCodec.is_json(b'north'))
        self.assertFalse(MessageCodec.is_json(b'{"incomplete"'))

    def test_roundtrip_json(self):
        """Test encoding then decoding JSON"""
        original = Message(
            type=MessageType.COMMAND,
            data={'text': 'inventory', 'count': 5},
            session_id='test-session'
        )

        encoded = MessageCodec.encode_json(original)
        decoded = MessageCodec.decode_json(encoded)

        self.assertEqual(decoded.type, original.type)
        self.assertEqual(decoded.data, original.data)
        self.assertEqual(decoded.session_id, original.session_id)


class TestMessageTypes(unittest.TestCase):
    """Test suite for MessageType enum"""

    def test_message_types_exist(self):
        """Test that expected message types exist"""
        expected_types = [
            'SYSTEM', 'ERROR', 'AUTH_REQUEST', 'AUTH_RESPONSE',
            'AUTH_SUCCESS', 'AUTH_FAILURE', 'AUTH_PAYLOAD', 'AUTH_VALIDATE',
            'CHAR_LIST', 'CHAR_SELECT', 'CHAR_SELECTED', 'CHAR_LOGON',
            'ROOM_DESCRIPTION', 'PROMPT', 'COMMAND', 'SAY', 'TELL',
            'WELCOME', 'DISCONNECT'
        ]

        for type_name in expected_types:
            self.assertTrue(
                hasattr(MessageType, type_name),
                f"MessageType.{type_name} should exist"
            )

    def test_message_type_values_unique(self):
        """Test that all message type values are unique"""
        values = [mt.value for mt in MessageType]
        self.assertEqual(len(values), len(set(values)))

    def test_message_type_by_name(self):
        """Test accessing message types by name"""
        system_type = MessageType['SYSTEM']
        self.assertEqual(system_type, MessageType.SYSTEM)

        command_type = MessageType['COMMAND']
        self.assertEqual(command_type, MessageType.COMMAND)


class TestMessageCodecEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""

    def test_decode_malformed_json(self):
        """Test decoding malformed JSON raises exception"""
        malformed = b'{"invalid": json}'

        with self.assertRaises(json.JSONDecodeError):
            MessageCodec.decode_json(malformed)

    def test_decode_json_missing_type(self):
        """Test decoding JSON without type field"""
        incomplete = json.dumps({'data': {'text': 'test'}}).encode('utf-8')

        with self.assertRaises(KeyError):
            MessageCodec.decode_json(incomplete)

    def test_encode_text_with_no_text_field(self):
        """Test encoding message with no text field"""
        msg = Message(
            type=MessageType.SYSTEM,
            data={'count': 5}  # No 'text' field
        )

        encoded = MessageCodec.encode_text(msg)

        # Should encode the data dict as string
        self.assertIsInstance(encoded, bytes)
        self.assertTrue(encoded.endswith(b'\r\n'))

    def test_decode_text_unicode(self):
        """Test decoding text with unicode characters"""
        unicode_text = 'Hello 世界\r\n'.encode('utf-8')

        msg = MessageCodec.decode_text(unicode_text)

        self.assertEqual(msg.data['text'], 'Hello 世界')


if __name__ == '__main__':
    unittest.main()
