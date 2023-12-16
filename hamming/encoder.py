from .prettier import color
from tables.char_to_binary import char_binaries
import math

CHARS_PER_MESSAGE = -1

def encode_msg(message, iwl=16):
    if(iwl % 8 != 0):
        print(f'Not walid argument {color.BOLD} iwl = {iwl} {color.END}  \n' )
        print(f'Argument iwl must be a multiple of 8 \n' )
        return 
    
    result = []
    
    CHARS_PER_MESSAGE = int(iwl / 8)

    message_blocks = split_by_blocks(message, CHARS_PER_MESSAGE)
    message_blocks = convert_to_binary(message_blocks)

    for message_block in message_blocks:
        result.append(insert_control_bits(message_block))

    print(f'\n Сообщение {color.BLUE}{message}{color.END} закодировано фрагментами: {color.BLUE}{result}{color.END}')

    return result


def split_by_blocks(message, char_per_message):
    return [message[i:i+char_per_message] for i in range(0, len(message), char_per_message)]

def convert_to_binary(message_blocks):
    binary = []

    for pair in message_blocks:
        binary_pair = ''
        for char in pair:
            binary_pair += char_binaries[char]
        binary.append(binary_pair)

    return binary

def insert_control_bits(message):
    pow = math.floor(math.log2(len(message)))
    control_bits_pos = [(2 ** i) - 1 for i in range(pow + 1)]
    message = list(message)
    
    for bit_pos in control_bits_pos:
        message.insert(bit_pos,'0')
    
    for bit_pos in control_bits_pos:
        message[bit_pos] = calculate_bit_value(message, bit_pos)

    return ''.join(message)
    
def calculate_bit_value(message, bit_pos):
    # 00010011010101001010
    # (0) 0 [0] 1 [0] 0 [0] 1 [1] 0 [1] 0 [1] 0 [1] 0 [0] 1 [0] 1 [0] //4 единицы => 0
    # 0 [(1)0] 10 [00] 11 [01] 01 [01] 00 [10] 10 // 3 единицы => 1
    # 0001[(0)011] 0101 [0100] 1010 // 3 единицы -> 1
    # ...

    ones_amount = 0
    message = message[bit_pos:]

    skip_distance, go_distance = bit_pos + 1, bit_pos + 1

    for bit in message:
        if skip_distance == 0:
            go_distance = bit_pos + 1
            skip_distance = bit_pos + 1

        if go_distance == 0:
            skip_distance -= 1
            continue
        else:
            if bit == '0':
                go_distance -= 1
                continue
            else:
                go_distance -= 1
                ones_amount += 1
            
    if ones_amount % 2 == 0:
        return '0'
    return '1'

