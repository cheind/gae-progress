
def ndbAttributesFromString(str, cls):
    if (not isinstance(str, basestring)):
        return None

    unclean_attr_names = str.strip().split(',')
    result = []
    for attr_name in unclean_attr_names:
        ascending = True
        if attr_name.startswith('-'):
            ascending = False
            attr_name = attr_name[1:]

        attr = cls._properties.get(attr_name)
        if attr is None:
            raise AttributeError('Order attribute %s not defined.' % (attr_name,))

        if ascending:
            result.append(+attr)
        else:
            result.append(-attr)

    return tuple(result)
