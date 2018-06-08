from __future__ import division
class Node():
    def __init__(self,child0=None,child1=None,operator=None,value=None):
        if not value is None:
            self.value = value
            self.left = None
            self.right = None
        else:
            if not child0.value is None and not child1.value is None:
                self.left = child0 if child0.value > child1.value else child1
                self.right = child1 if child0.value > child1.value else child0
                self.operator = operator
                opMap = {
                    'plu':self.left.value+self.right.value,
                    'min':self.left.value-self.right.value,
                    'mul':self.left.value*self.right.value,
                    'div':self.left.value/self.right.value if self.right.value!=0 else None,
                    'bak':self.right.value/self.left.value if self.left.value!=0 else None
                }
                self.value = opMap[operator]
            else:
                print('noerror')
                self.value=None
def get_raw():
    while True:
        rawstr = raw_input('INPUT YOUR FOUR NUMBERS, DIVIDED BY \",\":: ')
        li = rawstr.split(',')
        result = []
        if len(li)!=4:
            print('#'*4+'THIS PROGRAM TAKES EXACTLY 4 INTEGERS')
        else:
            for item in li:
                try:
                    if int(item)>=1:
                        result.append(int(item))
                    else:
                        print('#'*4+'ALL INPUTS HAS TO BE >=1')
                except ValueError as e:
                    print('#'*4+'ALL INPUTS SHOULD BE INTERGERS')
                    print(e)
            if len(result)==4:
                return result
def sep(nums):
    #nums = get_raw()
    result = []
    for i in range(1,4):
        temp_nums = list(nums)
        a = temp_nums[0]
        b = temp_nums[i]
        first = [a,b]
        temp_nums.remove(a)
        temp_nums.remove(b)
        rest = temp_nums
        result.append([first,rest])
    temp_result = []
    for group in result:
        for item in group:
            temp_group = list(group)
            temp = []
            for num in item:
                temp.append([num])
            temp_group.remove(item)
            temp.append(temp_group[0])
            temp_result.append(temp)
    result += temp_result
    return result

def check():
    grouped = sep(get_raw())
    operators = ['plu','min','mul','div','bak']
    for group in grouped:
        if len(group)==2:
            for op in operators:
                node1 = Node(child0=Node(value=group[0][0]),child1=Node(value=group[0][1]),operator=op)
                for op1 in operators:
                    node2 = Node(child0=Node(value=group[1][0]),child1=Node(value=group[1][1]),operator=op1)
                    for op2 in operators:
                        final = Node(node1,node2,operator=op2)
                        if final.value > 23.999 and final.value < 24.001:
                            return "({0}{1}{2}){3}({4}{5}{6})".format(
                                final.left.left.value,
                                final.left.operator,
                                final.left.right.value,
                                final.operator,
                                final.right.left.value,
                                final.right.operator,
                                final.right.right.value,)
        elif len(group)==3:
            for op in operators:
                node1 = Node(child0=Node(value=group[2][0]),child1=Node(value=group[2][1]),operator=op)
                for i in range(0,2):
                    node2 = Node(value=group[i][0])
                    for op1 in operators:
                        node3 = Node(node1,node2,op1)
                        node4 = Node(value=group[1][0]) if i==0 else Node(value=group[0][0])
                        for op2 in operators:
                            final = Node(node3,node4,operator=op2)
                            if final.value > 23.999 and final.value < 24.001:
                                result_str = ""
                                if final.left.left is None:
                                    result_str+=str(final.left.value)+final.operator
                                    if final.right.left.left is None:
                                        result_str+='('+str(final.right.left.value)+final.right.operator
                                        result_str+='('+str(final.right.right.left.value)+final.right.right.operator+str(final.right.right.right.value)+'))'
                                    else:
                                        result_str+='('+str(final.right.left.left.value)+final.right.left.operator+str(final.right.left.right.value)+')'
                                        result_str+=final.right.operator+str(final.right.right.value)
                                elif final.right.left is None:
                                    result_str+=str(final.left.left.value)+final.left.operator
                                    result_str+='('+str(final.left.right.left.value)+final.left.right.operator+str(final.left.right.right.value)+')'
                                    result_str+=final.operator+str(final.right.value)
                                else:
                                    result_str+='('+str(final.left.left.left.value)+final.left.left.operator+str(final.left.left.right.value)+')'
                                    result_str+=final.left.operator+str(final.left.right.value)
                                    result_str+=final.operator+str(final.right.value)
                                return result_str
    return 'No Solution Found'
if __name__ == '__main__':
    print(check())