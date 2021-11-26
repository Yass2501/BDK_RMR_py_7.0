
def hexToBin(x_hex):
    x_bin = ''
    if(x_hex == '0'):
        x_bin = '0000'
    elif(x_hex == '1'):
        x_bin = '0001'
    elif(x_hex == '2'):
        x_bin = '0010'
    elif(x_hex == '3'):
        x_bin = '0011'
    elif(x_hex == '4'):
        x_bin = '0100'
    elif(x_hex == '5'):
        x_bin = '0101'
    elif(x_hex == '6'):
        x_bin = '0110'
    elif(x_hex == '7'):
        x_bin = '0111'
    elif(x_hex == '8'):
        x_bin = '1000'
    elif(x_hex == '9'):
        x_bin = '1001'
    elif(x_hex == 'A' or x_hex == 'a'):
        x_bin = '1010'
    elif(x_hex == 'B' or x_hex == 'b'):
        x_bin = '1011'
    elif(x_hex == 'C' or x_hex == 'c'):
        x_bin = '1100'
    elif(x_hex == 'D' or x_hex == 'd'):
        x_bin = '1101'
    elif(x_hex == 'E' or x_hex == 'e'):
        x_bin = '1110'
    elif(x_hex == 'F' or x_hex == 'f'):
        x_bin = '1111'
    else:
        exit(1)
    return x_bin

def hexToBin_loop(x_hex):
    x_bin = ''
    for i in range(len(x_hex)):
        x_bin = x_bin + hexToBin(x_hex[i])
    return x_bin

def dec2bin(d,nb=8):
    """Représentation d'un nombre entier en chaine binaire (nb: nombre de bits du mot)"""
    if d == 0:
        return "0".zfill(nb)
    if d<0:
        d += 1<<nb
    b=""
    while d != 0:
        d, r = divmod(d, 2)
        b = "01"[r] + b
    return b.zfill(nb)
#bin = print(type((dec2bin(43,nb=24))))

def mask_obuMess_match(n_mask, offset, length, value, mess_bin):
    if(len(mess_bin) >= (offset[n_mask - 1] + length[n_mask - 1])):
        counter = 0
        for i in range(0,n_mask):
            O = offset[i]
            L = length[i]
            V = value[i]
            counter = counter + (mess_bin[O:O+L] == format(V,'b').zfill(L))
        if(counter == n_mask):
            return 1
        else:
            return 0
    else:
        return 0
    
    
    

'''bin = '000000010011111100111111001111110011111100001000001111110010110101010000010011110011111100100111'
n_mask = 3
offset = [0,17,93]
length = [8,2,3]
value = [1,1,7]

print(mask_obuMess_match(n_mask, offset, length, value, bin))
print(len(bin))'''

    
    
