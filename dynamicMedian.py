import heapq
class DynamicMedian:
    def __init__(self):
        self.minHp = []
        self.maxHp = []
        self.median = None
        self.size = 0

    def insert(self, i):
        if self.size == 0:
            heapq.heappush(self.minHp, i)
            self.median = i
        elif self.size % 2 == 0:
            if i >= self.median:
                heapq.heappush(self.minHp, i)
                self.median = self.minHp[0]
            else:
                heapq.heappush(self.maxHp, -i)
                self.median = -self.maxHp[0]
        else:
            if i >= self.median:
                heapq.heappush(self.minHp, i)
            else:
                heapq.heappush(self.maxHp, -i)
            if len(self.minHp) > len(self.maxHp):
                heapq.heappush(self.maxHp, -heapq.heappop(self.minHp))
            elif len(self.minHp) < len(self.maxHp):
                heapq.heappush(self.minHp, -heapq.heappop(self.maxHp))
            self.median = self.minHp[0]
        self.size += 1
    
    def getMedian(self):
        return self.median
    
    def delMedian(self):
        if self.size == 0:
            return
        if len(self.minHp) > len(self.maxHp):
            median = heapq.heappop(self.minHp)
            self.median = self.minHp[0]
        elif len(self.minHp) < len(self.maxHp):
            median = -heapq.heappop(self.maxHp)
            self.median = self.minHp[0]
        else:
            median = heapq.heappop(self.minHp)
            self.median = -self.maxHp[0]
        self.size -= 1
        return median
            

def main():
    dm = DynamicMedian()
    dm.insert(1)
    dm.insert(6)
    dm.insert(2)
    dm.insert(2)
    dm.insert(-1)
    dm.insert(3)
    # dm.insert(3)
    # dm.insert(3)
    dm.insert(4)
    dm.insert(5)
    print(dm.minHp)
    print(dm.maxHp)
    print(dm.getMedian())
    print(dm.delMedian())
    print(dm.minHp)
    print(dm.maxHp)
    print(dm.delMedian())
    print(dm.minHp)
    print(dm.maxHp)
    print(dm.delMedian())
    print(dm.getMedian())

if __name__ == '__main__': main()
