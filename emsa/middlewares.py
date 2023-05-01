from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
import time

class AMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
        print("One time A Initialization")

    def __call__(self,request):
        print("This is A before view")
        response=self.get_response(request)
        print("this is A after view")
        return response
    
class BMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
        print("One time B Initialization")

    def __call__(self,request):
        print("This is B before view")
        response=self.get_response(request)
        print("this is B after view")
        return response
class CMiddleware:
    def __init__(self,get_response):
        self.get_response=get_response
        print("One time C Initialization")

    def __call__(self,request):
        print("This is C before view")
        response=self.get_response(request)
        print("this is C after view")
        return response
    
    

class MyProcessMiddleware:
    def __init__(self,get_response):
        print("One time initialization")
        self.get_response=get_response

    def __call__(self,request):
        response=self.get_response(request)
        return response
    
    def process_view(request,*args,**kwargs):
        print("This is Process View- Before View")
        return HttpResponse("This is before View")
        # return None

class MyExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except ZeroDivisionError as e:
            response = self.handle_exception(request, e)
        return response

    def handle_exception(self, request, exception):
        # Handle the exception and return a response
        return HttpResponse("Oops! Something went wrong.")    
class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        duration = end_time - start_time
        print(start_time)
        print(end_time)
        print(f"Request to {request.path} took {duration:.2f} seconds")
        return response
    


class CustomViewMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/login/':
            response = self.process_request(request)
            if response is None:
                response = self.get_response(request)
            response = self.process_response(request, response)
            return response
        else:
            return self.get_response(request)

    def process_request(self, request):
        
        pass

    def process_response(self, request, response):
        pass
