# creating a basic priority queue object that can perform comparisions with keys and have values as it is
class PriorityQueueBase(object):
    __slots__ = "_key","_value" # used for reduction of usage of RAM since for a class its attributes are stored in a dictionary and memory used by that dictionary is dynamic to limit usage we predefine __slots__
    class _Item: # to store keys and values and use only keys for comparision_purposes
        def __init__(self,k,v):
            self._key = k
            self._value = v
        
        def __lt__(self,other): #magic function that uses less than operation between two item i.e between their keys
            return self._key < other._key
        
    def is_empty(self):
        return len(self)
            
class HeapPriorityQueue(PriorityQueueBase): # using basically built PriorityQueueBase and using it through inheritance(OOP)
    def _left(self,index): # function returns position of left node of the parent
        return 2*index+1
    
    def _right(self,index): # function returns position of right node of the parent
        return 2*index+2
    
    def _parent(self,j): # returns parent of a node
        return (j-1)//2
    
    def _has_left(self,index): # checks if the node has a left value
        return (2*index + 1)<len(self.queue)
    
    def _has_right(self,index): # checks if the node has a right value
        return (2*index+2)<len(self.queue)
    
    def _swap(self,i,j): # swaps two positions (i,j) in the array
        t = self.queue[i]
        self.queue[i] = self.queue[j]
        self.queue[j] = t
    def _upheap(self,j): # performing_heapify operation from node to top
        parent = self._parent(j)
        if j>0 and self.queue[j]<self.queue[parent]:
            self._swap(parent,j)
            self._upheap(parent)
    def _downheap(self,j): # performing_heapify operation from node to bottom
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
        self.queue = [] # our data structure for storing _Items or (Locations comes in the next part of code)
    
    def __len__(self):
        return len(self.queue)
    
    def _add(self,key,value): # inseting a (key,value) pair into min_heap
        self.queue.append(self._Item(key,value))
        self._upheap(len(self.queue)-1)
    
    def _min(self): # quierying the minimum element of the heap
        if len(self.queue) == 0:
            raise Exception(" priority queue is empty")
        item = self.queue[0]
        return (item._key,item._value)
    
    def remove_min(self): # process similar to extract_min operation in heap
        if len(self.queue) == 0:
            raise Exception("priority queue is empty")
        self._swap(0,len(self.queue)-1)
        item = self.queue.pop()
        self._downheap(0)
        return item._key,item._value
    

class AdaptableHeapPriorityQueue(HeapPriorityQueue): # requirement of the problem is to quiery with vertices rather than indexes so i have added a Locator class to quiery the element and perform operations on it
    class Locator(HeapPriorityQueue._Item): # initializing Locator class
        __slots__ = "_index" # same as mentioned above to minimize the RAM usage
        def __init__(self,k,v,j):
            super().__init__(k, v) # inheritance
            self._index = j
    
    def _swap(self,i,j): # i changed it because we have _index which we must be able to change and add the nwely modified location of the node in the array
        super()._swap(i,j) # used swap from previous class
        self.queue[i]._index = i
        self.queue[j]._index = j
    
    def _bubble(self,j): # modifiying heap if some thing changes i.e any key or value of a heap is altered
        if j>0 and self.queue[j]<self.queue[self._parent(j)]:
            self._upheap(j)
        else:
            self._downheap(j)
    def _add(self,key,value): # adding (key,value) pair so that the heap invairent remains and the function returns the location of the (key,value) in heap at every instant
        token = self.Locator(key, value,len(self.queue))
        self.queue.append(token)
        self._upheap(len(self.queue)-1) # performing upheap to maintain heap invarient
        return token # returns the token i.e Locator Object of the added element 
    
    def _update(self,loc,new_key,new_value): # we must be able to update the key of the heap and track its location
        j = loc._index
        loc._key = new_key
        loc._value = new_value
        self._bubble(j) # since a key is added we perform _bubble operation to maintain heap invarient
    def remove(self,loc): # removing a node form heap i.e with known locate Object of the node we want to remove
        j = loc._index
        if j == len(self)-1:
            self.queue.pop()
        else :
            self._swap(j,len(self)-1)
            self.queue.pop() # removes element from the Node
            self._bubble(j) # to maintain heapinvarient
        return loc._key,loc._value # return popped values
    

import sys
class Graph_algorithms( AdaptableHeapPriorityQueue):
    def __init__(self,V,graph):
        self.graph = graph # initalized graph (used adjacency lists) 
        self.vertex = V # list of vertexes
    def dijikstra(self,S):
        locations = {} # created a dict to store locate Objects of differnt vertices in the heap
        visited = set([]) # created a set so as to add the curr_min and not change it __greedy__approach
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

print(x.dijikstra("0")) # add any node to the list and check
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
