class PriorityQueueBase(object):
    __slots__ = "_key","_value"
    class _Item:
        def __init__(self,k,v):
            self._key = k
            self._value = v
        
        def __lt__(self,other):
            return self._key < other._key
        
    def is_empty(self):
        return len(self)
            
class HeapPriorityQueue(PriorityQueueBase):
    def _left(self,index):
        return 2*index+1
    
    def _right(self,index):
        return 2*index+2
    
    def _parent(self,j):
        return (j-1)//2
    
    def _has_left(self,index):
        return (2*index + 1)<len(self.queue)
    
    def _has_right(self,index):
        return (2*index+2)<len(self.queue)
    
    def _swap(self,i,j):
        t = self.queue[i]
        self.queue[i] = self.queue[j]
        self.queue[j] = t
    def _upheap(self,j):
        parent = self._parent(j)
        if j>0 and self.queue[j]<self.queue[parent]:
            self._swap(parent,j)
            self._upheap(parent)
    def _downheap(self,j):
        if self._has_left(j):
            left = self._left(j)
            if self.queue[left]<self.queue[j]:
                min_child = left
                if self._has_right(j): 
                    right = self._right(j)
                    if self.queue[right]<self.queue[left]:
                        min_child = right
                if self.queue[j]<self.queue[min_child]:
                    self._swap(min_child,j)
                    self._downheap(min_child)
    
    def __init__(self):
        self.queue = []
    
    def __len__(self):
        return len(self.queue)
    
    def _add(self,key,value):
        self.queue.append(self._Item(key,value))
        self._upheap(len(self.queue)-1)
    
    def _min(self):
        if len(self.queue) == 0:
            raise Exception(" priority queue is empty")
        item = self.queue[0]
        return (item._key,item._value)
    
    def remove_min(self):
        if len(self.queue) == 0:
            raise Exception("priority queue is empty")
        self._swap(0,len(self.queue)-1)
        item = self.queue.pop()
        self._downheap(0)
        return item._key,item._value
    

class AdaptableHeapPriorityQueue(HeapPriorityQueue):
    class Locator(HeapPriorityQueue._Item):
        __slots__ = "_index"
        def __init__(self,k,v,j):
            super().__init__(k, v)
            self._index = j
    
    def _swap(self,i,j):
        super()._swap(i,j)
        self.queue[i]._index = i
        self.queue[j]._index = j
    
    def _bubble(self,j):
        if j>0 and self.queue[j]<self.queue[self._parent(j)]:
            self._upheap(j)
        else:
            self._downheap(j)
    def _add(self,key,value):
        token = self.Locator(key, value,len(self.queue))
        self.queue.append(token)
        self._upheap(len(self.queue)-1)
        return token
    
    def _update(self,loc,new_key,new_value):
        j = loc._index
        loc._key = new_key
        loc._value = new_value
        self._bubble(j)
    def remove(self,loc):
        j = loc._index
        if j == len(self)-1:
            self.queue.pop()
        else :
            self._swap(j,len(self)-1)
            self.queue.pop()
            self._bubble(j)
        return loc._key,loc._value
    

import sys
class Graph_algorithms( AdaptableHeapPriorityQueue):
    def __init__(self,V,graph):
        self.graph = graph
        self.vertex = V
    def dijikstra(self,S):
        locations = {}
        visited = set([])
        x = AdaptableHeapPriorityQueue()
        for i in self.vertex:
            if i != str(S):
                locations[str(i)] = x._add(sys.maxsize,str(i))
            else:
                locations[str(i)] = x._add(0,str(i))
        while True :
            if len(x.queue) == 0:
                break
            u,m = x.remove_min()
            
            visited.add(m)
            M = list(self.graph[m].keys())
            for i in M :
                if i not in visited:
                    print(self.graph[m][i])
                    if x.queue[locations[i]._index]._key > u+self.graph[m][i]:
                        x._update(locations[i],u+int(self.graph[m][i]),i)
        M = {}
        for i in locations:
            M[locations[i]._value] = locations[i]._key
        return M
    
V = ["0","1","2","3","4"]
G = {"0":{"1":10,"2":5},"1":{"3":1,"2":2},"2":{"4":2,"1":3,"3":9},
     "3":{"4":4},"4":{"3":6,"0":7}}
x = Graph_algorithms(V,G)

print(x.dijikstra("0"))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        