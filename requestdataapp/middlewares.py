from django.http import HttpRequest, HttpResponseForbidden
import datetime

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

class Throttling:
    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_dict=dict()
        self.date_time=datetime.datetime.now()
        self.time_between = 0
        
    def __call__(self, request: HttpRequest):
        IP_client=request.META["REMOTE_ADDR"]
        if  IP_client in self.ip_dict:
            self.date_time = self.ip_dict[IP_client]

        self.ip_dict[IP_client]=datetime.datetime.now()
        
        print("IP client",IP_client)
        print("Last date", self.ip_dict[IP_client])
        self.time_between=int(self.ip_dict[IP_client].timestamp())-int(self.date_time.timestamp())
        print("time between requests, sec", self.time_between)

        if self.time_between < 10:
            return HttpResponseForbidden()
       
        response = self.get_response(request)

        return response