
from io import UnsupportedOperation
import struct
import six
import threading


'''
    B-> 1 byte
    H-> 2 bytes
    L-> 4 bytes
    Q-> 8 bytes
    '''

HEADER_STRUCT = '!BBHBBHLLQ'
HEADER_STRUCT_NOT_FOUND_OR_SET = '!BBHBBHLLQ'

def memcached_process(memcache, data):
    
    opcode = get_opcode(data)

    keylen = get_keylen(data)


    if(opcode == 0):

        key = get_key_get(data)
       
        value = memcache.getitem(key)

        return generate_get_response(value)

    elif(opcode == 1):


        print("key length: ", keylen , flush=True )

        key = get_key_set(data, keylen)

        value = get_value_set(data, keylen)

        memcache.setitem(key, value)

        return generate_set_response(key,value)

    else:

        raise UnsupportedOperation()




def generate_set_response(key,value):
    
    magic = 0x81 #'0x81'

    opcode = 0x01

    key_length = 0

    extra_len = 0

    data_type = 0

    status = 0

    total_body = 0

    opaque = 0

    CAS = 1

    format_str = HEADER_STRUCT_NOT_FOUND_OR_SET

    return_value = struct.pack(format_str , magic, opcode,key_length,extra_len,data_type,status,total_body,opaque,CAS)

    print("return: ", return_value, flush=True)

    return return_value



def generate_get_response(value):
    
    '''
    Byte/     0       |       1       |       2       |       3       |
        /              |               |               |               |
       |0 1 2 3 4 5 6 7|0 1 2 3 4 5 6 7|0 1 2 3 4 5 6 7|0 1 2 3 4 5 6 7|
       +---------------+---------------+---------------+---------------+
      0| 0x81          | 0x00          | 0x00          | 0x00          |
       +---------------+---------------+---------------+---------------+
      4| 0x04          | 0x00          | 0x00          | 0x00          |
       +---------------+---------------+---------------+---------------+
      8| 0x00          | 0x00          | 0x00          | 0x09          |
       +---------------+---------------+---------------+---------------+
     12| 0x00          | 0x00          | 0x00          | 0x00          |
       +---------------+---------------+---------------+---------------+
     16| 0x00          | 0x00          | 0x00          | 0x00          |
       +---------------+---------------+---------------+---------------+
     20| 0x00          | 0x00          | 0x00          | 0x01          |
       +---------------+---------------+---------------+---------------+
     24| 0xde          | 0xad          | 0xbe          | 0xef          |
       +---------------+---------------+---------------+---------------+
     28| 0x57 ('W')    | 0x6f ('o')    | 0x72 ('r)    | 0x6c ('l')    |
       +---------------+---------------+---------------+---------------+
     32| 0x64 ('d')    |
       +---------------+ '''

    magic = 0x81 #'0x81 -> response magic'
    
    opcode = 0x00 #get opcode
    
    key_length = 0

    data_type = 0 #'0x00 - raw bytes'
    
    opaque = 0 #'0x00000000'
    
    
    if(value is not None):

        #value found
        status =  0 #'0x0000'

        CAS = 1

        '''documented value for get 'extras' or flags' was 3735928559, '0xdeadbeef'. was causing client to try and decompresshad to find at what values that branch doesn't
         get evaluated (where flags & (1 << 3) == 0 . To go down correct code branch, the flag also had to be divisible by 4 (flags & 1 << 4) !=0. I had the code run and 
         just print a bunch of values that would work and I picked one)'''
        extra= 1765040  
        
        extra_len = 4 #'0x04'

        valbytes = str_to_bytes(value)
        
        total_body = len(valbytes) + extra_len 

        format_str = HEADER_STRUCT + ('L%ds'%(len(valbytes)))   
        
        return_value = struct.pack(format_str , magic, opcode,key_length,extra_len,data_type,status,total_body,opaque,CAS,extra,valbytes) 
                                                #!B   |  B   |    H     |      B  |     B   |  H   | L        | L    | Q |  L  | %ds'%(len(valbytes))    

    else:

        # not found 
        status = 1

        CAS = 0

        value = "not found"

        extra_len = 0

        valbytes = str_to_bytes(value)

        total_body = len(value) + extra_len 

        format_str = HEADER_STRUCT_NOT_FOUND_OR_SET + ('%ds'%(len(valbytes)))
        
        return_value = struct.pack(format_str , magic, opcode,key_length,extra_len,data_type,status,total_body,opaque,CAS,valbytes) 
                                                #!B     B       H           B       B           H       L          L    Q          
    print("return: ",return_value, flush=True)

    print(len(return_value), flush=True)

    return return_value


#gets the opcode from the byte string
def get_opcode(data):

    if(data[1] == 1):

        print("Operation: Set", flush=True)

        #return 1 to indicate set operation
        return 1

    elif(data[1] == 0):

        print("Operation: get", flush=True)

        #return 0 to indicate get operation
        return 0

def get_key_get(data):

    #get key is bytes 24-end
    print(data[24:])

    return data[24:]

def get_key_set(data, keylen):

    #set key is bytes range(32, 32+length of key)
    key  = data[32:32+keylen]

    print(key, flush=True)

    return key

def get_value_set(data, keylen):

    #set value is bytes range (32+length of key, end)

    value = data[32+keylen:]

    print(value, flush=True)

    return value

def get_keylen(data):

    return data[3]

#from python-binary-memcached
def str_to_bytes(value):
    """
    Simply convert a string type to bytes if the value is a string
    and is an instance of six.string_types but not of six.binary_type
    in python2 struct.pack("<Q") is both string_types and binary_type but
    in python3 struct.pack("<Q") is binary_type but not a string_types
    :param value:
    :param binary:
    :return:
    """
    if not isinstance(value, six.binary_type) and isinstance(value, six.string_types):
        return value.encode()
    return value