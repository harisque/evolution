from numpy.random import choice

def init_probability():
    p_map = [
        {
            'name':'move_up',
            'value':0.3/4
        },
        {
            'name':'move_right',
            'value':0.3/4
        },
        {
            'name':'move_down',
            'value':0.3/4
        },
        {
            'name':'move_left',
            'value':0.3/4
        },
        {
            'name':'move_none',
            'value':0.1
        },
        {
            'name':'grow_up',
            'value':0.3/4
        },
        {
            'name':'grow_right',
            'value':0.3/4
        },
        {
            'name':'grow_down',
            'value':0.3/4
        },
        {
            'name':'grow_left',
            'value':0.3/4
        },
        {
            'name':'prop',
            'value':0.3
        }
        ]
    result = []
    cur = 0
    while cur < 10:
        result.append([p['value'] for p in p_map])
        cur += 1
    return result
class Cell():
    '''BASIC ELEMENT'''
    def __init__(self,loc,size,id,probability):
        self.loc = loc
        self.size = size
        self.alive = True 
        self.id = id
        self.history = []
        self.p = probability
        self.child_probablity = self.p
        self.age = 0
        self.childen_count = 0
    def getArea(self):
        return self.size[0]*self.size[1]
    def adjust_children_probability(self,num):
        cur = 0
        while cur < 10:
            if cur != num:
                self.child_probablity[self.age][cur] -= 0.054/9
                if(self.child_probablity[self.age][cur]<0):
                    self.child_probablity[self.age][num]+=self.child_probablity[self.age][cur]
                    self.child_probablity[self.age][cur]=0
            else:
                self.child_probablity[self.age][cur] += 0.054
            cur += 1
    def inner_drive(self):
        def action(num):
            self.history.append(num)
            self.adjust_children_probability(num)
            #print(self.child_probablity[self.age])
            if num == 0:
                print("{0} CHOSE TO MOVE UP".format(self.id))
                self.move([0,1])#UP
            elif num == 1:
                print("{0} CHOSE TO MOVE RIGHT".format(self.id))
                self.move([1,0])#RIGHT
            elif num == 2:
                print("{0} CHOSE TO MOVE DOWN".format(self.id))
                self.move([0,-1])#DOWN
            elif num == 3:
                print("{0} CHOSE TO MOVE LEFT".format(self.id))
                self.move([-1,0])#left
            elif num == 4:
                print("{0} CHOSE TO NOT MOVE".format(self.id))
                self.move([0,0])#none
            elif num == 5:
                print("{0} CHOSE TO GROW UP".format(self.id))
                self.grow([0,1])#UP
            elif num == 6:
                print("{0} CHOSE TO GROW RIGHT".format(self.id))
                self.grow([1,0])#RIGHT
            elif num == 7:
                print("{0} CHOSE TO GROW DOWN".format(self.id))
                self.grow([0,1])
                self.move([0,-1])#DOWN
            elif num == 8:
                print("{0} CHOSE TO GROW LEFT".format(self.id))
                self.grow([1,0])
                self.move([-1,0])#left
            elif num == 9:
                print("{0} CHOSE TO PROP".format(self.id))
                self.prop()
        action(choice(range(10),p=self.p[self.age]))
        self.age += 1
        if self.age >= 10:
            self.kill('OLD')
    def check_over_border(self):
        if self.loc[0] + self.size[0]>world[0] or self.loc[0] <world[0]*-1:
            self.kill('OVER_BORDER')
            print('OVER BORDER,KILLED')
        elif self.loc[1] + self.size[1]>world[1] or self.loc[1] <world[1]*-1:
            self.kill("OVER_BORDER")
            print('OVER BORDER,KILLED')
        
    def matured(self):
        return self.size[0]*self.size[1]>1
    def move(self,vector):
        self.loc[0] += vector[0]
        self.loc[1] += vector[1]
        self.check_over_border()
    def grow(self,vector):
        self.size[0] += vector[0]
        self.size[1] += vector[1]
        self.check_over_border()
    def kill(self,reason):
        self.alive = False
        living_beings.remove(self)
        print("DEAD:: ID: {0}, HISTORY: {1}, size: {3}; REASON: {2}".format(self.id,self.history,reason,self.getArea()))
        self.size = (0,0)
    def prop(self):
        def cut(side):
            if side%2==0:
                return (side/2,side/2)
            else:
                return ((side+1)/2,side-(side+1)/2)
        if self.matured():
            if self.size[0] < self.size[1]:
                old = cut(self.size[1])[0]
                new = cut(self.size[1])[1]
                self.size[1]=old
                child = Cell(
                    [self.loc[0],self.loc[1]+self.size[1]],
                    [self.size[0],new],
                    self.id+str(self.childen_count),
                    self.child_probablity)
            else:
                old = cut(self.size[0])[0]
                new = cut(self.size[0])[1]
                self.size[0]=old
                child = Cell(
                    [self.loc[0]+self.size[0],self.loc[1]],
                    [new,self.size[1]],
                    self.id+str(self.childen_count),
                    self.child_probablity)
            new_baby.append(child)
            self.childen_count +=1
        else:
            if len(living_beings)<world[0]*world[1]/10000:
                child = Cell(
                    [self.loc[0],self.loc[1]+1],
                    [1,1],
                    self.id+str(self.childen_count),
                    self.child_probablity)
                new_baby.append(child)
                self.childen_count +=1
            else:
                print('NOT MATURED')
        
        

def init_world():
    global living_beings
    living_beings = []
    global world
    world = (500,500)
    living_beings.append(Cell([0,0],[1,1],'0',init_probability()))
    time = 0
    while time <1000:
        global new_baby
        new_baby = []
        print("#"*30+'THE {0} STEP OF THE WORLD'.format(time))
        for being in living_beings:
            being.inner_drive()
        living_beings.sort(key=lambda x:x.getArea(),reverse=True)
        rest = list(living_beings)
        #check conflict
        to_kill = []
        for i in range(len(living_beings)):
            being = living_beings[i]
            rest.remove(being)
            for r in rest:
                logic_left = r.loc[0] in range(being.loc[0],being.loc[0]+being.size[0])
                logic_right = r.loc[0]+r.size[0] in range(being.loc[0],being.loc[0]+being.size[0])
                logic_bottom = r.loc[1] in range(being.loc[1],being.loc[1]+being.size[1])
                logic_top = r.loc[1]+r.size[1] in range(being.loc[1],being.loc[1]+being.size[1])
                #logic_protect = (len(r.id) > len(being.id)) and (r.id[:len(being.id)]==being.id)
                if (logic_left or logic_right) and (logic_bottom or logic_top):
                    to_kill.append(r)
        to_kill = list(set(to_kill))
        for k in to_kill:
            k.kill('OTHER')
        time +=1
        print("-"*30+'THERE ARE {0} IN THE WORLD'.format(len(living_beings)))
        living_beings = new_baby + living_beings
if __name__ == "__main__":
    
    init_world()
                
                





