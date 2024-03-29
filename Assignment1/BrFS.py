import queue

def printSolution(listQ):
    print(listQ)
    for i in range(N):
        str=""
        for col in range(len(listQ)):
            if listQ[col]==i:
                str+="Q "
            else:
                str+=". "
        print(str)
    print('\n')


def isSafe(listQ, posQ):
    col=len(listQ)
    for i in range(col):
        if (listQ[i]==posQ or col-i==abs(posQ-listQ[i])):
            return False
    
    return True

totalSolution=0
def solveNQueens():
    frontier=queue.Queue()
    listQ=[]
    stateQueens=[]
    global totalSolution
    frontier.put(stateQueens)

    while frontier.empty()==False:
        listQ=frontier.get()
        if len(listQ)==N:
            totalSolution+=1
            printSolution(listQ)
            continue

        for i in range(N):
            if isSafe(listQ, i)==True:
                stateQueens=listQ.copy()
                stateQueens.append(i)
                frontier.put(stateQueens)


def main():
    n=input("Size of board: ")
    global N
    N=int(n)
    solveNQueens()
    print("Total solution of N-Queens problem with size {} is {}.".format(N, totalSolution))
    

if __name__=="__main__":
    main()
