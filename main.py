from blessed import Terminal

term = Terminal()
buffer = " "
filename = ""
cur = 1
frame = 0
copy = ""


def hextostring(str):
    """Converts a hex number (i.e 6C for l) to string

    Args:
        str (str): Input String

    Returns:
        str: ASCII from Hex number
    """
    hex_values = str
    return "".join(
        [chr(int(hex_values[i : i + 2], 16)) for i in range(0, len(hex_values), 2)]
    )


def stringtohex(s):
    """Converts a string (i.e l for 6C) to hex

    Args:
        s (str): Input String

    Returns:
        str: Hex number
    """
    return "".join([format(ord(char), "02x") for char in s])


def inp(maxlen=100, hexval=False):
    """Simple Input Function for use with Blessed

    Args:
        maxlen (int, optional): Maximum Length the output can be. Defaults to 100.
        hexval (bool, optional): Is this input gonna be used for Hexadecimal characters?. Defaults to False.

    Returns:
        str: User's input
    """
    print(term.clear())
    val = ""
    k = term.inkey(0)
    while 1:
        print(term.clear(), end="")
        print(":" + val)
        k = term.inkey()
        if k.name == "KEY_BACKSPACE":
            val = val[:-1]
        if k in "0123456789ABCDEFabcdef" and hexval:
            val += k.upper()
        if (
            k in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890._-"
            and not hexval
        ):
            val += k
        if k.name == "KEY_ENTER":
            break
    print(term.clear(), end="")
    return val


def ins(buffer):
    """Add character to buffer

    Args:
        buffer (str): Text buffer

    Returns:
        str: new buffer
    """
    global cur
    buffer = list(buffer)
    buffer.extend([" "] * (cur - len(buffer)))
    buffer[cur - 1] = hextostring(inp(2, True))
    cur += 1
    return "".join(buffer)


def save():
    """Saves to file
    """
    global filename, buffer
    if filename == "":
        filename = inp()
    with open(filename, "w") as f:
        f.write(buffer)


with term.cbreak(), term.fullscreen(), term.hidden_cursor():
    print(term.clear())
    key = term.inkey(0)
    buffer = ""
    while 1:
        print(term.clear(), end="")
        if key.name == "KEY_ENTER":
            buffer = ins(buffer)
        if key.name == "KEY_LEFT":
            cur -= 1
        if key.name == "KEY_RIGHT":
            cur += 1
        if key.name == "KEY_UP":
            buffer = list(buffer)
            buffer.extend([" "] * (cur - len(buffer)))
            char = stringtohex(buffer[cur - 1])
            char = int(char, 16) + 1
            char = char % 0xFF
            buffer[cur - 1] = chr(char)
            buffer = "".join(buffer)
        if key.name == "KEY_DOWN":
            buffer = list(buffer)
            buffer.extend([" "] * (cur - len(buffer)))
            char = stringtohex(buffer[cur - 1])
            char = int(char, 16) - 1
            char = char % 0xFF
            buffer[cur - 1] = chr(char)
            buffer = "".join(buffer)
        if key.name == "KEY_BACKSPACE":
            buffer = list(buffer)
            buffer.extend([" "] * (cur - len(buffer)))
            buffer[cur - 1] = ""
            buffer = "".join(buffer)
        if key == "s":
            save()
        if key == "c":
            copy = buffer[cur - 1]
        if key == "v":
            buffer = list(buffer)
            buffer.extend([" "] * (cur - len(buffer)))
            buffer[cur - 1] = copy
            buffer = "".join(buffer)
        if key == "q":
            break
        # cur = cur % len(buffer+" ") + 1

        print(buffer)
        print(term.move_xy(cur - 1, 1) + "^")

        key = term.inkey(1)
        frame += 1
