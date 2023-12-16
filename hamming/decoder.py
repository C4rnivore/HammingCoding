import math
from tables.char_to_binary import binary_chars
from .prettier import color

def decode_msg(message):
    msg = ''
    for message_block in message:
        msg += compare(message_block, recalculate_bits(message_block))
    print(f' Результат декодирования: {color.BLUE}{msg}{color.END} \n ')
        

def get_control_bits(message_block):
    pow = math.floor(math.log2(len(message_block)))
    control_bits_pos = [(2 ** i) - 1 for i in range(pow + 1)]
    return control_bits_pos


def recalculate_bits(message_block):
    control_bits_pos = get_control_bits(message_block)

    message = list(message_block)
    message = remove_initial_bits(message, control_bits_pos)

    for bit_pos in control_bits_pos:
        message.insert(bit_pos,'0')
    
    for bit_pos in control_bits_pos:
        message[bit_pos] = calculate_bit_value(message, bit_pos)

    return ''.join(message)

def calculate_bit_value(message, bit_pos:list):
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

def remove_initial_bits(message_block, bit_pos):
    result = []
    index = 0

    for bit in message_block:
        if index in bit_pos:
            index+=1
            continue
        else:
            result.append(bit)
            index+=1
    
    return result

def compare(initial_msg_block, recalculatd_message_block):
    initial_msg_block = list(initial_msg_block)
    recalculatd_message_block = list(recalculatd_message_block)
    control_bits_pos = get_control_bits(initial_msg_block)
    mistake_index = -1
    has_mistake = False

    for bit_pos in control_bits_pos:
        if initial_msg_block[bit_pos] == recalculatd_message_block[bit_pos]:
            continue
        else:
            has_mistake = True
            mistake_index += bit_pos + 1

    if has_mistake:
        print(f'При передаче фрагмента сообщения {color.RED}{initial_msg_block}{color.END} возникла ошибка в бите под индексом {mistake_index}')
        return decode_block(recalculatd_message_block, control_bits_pos, mistake_index)
        
    else:
        print(f'Фрагмент сообщения {color.GREEN}{initial_msg_block}{color.END} передан без ошибки')
        return decode_block(initial_msg_block, control_bits_pos)
        

def decode_block(message_block,control_bits_pos, mistake_index = -1):
    block_msg=''

    if mistake_index != -1:
        if message_block[mistake_index] == '0':
            message_block[mistake_index] = '1'
        else:
            message_block[mistake_index] = '0'

    message_block = remove_initial_bits(message_block, control_bits_pos)
    message_block = ''.join(message_block)
    chars_count = int(len(message_block) / 8)

    for i in range(0,chars_count ):
        char_binary = message_block[i*8 : (i + 1)*8]
        char = binary_chars[char_binary]
        block_msg+=char

    return block_msg
        


