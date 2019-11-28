# class MagicMeta(type):
#     """
#     调用MagicCall不存在的方法时，会调用其元类的getattr方法
#     """
#
#     def __getattr__(self, method_name):
#         def func(*args, **kwargs):
#             getattr(object.__new__(self), '_call_method')(method_name, *args, **kwargs)
#         return func
#
#
# class MagicCall(metaclass=MagicMeta):
#
#     def __getattr__(self, method_name):
#         def func(*args, **kwargs):
#             self._call_method(method_name, *args, **kwargs)
#         return func
#
#     def _call_method(self, method_name, *args, **kwargs):
#         pass
#
#
# class MyClass(MagicCall):
#
#     def _call_method(self, method_name, *args, **kwargs):
#         print(method_name, args, kwargs)
#
#     def __new__(cls, *args, **kwargs):
#         return object.__new__(cls)
#
#
# if __name__ == '__main__':
#     MyClass().hello('xxx', 'ppp', xname='linxianlong')
#     MyClass.hello('xxx', 'ppp', xname='linxianlong')


class MagicMeta(type):
    def __getattribute__(self, key):
        if key == "__new__":
            return object.__new__(self)
        try:
            return object.__getattribute__(self, key)
        except:
            return getattr(object.__new__(self), key)

class MagicCall(metaclass=MagicMeta):

    def __getattribute__(self, key):
        return object.__getattribute__(self, key)

    def __getattr__(self, key):
        raise AttributeError(r"%s has no attribute or method '%s'" % (
            self.__class__.__name__, key))

    def gets(self, *args, **kw):
        return self


class MyClass(MagicCall):
    pass



if __name__ == '__main__':
    print(MyClass().gets('xxx', 'ppp', xname='linxianlong'))
    # MyClass.gets('xxx', 'ppp', xname='linxianlong')