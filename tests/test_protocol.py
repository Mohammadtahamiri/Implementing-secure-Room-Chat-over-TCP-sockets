from client.protocol import encode_message, decode_message


def test_encode_message():
    message = "Hello"
    encoded = encode_message(message)

    assert isinstance(encoded, bytes)
    assert encoded == b"Hello"


def test_decode_message():
    data = b"Hello"
    decoded = decode_message(data)

    assert isinstance(decoded, str)
    assert decoded == "Hello"


def test_encode_decode_message():
    message = "Secure Chat"
    encoded = encode_message(message)
    decoded = decode_message(encoded)

    assert decoded == message