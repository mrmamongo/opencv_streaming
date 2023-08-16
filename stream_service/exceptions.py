class DisposeException(Exception):
    pass


class StartServerException(Exception):
    @property
    def message(self) -> str:
        return "HTTP server failed to start"
