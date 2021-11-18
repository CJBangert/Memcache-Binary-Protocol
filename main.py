
from io import UnsupportedOperation

def memcached_process(memcache, data):
    
    opcode = get_opcode(data)

    keylen = get_keylen(data)


    if(opcode == 0):

        key = get_key_get(data)
       
        value = memcache.getitem(key)

        return generate_get_response(value, keylen, data)

    elif(opcode == 1):


        print("key length: ", keylen  )

        key = get_key_set(data, keylen)

        value = get_value_set(data, keylen)

        memcache.setitem(key, value)

    else:

        raise UnsupportedOperation()


def generate_get_response(value, keylen):

    if(value is not None):

        magic = '0x81'
        opcode = '0x00'
        key_length = keylen
        extra_len = '0x00'
        data_type = '0x00'
        VBucket = '0x0000'
        return return_value


#gets the opcode from the byte string
def get_opcode(data):

    if(data[1] == 1):

        print("set")

        #return 1 to indicate set operation
        return 1

    elif(data[1] == 0):

        print("get")

        #return 0 to indicate get operation
        return 0

def get_key_get(data):

    #get key is bytes 24-end
    print(data[24:])
    return data[24:]

def get_key_set(data, keylen):

    #set key is bytes range(32, 32+length of key)
    key  = data[32:32+keylen]

    print(key)

    return key

def get_value_set(data, keylen):

    #set value is bytes range (32+length of key, end)

    value = data[32+keylen:]

    print(value)

    return value

def get_keylen(data):

    return data[3]