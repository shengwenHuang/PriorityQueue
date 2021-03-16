from collections import defaultdict
import random
import heapq
class Board:
    def swap(self, i, j, src):
        n = len(src)
        ri = (i - 1) // n
        ci = (i - 1) % n
        rj = (j - 1) // n
        cj = (j - 1) % n
        tiles = [[] for _ in range(n)]
        for r in range(n):
            tiles[r] = src[r][:]
        temp = tiles[ri][ci]
        tiles[ri][ci] = tiles[rj][cj]
        tiles[rj][cj] = temp
        return Board(tiles)

    def __init__(self, tiles):
        self._size = len(tiles)
        self._board = [[0 for _ in range(self._size)] for _ in range(self._size)]
        self._idx = defaultdict(list)
        self._adj = defaultdict(list)
        self._neighbor = []
        self._zero = -1
        for row in range(self._size):
            for column in range(self._size):
                self._board[row][column] = tiles[row][column]
                if self._board[row][column] == 0:
                    self._zero = row * self._size + column + 1
                curr = row * self._size + column + 1
                self._idx[curr] = [row, column]
                temp = []
                if row == 0:
                    temp.append(curr + self._size)
                if column == 0:
                    temp.append(curr + 1)

                if row == self._size - 1:
                    temp.append(curr - self._size)

                if column == self._size - 1:
                    temp.append(curr - 1)

                if 0 < row and row < self._size - 1:
                    temp.append(curr + self._size)
                    temp.append(curr - self._size)

                if 0 < column and column < self._size - 1:
                    temp.append(curr + 1)
                    temp.append(curr - 1)

                self._adj[curr] = temp
    
    def __lt__(self, other):
        return self.hamming() < other.hamming()

    def __eq__(self, other):
        if(other == None):
            return False
        if(not isinstance(other, Board)):
            return False
        return self.hamming() == other.hamming()

    def toString(self):
        s = str(self._size) + '\n'
        for row in range(self._size):
            temp = ' '.join(str(x) for x in self._board[row])
            s += temp + '\n'
        return s

    def dimension(self):
        return self._size

    def hamming(self):
        ham = 0
        for row in range(self._size):
            for column in range(self._size):
                if self._board[row][column] == 0:
                    continue
                if self._board[row][column] != row * self._size + column + 1:
                    ham += 1
        return ham

    def manhattan(self):
        man = 0
        for row in range(self._size):
            for column in range(self._size):
                if self._board[row][column] == 0:
                    continue
                goal = self._idx[self._board[row][column]]
                man += abs(row - goal[0]) + abs(column - goal[1])
        return man

    def isGoal(self):
        for row in range(self._size):
            for column in range(self._size):
                if row == self._size - 1 and column == self._size - 1 and self._board[row][column] == 0:
                    break
                if self._board[row][column] != row * self._size + column + 1:
                    return False
        return True

    def equals(self, b2):
        s1 = self.toString()
        s2 = b2.toString()
        return s1 == s2

    def neighbors(self):
        adjSpace = self._adj[self._zero]
        for i in range(len(adjSpace)):
            self._neighbor.append(self.swap(self._zero, adjSpace[i], self._board))
        return self._neighbor

    def twin(self):
        n = self._size * self._size
        origin = random.randrange(1 + self._zero, n + self._zero)
        originR = ((origin - 1) % n) // self._size
        originC = ((origin - 1) % n) % self._size
        new = random.randrange(1 + self._zero, n + self._zero)
        newR = ((new - 1) % n) // self._size
        newC = ((new - 1) % n) % self._size

        tiles = [[] for _ in range(self._size)]
        for i in range(self._size):
            tiles[i] = self._board[i][:]
        temp = tiles[newR][newC]
        tiles[newR][newC] = tiles[originR][originC]
        tiles[originR][originC] = temp
        return Board(tiles)

class Solver():
    def __init__(self, initial):
        self._initial = initial
        self._twin = initial.twin()
        self._solution = []
        self._move = -1
        self._pq = []
        self._twin_pq = []
        self._solvable = False

        step = 0
        path = []
        priority = self._initial.manhattan() + step
        twin_priority = self._twin.manhattan() + step
        heapq.heappush(self._pq, (priority, step, self._initial))
        path.append(self._initial)
        heapq.heappush(self._twin_pq, (twin_priority, step, self._twin))
        top = heapq.heappop(self._pq)
        twin_top = heapq.heappop(self._twin_pq)
        visited = set()
        twin_visited = set()
        while not top[2].isGoal() and not twin_top[2].isGoal() and step < 5:
            # print(step)
            step += 1
            visited.add(top[2].toString())
            twin_visited.add(twin_top[2].toString())
            neighbor = top[2].neighbors()
            for i in range(len(neighbor)):
                if neighbor[i].toString() not in visited:
                    # print('push', neighbor[i].toString())
                    priority = neighbor[i].manhattan() + step
                    heapq.heappush(self._pq, (priority, step, neighbor[i]))
            top = heapq.heappop(self._pq)
            # print('pop', top[2].toString())
            path.append(top[2])

            twin_neighbor = twin_top[2].neighbors()
            for i in range(len(twin_neighbor)):
                if twin_neighbor[i].toString() not in twin_visited:
                    twin_priority = twin_neighbor[i].manhattan() + step
                    heapq.heappush(self._twin_pq, (twin_priority, step, twin_neighbor[i]))
            twin_top = heapq.heappop(self._twin_pq)

        if top[2].isGoal():
            self._solvable = True
            self._move = step
            self._solution = path

    def isSolvable(self):
        return self._solvable
    
    def moves(self):
        return self._move

    def solution(self):
        return self._solution


def main():
    # b1 = Board([[8, 1, 3], [4, 0, 2], [7, 6, 5]])
    # print('b1 dimenstion: ', b1.dimension())
    # print('b1 is goal? ', b1.isGoal())
    # print("b1: " + b1.toString())
    # print("b1 hamming & manhattan: ", b1.hamming(), " ", b1.manhattan())
    # print("b1 neighbors: ")
    # n = b1.neighbors()
    # for i in range(len(n)):
    #     print(n[i].toString())
    # b2 = Board([[1, 2, 3], [7, 8, 5], [0, 4, 6]])
    # print("b1 equals [[1, 2, 3], [7, 8, 5], [0, 4, 6]? ", b1.equals(b2))
    # print("b2 twin: \n", b2.twin().toString())
    initial = Board([[1, 2, 3], [4, 5, 6], [8, 7, 0]])
    solver = Solver(initial)

    if not solver.isSolvable():
        print("No solution")
    else:
        print("Min moves = ", solver.moves())
        for b in solver.solution():
            print(b.toString())

if __name__ == '__main__': main()
