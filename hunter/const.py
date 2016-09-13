'''
File: const.py
Description:
实现常量
'''
#用法演示，继承使用
'''
class A(_const):
    def __init__(self):
        self.CONST1=1
        self.CONST2=2


A1=A()
print(A1.CONST1)
A1.CONST1=2
'''

class _const:
    '''
    _const类：  常量类
    常量要求： 无法改变 ；  全部变量名大写
    '''
    class ConstError(TypeError): pass
    class ConstCaseError(ConstError): pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError  ('Cant change const.%s' % name)
        if not name.isupper():
            raise self.ConstCaseError  ('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value





