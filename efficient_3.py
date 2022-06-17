from concurrent.futures import process
import sys
import time
import psutil
import os


def minimum_penalty(x, y, gap, mismatch):
    # initialize pointers
    i = 0
    j = 0
    # pattern lengths
    m = len(x)
    n = len(y)
    # create tables to store minimum cost of an alignment
    # dp[i,j]: the min cost between x1,x2...xi and y1,y2...yj
    dp = [[None for j in range(n + 1)] for i in range(m + 1)]

    # initialize A[i,0] and A[0,j]
    for i in range(m + 1):
        dp[i][0] = i * gap
    for j in range(n + 1):
        dp[0][j] = j * gap

    # find the minimum penalty: recurrence relations
    # skip the first row (initialized) and start it from index 1
    i = 1
    while i <= m:
        j = 1  # skip the first column (initialized) and start it from index 1
        while j <= n:
            # compare the cost of 3 cases and find the minimum:
            # 1. add a mismatch cost
            # 2. add a gap to the second string
            # 3. add a gap to the first string
            dp[i][j] = min(
                dp[i - 1][j - 1] + mismatch[(x[i - 1], y[j - 1])],
                dp[i - 1][j] + gap,
                dp[i][j - 1] + gap)

            j += 1
        i += 1

    # Reconstructing the solution
    l = n + m  # maximum possible length of the optimal alignment
    i = m
    j = n

    xpos = l
    ypos = l

    # final two strings with gaps and mismatch
    x_opt = [None for i in range(l + 1)]
    y_opt = [None for j in range(l + 1)]

    # loop through until either the first pointer or the second pointer moves to the last element (the first element in the list)
    while not (i == 0 or j == 0):
        if (dp[i - 1][j - 1] + mismatch[(x[i - 1], y[j - 1])]) == dp[i][j]:
            x_opt[xpos] = ord(x[i - 1])
            y_opt[ypos] = ord(y[j - 1])
            xpos -= 1
            ypos -= 1
            i -= 1
            j -= 1
        # gap on the second string
        elif (dp[i - 1][j] + gap) == dp[i][j]:
            x_opt[xpos] = ord(x[i - 1])
            # add gap symbol to the second string element
            y_opt[ypos] = ord('_')
            xpos -= 1
            ypos -= 1
            i -= 1
        # gap on the first string
        elif (dp[i][j - 1] + gap) == dp[i][j]:
            # add gap symbol to the first string element
            x_opt[xpos] = ord('_')
            y_opt[ypos] = ord(y[j - 1])
            xpos -= 1
            ypos -= 1
            j -= 1

    while xpos > 0:
        if i > 0:
            i -= 1
            x_opt[xpos] = ord(x[i])
            xpos -= 1
        else:
            x_opt[xpos] = ord('_')
            xpos -= 1

    while ypos > 0:
        if j > 0:
            j -= 1
            y_opt[ypos] = ord(y[j])
            ypos -= 1
        else:
            y_opt[ypos] = ord('_')
            ypos -= 1

    # Since we have assumed the maximum optimal alignment to be n+m long,
    # we need to remove the extra gaps in the starting
    # idx represents the index from which the arrays
    # x_opt, y_opt are useful

    idx = 1
    i = l
    while i >= 1:
        if (chr(y_opt[i]) == '_') and chr(x_opt[i]) == '_':
            idx = i + 1
            break

        i -= 1

    # The final alignment after removing the extra gaps
    # X
    i = idx
    x_seq = ""
    while i <= l:
        x_seq += chr(x_opt[i])
        i += 1

    # Y
    i = idx
    y_seq = ""
    while i <= l:
        y_seq += chr(y_opt[i])
        i += 1

    return dp[m][n], x_seq, y_seq


def process_memory():
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


def Input_String_Generator(lines):
    number = list()
    string = list()
    index = list()
    result = list()
    resultmap = dict()
    for i in range(len(lines)):
        try:
            x = int(lines[i].rstrip("\n"))
            number.append(x)
        except ValueError:
            index.append(i)
            x = lines[i].rstrip("\n")
            string.append(x)
    number2 = list()
    number2.append(number[index[0]:index[1] - 1])
    number2.append(number[index[1] - 1:])

    x = string[0]
    for j in number2[0]:
        temp = x[0:j + 1] + x + x[j + 1:]
        x = temp
    result.append(x)

    x = string[1]
    for j in number2[1]:
        temp = x[0:j + 1] + x + x[j + 1:]
        x = temp
    result.append(x)

    return result


# Space efficient alignment, which caculates the length of the
# shortest path from (0,0) to (i,j) and only returns the optimal value.
# page 285 algorithm in book

