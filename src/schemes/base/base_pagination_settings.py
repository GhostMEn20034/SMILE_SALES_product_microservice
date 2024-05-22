from pydantic import conint


class BasePaginationSettings:
    def __init__(self, page: conint(ge=0) = 1,
                 page_size: conint(ge=0) = 20,):
        self.page = page
        self.page_size = page_size
