
class Template:
    def __init__(self, *args, **kwargs):
        """
        It will work with each method which is decorated by the @template decorator
        in the object which implements Template
        :param name:
            name of the cell used for all templates
            it will be incremented with each cell created from the template
        :param compile_paths:
            paths to folders containing mods. Can be list or string separated by spaces.
        """
        self._cls = self._get_cls()
        self._counter = 0
        self._init_params = args, kwargs
        self._func_calls = []

    def build(self):
        """
        Build template.
        It is intended to use by Population object, no by the user.
        :return:
            tuple(new_cell, results)

            new_obj - a object created from the template
            results - list of results from the method called in the order by original object
            if method doesn't return any value - it result element will contain None
        """
        results = []
        obj = self._cls(*self._init_params[0], **self._init_params[1])
        for func, args, kwargs in self._func_calls:
            r = func(obj, *args, **kwargs)
            results.append(r)

        return obj, results

    def _get_cls(self):
        for c in self.__class__.mro():
            if Template not in c.mro():
                return c
