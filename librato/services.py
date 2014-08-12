class Service(object):
    """Librato Service Base class"""
    properties = (
        'id',
        'type',
        'settings',
        'title'
    )

    def __init__(self, connection, *args, **kwargs):
        for dictionary in args:
            for key in dictionary:
                if not key == "conditions" and not key == "services":
                    setattr(self, key, dictionary[key])
        for key in kwargs:
            if not key == "conditions" and not key == "services":
                setattr(self, key, kwargs[key])
        if not hasattr(self, 'version'): self.version = 2
        for prop in self.properties:
            if not hasattr(self, prop): setattr(self, prop, None)

    @classmethod
    def from_dict(cls, connection, data):
        """Returns a metric object from a dictionary item,
        which is usually from librato's API"""
        return cls(connection, data)

    def get_payload(self):
        payload = {}
        for prop in self.properties:
            payload[prop] = getattr(self, prop)
        return payload