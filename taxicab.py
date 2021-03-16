import heapq
class Taxicab:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.sum = pow(i, 3) + pow(j, 3)

    def __lt__(self, other):
        if self.sum == other.sum:
            return self.i < other.i
        return self.sum < other.sum

def main():
    pq = []
    ans = []
    inpt = input("Please input n: ")
    n = int(inpt)
    for i in range(1, n):
        heapq.heappush(pq, Taxicab(i, i))
    
    prev = Taxicab(0, 0)
    count = 1
    while pq:
        curr = heapq.heappop(pq)
        if curr.sum == prev.sum:
            count += 1
            if count == 2:
                ans.append([curr.sum, prev.i, prev.j, curr.i, curr.j])
        else:
            count = 1
        prev = curr

        if curr.j < n:
            heapq.heappush(pq, Taxicab(curr.i, curr.j + 1))

    print(ans)

if __name__ == '__main__': main()