def space_efficient(x, y, gap, mismatch):
    m, n = len(x), len(y)
    T = [[None for j in range(2)] for i in range(m+1)]
    for i in range(m+1):
        T[i][0] = gap * i
    for j in range(1, n+1):
        T[0][1] = gap * j
        for i in range(1, m+1):
            T[i][1] = min(T[i][0] + gap,
                          T[i-1][1] + gap,
                          T[i-1][0] + mismatch[(x[i-1],y[j-1])])
        for i in range(m+1):
            T[i][0] = T[i][1]
    T = [t[1] for t in T]
    mem_eff.append(process_memory())

    return T

# Backward space efficient alignment, which caculates the length of the
# shortest path from (i,j) to (m,n) and only returns the optimal value.

# this part is similar to space_efficient method(rotating)
# page 286 in book

def backspace_efficient(x, y, gap, mismatch):
    m, n = len(x), len(y)
    S = [[None for i in range(2)] for j in range(m+1)]
    for i in range(m+1):
        S[i][0] = gap * i
    for j in range(1, n+1):
        S[0][1] = gap * j
        for i in range(1, m+1):
            S[i][1] = min(S[i][0] + gap,
                          S[i-1][1] + gap,
                          S[i-1][0] + mismatch[(x[m-i],y[n-j])])
        for i in range(m+1):
            S[i][0] = S[i][1]
    S = [s[1] for s in S]
    mem_eff.append(process_memory())

    return S

# divide and conquer algorithm
def dc(x, y, gap, mismatch):
    m, n = len(x), len(y)
    
    if m<=2 or n<=2:
        return minimum_penalty(x, y, gap, mismatch)
    
    else:
        yleft = y[:n//2]
        yright = y[n//2:]
        F, B = space_efficient(x, yleft, gap, mismatch), backspace_efficient(x, yright, gap, mismatch)
        #partition = [F[j] + B[m-j] for j in range(m+1)]
        #cut = partition.index(min(partition))
        cut = 0
        opt = F[0] + B[m]
        for i in range(1, m+1):
            if F[i] + B[m-i] < opt:
                opt = F[i] + B[m-i]
                cut = i
        callLeft = dc(x[:cut], yleft, gap, mismatch)
        callRight = dc(x[cut:], yright, gap, mismatch)

        
        return callLeft[0]+callRight[0], callLeft[1]+callRight[1], callLeft[2]+callRight[2]


if __name__ == "__main__":
    # list that stores memory for each call on DC function
    mem_eff = list()

    start = time.time()
    # dictionary that stores all alpha values (mismatch costs)
    mismatch = {
        ('A', 'A'): 0,
        ('C', 'C'): 0,
        ('G', 'G'): 0,
        ('T', 'T'): 0,
        ('A', 'C'): 100,
        ('C', 'A'): 100,
        ('A', 'G'): 48,
        ('G', 'A'): 48,
        ('A', 'T'): 94,
        ('T', 'A'): 94,
        ('C', 'G'): 118,
        ('G', 'C'): 118,
        ('C', 'T'): 48,
        ('T', 'C'): 48,
        ('G', 'T'): 110,
        ('T', 'G'): 110
    }
    # delta (gap cost) value
    gap = 30

    # list that stores all system argument
    files_name = sys.argv
    input_file_path = files_name[1]
    output_file_path = files_name[2]
    # input_file_path = "../Project/SampleTestCases/input1.txt"
    # input_file_path = "../Project/datapoints/in4.txt"
    lines = open(input_file_path, 'r').readlines()
    strings = Input_String_Generator(lines)

    x = strings[0]  # the first sequence
    y = strings[1]  # the second sequence

    # min_cost = space_efficient(x, y, gap, mismatch)
    # min_cost2 = backspace_efficient(x, y, gap, mismatch)

    # print(minimum_penalty(x, y, gap, mismatch))
    # p = []  # keep track of all the half point that the shortest path passes through
    min_cost, first_seq, second_seq = dc(x, y, gap, mismatch)
    # print(min_cost)
    # print(first_seq)
    # # print(second_seq)
    # time_eff = (time.time()-start)*1000
    # print((time.time()-start)*1000)
    # # print(str(process_memory()) + '\n')
    # print(str(max(mem_eff))+'\n')

    f = open(output_file_path, 'w')
    f.write(str(min_cost)+'\n')
    f.write(first_seq+'\n')
    f.write(second_seq+'\n')
    f.write(str((time.time()-start)*1000)+'\n')
    f.write(str(max(mem_eff)))
    f.close()