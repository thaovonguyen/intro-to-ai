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
def solveNQueens(listQ, col):
    global totalSolution
    if col==N:
        totalSolution+=1
        printSolution(listQ)
        return True
        
    for i in range(N):
        if isSafe(listQ, i)==True:
            listQ.append(i)
            solveNQueens(listQ, col+1)
            listQ.pop()


def solve():    
    listQueens=[]
    solveNQueens(listQueens, 0)


def main():
    n=input("Size of board: ")
    global N
    N=int(n)
    solve()
    print("Total solution of N-Queens problem with size {} is {}.".format(N, totalSolution))
    

if __name__=="__main__":
    main()
