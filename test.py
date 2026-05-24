# x = [0,1,2,3,4]

# print(x[-2:])

# x.insert(-2,2)

# print(x)

# y = []

# y = [a for a in y if a]

# print(y)


# from utils import *

# x = calculate_manhattan((0,0),(16,32))

# print(x)

# print(25//32)

# print(2==1.0)

# print((Vector2(16,16)-Vector2(48,48)).length())

class XY():

    def __init__(self):
        self.num =23
        pass

    def pp(self):
        print(self.num)

    def ww(self):
        print(self.num)


class OOO():

    def __init__(self):
        self.num = 8394083429872349
        pass
        
    def pp(self):

        print(self.num)

    def ww(self):
        print(self.num)


a = XY()
b = OOO()


funcs = []

funcs.append(a.pp)
funcs.append(b.pp)

funcs.append(XY().ww)
funcs.append(OOO().ww)


for i in funcs:
    i()

l = {'kk':XY()}

l['kk'].num = 2020290981746739846972438248

l['kk'].ww()



class BB():

    def __init__(self):
        
        self.x = 32
        self.y = None
        self.z = None
        self.original_vars = None

    def init(self):

        self.y = 90

        self.original_vars = {k:v for k,v in self.__dict__.items()}

class DD(BB):

    def __init__(self):
        pass

    def init(self):

        self.z = 13404040

        return super().init()


class CC(DD):

    def __init__(self):
        DD.__init__(self)


    def init(self):
        self.x = 1111
        return super().init()
        
    


x = CC()
x.init()

print(x.y)
print(x.x)
print(x.z)
print(x.original_vars)



x = {'class':'Wall'}

import engine.pens as p
print(p.penHolder)