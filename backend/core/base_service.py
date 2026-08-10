"""
TERATAI Base Service
"""

class BaseService:

    SERVICE_NAME = "Base Service"
    SERVICE_VERSION = "1.0.0"

    def __init__(self):

        self.ready = False

    # ==============================

    def initialize(self):

        self.load()

        self.ready = True

    # ==============================

    def load(self):

        raise NotImplementedError

    # ==============================

    def reload(self):

        self.clear_cache()

        self.load()

    # ==============================

    def clear_cache(self):

        pass

    # ==============================

    def shutdown(self):

        self.clear_cache()

        self.ready = False

    # ==============================

    def statistics(self):

        return {}