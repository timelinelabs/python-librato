from librato.services import Service

class Alert(object):
    """Librato Alert Base class"""
    properties = {
        1: (
            'id',
            'name',
            'version',
            'active',
            'services',
            'entity_type',
            'entity_name',
            'thresh_above_value',
            'thresh_below_value'
            ),
        2: (
            'id',
            'name',
            'version',
            'active',
            'services',
            'conditions', 
            'description',
            'rearm_seconds',
            'attributes',
            'created_at',
            'updated_at'
            )
    }

    def __init__(self, connection, *args, **kwargs):
        for dictionary in args:
            for key in dictionary:
                if not key == "conditions" and not key == "services":
                    setattr(self, key, dictionary[key])
        for key in kwargs:
            if not key == "conditions" and not key == "services":
                setattr(self, key, kwargs[key])
        if not hasattr(self, 'version'): self.version = 2
        for prop in self.properties[self.version]:
            if not hasattr(self, prop): setattr(self, prop, None)


    @classmethod
    def from_dict(cls, connection, data):
        """Returns an alert object from a dictionary item,
        which is usually from librato's API"""
        obj = cls(connection, data)
        if 'services' in data:
            obj.services = []
            for s in data['services']:
                if isinstance(s, Service):
                    obj.services.append(s)
                elif isinstance(s, dict):
                    obj.services.append(Service.from_dict(connection, s))
        if 'conditions' in data:
            obj.conditions = []
            for c in data['conditions']:
                if isinstance(c, Condition):
                    obj.conditions.append(c)
                elif isinstance(c, dict):
                    obj.conditions.append(Condition(connection, c))
        return obj

    def get_payload(self):
        payload = {}
        payload['version'] = self.version
        for prop in self.properties[self.version]:
            if prop == 'services':
                if self.services is None:
                    payload[prop] = None
                else:
                    payload[prop] = [s.get_payload() for s in self.services]
            elif prop == 'conditions':
                if self.conditions is None:
                    payload[prop] = None
                else:
                    payload[prop] = [c.get_payload() for c in self.conditions]
            else:
                payload[prop] = getattr(self, prop)
        return payload


class Condition(object):
    """Librato Alert Conditions class"""
    properties = {
        'above': (
            'metric_name',
            'source',
            'threshold',
            'summary_function',
            'duration',
            'detect_reset'
        ),
        'absent': (
            'metric_name',
            'source',
            'duration'       
        ),
        'below': (
            'metric_name',
            'source',
            'threshold',
            'summary_function',
            'duration',
            'detect_reset'
        )
    }

    def __init__(self, connection, *args, **kwargs):
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
        # if not hasattr(self, ''): self.version = 2
        for prop in self.properties[self.type]:
            if not hasattr(self, prop): setattr(self, prop, None)

    def get_payload(self):
        payload = {}
        payload['type'] = self.type
        for prop in self.properties[self.type]:
            payload[prop] = getattr(self, prop)
        return payload
