from backend.util.hex_to_binary import hex_to_binary

def test_hex_to_binary():
    original_representation = 45656
    hexidecimal_representation = hex(original_representation)[2:]
    binary_representation = hex_to_binary(hexidecimal_representation)

    assert int(binary_representation, 2) == original_representation