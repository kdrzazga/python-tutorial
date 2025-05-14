# https://sio2.mimuw.edu.pl/c/oij14-1/p/hax/

def encode(caption):
    encoded = ""
    for i in range(len(caption)):
        origin = caption[i]
        encoded += code(origin)

    return encoded


def code(letter):
    d = {
        'a': 4,
        'e': 3,
        'i': 1,
        'o': 0,
        's': 5
    }

    return str(d[letter]) if letter in d.keys() else letter


test_values = ('haxor', 'rigcz', 'aeios')
for test_value in test_values:
    print(encode(test_value))
