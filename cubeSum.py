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
    inpt = input("Please input n: ")
    n = int(inpt)
    for i in range(n):
        heapq.heappush(pq, Taxicab(i, i))

    while pq:
        curr = heapq.heappop(pq)
        print(curr.sum, ' = ', curr.i, '^3 + ', curr.j, '^3')

        if curr.j < n:
            heapq.heappush(pq, Taxicab(curr.i, curr.j + 1))


if __name__ == '__main__': main()
