import time

from expiringdict import ExpiringDict
from fastapi import HTTPException, Request
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

MAX_DATA_SIZE = 85


class RateLimiter:
    def __init__(
        self,
        times: int = 1,
        seconds: int = 0,
        minutes: int = 0,
        hours: int = 0,
        days: int = 0,
    ) -> None:
        self.times = times
        self.seconds = seconds + minutes * 60 + hours * 3600 + days * 86400
        self.data = ExpiringDict(1, self.seconds + 1)

    async def default_identifier(self, request: Request):
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0]
        else:
            ip = request.client.host
        return ip

    async def check(self, request: Request) -> bool:
        ip = await self.default_identifier(request)
        current_time = int(time.time())
        key = f"{ip}-{current_time}"

        if key in self.data:
            self.data[key] += 1
        else:
            self.data[key] = 1

        key_check = [f"{ip}-{current_time - x}" for x in range(self.seconds)]
        tot_req = sum(
            dict(filter(lambda x: x[0] in key_check, self.data.items())).values()
        )

        return tot_req > self.times

    async def __call__(self, request: Request):
        if len(self.data) > (self.data.max_len * (MAX_DATA_SIZE / 100)):
            self.data.max_len *= 2

        if await self.check(request):
            raise HTTPException(HTTP_429_TOO_MANY_REQUESTS, "Too Many Requests")
