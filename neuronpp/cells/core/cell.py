class Cell:
    def __init__(self, name):
        """
        :param name:
            Name of the cell
        """
        self.name = name

    def _filter_obj_dict(self, obj_dict_name, mech_type: str = None, names=None, as_list=False):
        """
        :param obj_dict_name:
            Name of the attribute dict with structure dict[name] = value
        :param mech_type:
            Mechanism name. Optional if require prefix for name, eg. SynACh_head[0] -> SynACh is mech_name here.
            Can be single string without spaces.
        :param names:
            List of string names as list or separated by space.
            Filter will look for obj_dict keys which contains each sec_name.
            None or 'all' will return all sections.
        :param as_list:
            if return as list. Otherwise will return as dict with name as key
        :return
            dict[sec_name] = sec
        """
        if names == 'all':
            names = None

        if isinstance(names, str):
            names = names.split(' ')

        if not hasattr(self, obj_dict_name):
            raise ProcessLookupError(
                "Object of class %s has no dict attribute of %s." % (self.__class__.__name__, obj_dict_name))

        obj_dict = getattr(self, obj_dict_name)
        if not isinstance(obj_dict, dict):
            raise AttributeError("Object of class %s has attribute %s, but it is not a dictionary." % (
            self.__class__.__name__, obj_dict_name))

        if mech_type:
            names = ["%s_%s" % (mech_type, n) for n in names]

        result = [] if as_list else {}
        for k, v in obj_dict.items():
            if names is None:
                if as_list:
                    result.append(v)
                else:
                    result[k] = v
                continue

            for s in names:
                # section names (especially created by NEURON or hoc) frequently have array-like string name
                # eg. soma[0]. User can specify exact name eg. dend[12]
                # or group of names eg. dend (if apply to array-like naming convention)
                # or single name without array-like brackets (mostly this case works for user-defined compartments)
                if self._is_array_name(k) and not self._is_array_name(s):
                    sec_name = ''.join(k.split("[")[:-1])
                else:
                    sec_name = k
                if s.lower() == sec_name.lower():
                    if as_list:
                        result.append(v)
                    else:
                        result[k] = v
                    break

        if len(result) == 0:
            if names:
                raise LookupError("Cannot find sections of type %s and named %s" % (obj_dict_name, names))
            else:
                raise LookupError("Cannot find any sections of type %s." % obj_dict_name)

        return result

    @staticmethod
    def _is_array_name(name):
        return "[" in name

    def __repr__(self):
        return "Cell[{}]".format(self.name)
