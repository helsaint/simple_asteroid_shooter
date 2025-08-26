class EventDispatcher:
    def __init__(self):
        self._listeners = {}

    def register_event(self, event_name, callback):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)

    def dispatch_event(self, event_name, data=None):
        for callback in self._listeners.get(event_name, []):
            callback(data)

# Global singleton instance if preferred
dispatcher = EventDispatcher()