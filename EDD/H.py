import sys
sys.setrecursionlimit(3000)

# el problema se modelara como una lista de listas donde el #
# elemento superior sera el 0,0 y los inferiores del n,0 hasta el n,n #

class Pyramid:

    def __init__(self):#, lista, height):
        #self.balls = lista
        #self.height = height
        self.balls = [[3], [-5, 3], [-8, 2, -8], [3, 9, -2, 7]]
        self.height = 4
        self.max_price = 0
        self.values = {}
        self.all_used_nodes = {}


    def set_values(self):
        for i in range(len(self.balls)):
            for j in range(len(self.balls[i])):
                if i == j:
                    self.balls[i][j] = self.balls[i][j]
                else:
                    self.balls[i][j] = self.balls[i][j] + self.balls[i-1][j]



    def find_price(self, i, j, used_nodes):
        if (i,j) in self.all_used_nodes:
            return 0

        if (i,j) in self.values:
            return self.values[(i,j)]

        if j == 0 and (i,j):
            return self.balls[i][j]

        else:
            self.values[(i,j)] = self.balls[i][j] + self.find_price(i-1, j-1)
            return self.values[(i,j)]


    def set_used_nodes(self, used_nodes, i, j):
        used_nodes[(x,y)] = True

        for y in range(j+1)[::-1]:
            if i+1 == -1:
                print("[set_used_nodes]: i+1 = -1 HAPPENS")
                return used_nodes

            for x in range(i+1)[::-1]:
                print("Banned Nodes: ({},{})\n".format(x, y))
                if (x,y) not in self.all_used_nodes:
                    self.all_used_nodes[(x,y)] = 1
                else:
                    self.all_used_nodes[(x,y)] += 1
            i -= 1
        return used_nodes

    def unset_used_nodes(self, used_nodes, i, j):
        del used_nodes[(x,y)]

        for y in range(j+1)[::-1]:
            if i+1 == -1:
                print("[set_used_nodes]: i+1 = -1 HAPPENS")
                return used_nodes

            for x in range(i+1)[::-1]:
                print("Banned Nodes: ({},{})\n".format(x, y))
                if self.all_used_nodes[(x,y)] == 1:
                    del self.all_used_nodes[(x,y)]
                else:
                    self.all_used_nodes[(x,y)] -= 1
            i -= 1
        return used_nodes

    def find_biggest_price(self, domain, last_value, used_nodes):

        if domain == {}:
            #Only at start do we set the domain value#
            size = 0
            for i in range(len(self.balls)):
                for j in range(len(self.balls[i])):
                    domain[size] = (i,j)
                    check_domain[(i,j)] = True
                    size += 1

        max = 0

        for pos in range(len(size)):
            #Iterate through posibilities#
            #Stablish tempting domain value#
            (i,j) = domain[size[pos]]
            if check_domain[(i,j)] and (i,j) not in used_nodes:
                price = find_price(i, j)
                if price > 0:
                    #If price is over 0 at current standard then check it out#
                    # to check it out we must first add used_nodes
                    used_nodes = self.set_used_nodes(used_nodes, i, j)

                    get_value = self.find_biggest_price(domain, last_value + price, used_nodes)

    ]               used_nodes = self.unset_used_nodes(used_nodes, i, j)

                if(get_value > max):

                    self.max_price = get_value




p = Pyramid()
print(p.balls)
p.set_values()
print(p.balls)

p.find_biggest_price()

print()
