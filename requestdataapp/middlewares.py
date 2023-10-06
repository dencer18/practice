from datetime import datetime, timedelta
from http import HTTPStatus
from django.http import HttpRequest, HttpResponse

def setup_user_agent_on_request_middleware(get_response):
    print("Initial call")
    def middleware(request: HttpRequest):
        print("before get response")
        request.user_agent = request.META["HTTP_USER_AGENT"]
        response = get_response(request)
        print("after get response")
        return response

    return middleware

class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("Requests count", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("Responses count", self.responses_count)
        return response
    
    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print("got", self.exceptions_count, "exceptions so far")

THROTTLING_RATE_MS = 1500

class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.bucket: dict[str, datetime] = {}
        self.rate_ms = THROTTLING_RATE_MS

    @classmethod
    def get_client_ip(cls, request: HttpRequest):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    def request_is_allowed(self, client_ip: str) -> bool:
        now = datetime.utcnow()
        last_access = self.bucket.get(client_ip)
        if not last_access:
            return True
        if (now - last_access) > timedelta(milliseconds=self.rate_ms):
            return True

        return False

    def __call__(self, request: HttpRequest):
        client_ip = self.get_client_ip(request)
        if self.request_is_allowed(client_ip):
            response = self.get_response(request)
            self.bucket[client_ip] = datetime.utcnow()
        else:
            response = HttpResponse("Rate limit exceeded", status=HTTPStatus.TOO_MANY_REQUESTS)
        return response