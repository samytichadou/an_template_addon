import base64 


def enc(clear):
    sample_string_bytes = clear.encode("ascii") 
    
    base64_bytes = base64.b64encode(sample_string_bytes) 
    base64_string = base64_bytes.decode("ascii")

    return base64_string


def dec(encoded):
    base64_bytes = encoded.encode("ascii")
    
    sample_string_bytes = base64.b64decode(base64_bytes)
    sample_string = sample_string_bytes.decode("ascii")

    return sample_string

print(enc("animationnodestemplates"))