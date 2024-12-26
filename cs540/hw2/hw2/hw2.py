import sys
import math


def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)

def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    X=dict()
    
    with open (filename,encoding='utf-8') as f:
        # TODO: add your code here
        msg = f.read()
        msg_upper = msg.upper()
        
        for i in range(65,91):
            X[chr(i)] = 0
        
        for letter in msg_upper:
            if letter in X:
                X[letter] +=1

    return X


def print_q1(filename):
    print("Q1")
    shred_dict = shred(filename)
    for letter in shred_dict:
        print(letter, shred_dict[letter])


def print_q2(filename):
    print("Q2")
    shred_dict = shred(filename)
    e_vals, s_vals = get_parameter_vectors()
    print(round(shred_dict["A"] * math.log(e_vals[0]), 4))
    print(round(shred_dict["A"] * math.log(s_vals[0]), 4))


def print_q3(filename, p_english = 0.6, p_spanish = 0.4):
    print("Q3")
    
    shred_dict = shred(filename)
    X_values = list(shred_dict.values())
       
    summation_english = 0
    summation_spanish = 0
    
    e_vals, s_vals = get_parameter_vectors()
        
    for i in range(len(X_values)):
        summation_english += X_values[i] * math.log(e_vals[i])
        summation_spanish += X_values[i] * math.log(s_vals[i])

    f_english = math.log(float(p_english)) + summation_english
    f_spanish = math.log(float(p_spanish)) + summation_spanish
    print(round(f_english, 4))
    print(round(f_spanish, 4))


def print_q4(filename, p_english = 0.6, p_spanish = 0.4):
    
    shred_dict = shred(filename)
    X_values = list(shred_dict.values())
    summation_english = 0
    summation_spanish = 0
    
    e_vals, s_vals = get_parameter_vectors()
        
    for i in range(len(X_values)):
        summation_english += X_values[i] * math.log(e_vals[i])
        summation_spanish += X_values[i] * math.log(s_vals[i])
    
    f_english = math.log(float(p_english)) + summation_english
    f_spanish = math.log(float(p_spanish)) + summation_spanish

    if f_spanish - f_english >= 100:
        P_english = 0
    elif f_spanish - f_english <= -100:
        P_english = 1
    else:
        denom = 1 + math.e **(f_spanish - f_english)
        P_english = 1 / denom
        
    print("Q4")
    print(round(P_english, 4))


print_q1(sys.argv[1])
print_q2(sys.argv[1])
print_q3(sys.argv[1], sys.argv[2], sys.argv[3])
print_q4(sys.argv[1], sys.argv[2], sys.argv[3])

# +
#print_q1(("samples\letter0.txt"))
#print_q2(("samples\letter0.txt"))
#print_q3(("samples\letter0.txt"))
#print_q4(("samples\letter0.txt"))

# +
#print_q1(("samples\letter3.txt"))
#print_q2(("samples\letter3.txt"))
#print_q3(("samples\letter3.txt"))
#print_q4(("samples\letter3.txt"))
# -

#sample_0 = shred("samples\letter0.txt")
#with open ("samples\letter0_out.txt",encoding='utf-8') as f:
 #   answer_0 = f.read()
#print(answer_0)

# +
#sample_1 = shred("samples\letter1.txt")
#with open ("samples\letter1_out.txt",encoding='utf-8') as f:
#    answer_1 = f.read()
#print(answer_1)
# -

#sample_2 = shred("samples\letter2.txt")
#with open ("samples\letter2_out.txt",encoding='utf-8') as f:
 #   answer_2 = f.read()
#print(answer_2)

#sample_3 = shred("samples\letter3.txt")
#with open ("samples\letter3_out.txt",encoding='utf-8') as f:
 #   answer_3 = f.read()
#print(answer_3)

#sample_4 = shred("samples\letter4.txt")
#with open ("samples\letter4_out.txt",encoding='utf-8') as f:
 #   answer_4 = f.read()
#print(answer_4)

# TODO: add your code here for the assignment
# You are free to implement it as you wish!
# Happy Coding!


