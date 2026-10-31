from core.logger import setup_logger


class BaseService:
    """Base class for shared bot services."""

    def init(self, name="HariLabs"):
        self.name = name
        self.logger = setup_logger(name)

    def start(self):
        self.logger.info("%s service started", self.name)

    def stop(self):
        self.logger.info("%s service stopped", self.name)
