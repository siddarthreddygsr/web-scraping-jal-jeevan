def encode_func(keyvalue):
    dtcode11 = ""
    for i in keyvalue:
        if int(i) == 9:
            dtcode11 += "%3A"
        else:
            dtcode11 += str(int(i)+1)
    dtcode11 += "1"
    return dtcode11