def get_input():
    positive_decimal = int(input("enter a positive integer\n"))
    bit_size = int(input("enter the memory size in bits\n"))
    return positive_decimal , bit_size

def decimal_to_binary(str_num , bits):
    binary_str_num = bin(str_num)[2:]
    return binary_str_num.zfill(bits)

def twos_complemet(str_binary_num):
    inverted_str_num = "".join('1' if bit == '0' else '0' for bit in str_binary_num)
    decimal_value = bin(int(inverted_str_num , base =2)+1)[2:]
    return decimal_value







def main(): 

    positive_decimal , bit_size = get_input()
    binary_num = decimal_to_binary(positive_decimal , bit_size)
    negative_num = twos_complemet(binary_num)
    print (f"The decimal input: {positive_decimal}")
    print(f"The number in binary representation: {binary_num}")
    print(f"The negative binary number in twos complement method: {negative_num} ")

if __name__ == "__main__": 
    main()
    
    ## Done