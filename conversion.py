def decimalToBinary(n):
    # converting decimal to binary
    # and removing the prefix(0b)
    return "{:032b}".format(x)

def binaryToDecimal(n):
    return int(n,2)

def twosCompliment(n):
    return -(
        -int(
            "0b" + n,
            2,
        )
        & (2**len(n)-1)
    )
