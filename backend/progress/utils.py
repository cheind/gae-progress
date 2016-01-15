

def ndbAttributesFromString(str, cls):
    """Convert stringified sorting order to database properties.

    Allows you to specify order such as '-lastUpdated,created',
    meaning that you want to order first based on lastUpdated descending,
    then on created ascending.

    This code is merely taken from Endpoints Proto Datastore API
    http://endpoints-proto-datastore.appspot.com/

    Args:
        str: Stringified sorting order.
        cls: ndb.Model class with properties.
    """

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
