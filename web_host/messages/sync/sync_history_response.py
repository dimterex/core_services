from web_host.messages.base_response import BaseResponse


class SyncHistoryResponse(BaseResponse):
    def __init__(self, status: str, items: any = None,  exception: str = None):
        super().__init__(status, exception)
        self.items = items

    def serialize(self) -> dict:
        return {
            'status': self.status,
            'items': self.items,
            'exception': self.exception,
        }
