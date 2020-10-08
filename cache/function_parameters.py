class FunctionArguments:
    """ This objects represents a list of arguments given to a function. It's hashable, therefore you can use it
        as a dictionary key. """
    def __init__(self, *args, **kwargs):
        self.positional_arguments = args
        self.keyword_arguments = kwargs

    @property
    def _identifier(self):
        """ Unique hashable identifier for objects with the same attributes. """
        return tuple(self.positional_arguments) + tuple(self.keyword_arguments.items())

    def __str__(self):
        return f'Positional arguments={self.positional_arguments}. Keyword arguments={self.keyword_arguments}'

    # Methods to make the object hashable
    def __hash__(self):
        """ Instances with the same arguments are going to have the same hash. """
        return hash(self._identifier)

    def __eq__(self, other):
        return hash(self) == hash(other)