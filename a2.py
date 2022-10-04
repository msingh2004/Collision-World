eps = 0


def cmp(x, y):
    # Comparator to compare the tuples according to what order we want
    if x[0] < y[0] - eps:
        return True
    elif x[0] > y[0] + eps:
        return False
    else:
        if x[2] < y[2] - eps:
            return True
        elif x[2] > y[2] + eps:
            return False
        else:
            return x < y


def min_2(x, y):
    if cmp(x, y):
        return x
    else:
        return y


class heap:
    def __init__(self, n):
        self._list = []  # The array heap
        self._len = 0
        self._access_array = []  # access_array[i] gives the index of the ith particle in the list
        for i in range(n):
            self._access_array.append(-1)  #Initializing the empty locations to -1

    def is_empty(self):
        return self._len == 0

    def heap_up(self, x):  # Heap up operation, swapping the element x as long as it is smaller than its parent
        if x == 0:
            return
        while x > 0 and cmp(self._list[x], self._list[(x - 1) // 2]):
            self._list[x], self._list[(x - 1) // 2] = self._list[(x - 1) // 2], self._list[x]
            self._access_array[self._list[x][1]], self._access_array[self._list[(x - 1) // 2][1]] = self._access_array[self._list[(x - 1) // 2][1]], self._access_array[self._list[x][1]]
            x = (x - 1) // 2

    def enqueue(self, node):  # Adding a node to the heap
        self._list.append(node)
        self._len += 1
        self._access_array[node[1]] = self._len-1
        self.heap_up(self._len - 1)

    def heap_down(self, x):  # Swapping node x with min of its children as long as one of them is smaller than x
        while 2 * x + 1 < self._len:
            if 2 * x + 2 < self._len:
                if cmp(min(self._list[2 * x + 1], self._list[2 * x + 2]), self._list[x]):
                    if cmp(self._list[2 * x + 1], self._list[2 * x + 2]):
                        self._list[x], self._list[2 * x + 1] = self._list[2 * x + 1], self._list[x]
                        self._access_array[self._list[x][1]], self._access_array[self._list[2 * x + 1][1]] = self._access_array[self._list[2 * x + 1][1]], self._access_array[self._list[x][1]]

                        x = 2 * x + 1
                    else:
                        self._list[x], self._list[2 * x + 2] = self._list[2 * x + 2], self._list[x]
                        self._access_array[self._list[x][1]], self._access_array[self._list[2 * x + 2][1]] = self._access_array[self._list[2 * x + 2][1]], self._access_array[self._list[x][1]]

                        x = 2 * x + 2
                else:
                    break
            else:
                if cmp(self._list[2 * x + 1], self._list[x]):
                    self._list[x], self._list[2 * x + 1] = self._list[2 * x + 1], self._list[x]
                    self._access_array[self._list[x][1]], self._access_array[self._list[2 * x + 1][1]] = self._access_array[self._list[2 * x + 1][1]], self._access_array[self._list[x][1]]

                    x = 2 * x + 1
                else:
                    break

    def extract_min(self):  # Extracting the minimum element from the heap, and reheaping the entire thing
        self._len -= 1
        if len(self._list) == 1:
            self._access_array[self._list[0][1]] = -1
            return self._list.pop()

        w = self._list[0]
        u = self._list.pop()
        self._list[0] = u
        self._access_array[u[1]] = 0
        self._access_array[w[1]] = -1
        self.heap_down(0)
        return w

    def change_key(self, node):  # Changing the key of a particular node
        x2 = self._list[self._access_array[node[1]]]
        self._list[self._access_array[node[1]]] = node
        if cmp(node, x2):
            self.heap_up(self._access_array[node[1]])
        else:
            self.heap_down(self._access_array[node[1]])

    def add_node(self, node):  # Combines functionality of enqueue and change_key depending on whether we had a collision corresponding to that particle stored or not
        if self._access_array[node[1]] == -1:
            self.enqueue(node)
        else:
            self.change_key(node)

    def build_heap(self, l):  # Fast build_heap O(n) time
        self._len = len(l)
        self._list = l
        for i in range(len(l)):
            self._access_array[l[i][1]] = i

        for u in range(self._len - 1, -1, -1):

            self.heap_down(u)


def new_velocities(m1, v1, m2, v2):  # velocities after collision
    v1_new = ((m1 - m2)*v1)/(m1+m2) + 2*m2*v2/(m1+m2)
    v2_new = 2*m1*v1/(m1+m2) - ((m1-m2)*v2)/(m1+m2)
    return v1_new, v2_new


def listCollisions(M, x, v, m, T):
    n = len(M)
    ans = []
    counter = 0
    time = 0
    time_last = []  # storing the time at which ith particle last collided, 0 initially
    for j in range(n):
        time_last.append(0)
    collisions = heap(n)
    list_collisions = []  ####
    for i in range(n-1):
        if v[i+1] - v[i] < -1*eps:
            coll_time = (x[i+1]-x[i])/(v[i]-v[i+1])
            coll_place = x[i] + coll_time*v[i]
            list_collisions.append((coll_time, i, coll_place)) ####


    collisions.build_heap(list_collisions)  # Building the heap in O(n) time based on the collisions apparent from the initial list

    while (not collisions.is_empty()) and counter < m and time <= T:
        # Now we simulate the entire collision process, whenever we extract min, a collision takes place,
        # Then update the corresponding values of x, v, and time_last for ith and (i+1)th particle
        # Then we check if there is an imminent collision between particles i+1 and i+2 or i-1 and i, calculate the time and
        # place for this eventual collision and add it to our heap(the addition takes care of whether there was a possible collision between the two already or not)
        #As we are extracting min m times, and each time it takes O(logn) time, we have total complexity to be O(n+m*logn)
        node = collisions.extract_min()
        counter += 1
        i = node[1]
        time = node[0]
        v[i], v[i+1] = new_velocities(M[i], v[i], M[i+1], v[i+1])
        x[i], x[i+1] = node[2], node[2]
        time_last[i] = time
        time_last[i+1] = time
        if time <= T:
            ans.append((round(node[0], 4), node[1], round(node[2], 4)))

            if i != n-2:
                if v[i+2] - v[i+1] < -1*eps:

                    coll_time_2 = (x[i+2] + v[i+2]*(time - time_last[i+2]) - x[i+1])/(v[i+1]-v[i+2])
                    coll_pos_2 = v[i+1]*coll_time_2 + x[i+1]
                    collisions.add_node((coll_time_2 + time, i+1, coll_pos_2))

            if i != 0:
                if v[i] - v[i-1] < -1*eps:

                    coll_time_2 = (x[i] - x[i-1] - v[i-1]*(time - time_last[i-1]))/(v[i-1]-v[i])

                    coll_pos_2 = x[i] + v[i]*coll_time_2
                    collisions.add_node((coll_time_2 + time, i-1, coll_pos_2))

        else:
            break


    return ans

print(listCollisions( [10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 6, 10.0 ))