import random
from hamming.encoder import encode_msg
from hamming.decoder import decode_msg

LENGTH = 16

def encode(message=''):
    try:
        message = encode_msg(message, LENGTH)
        message = make_mistake(message)
        decode_msg(message)
    except:
        print('error')
    return

def make_mistake(message):
    result = []

    for message_block in message:
        a = random.random()
        if(a <= 0.5):
            result.append(message_block)
        else:  
            random_index = random.randrange(0, len(message_block))
            message_l = list(message_block)
            if message_l[random_index] == '0':
                message_l[random_index] = '1'
            else:
                message_l[random_index] = '0'

            result.append(''.join(message_l)) 

    return result

if __name__ == '__main__':
    message = 'Hello, world!'
    encode(message)
