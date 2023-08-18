class DecodeEncodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('INPUT:', request.body)
        print('INPUT:', request.META)

        response = self.get_response(request)

        print('OUTPUT:', response.data)

        return response
