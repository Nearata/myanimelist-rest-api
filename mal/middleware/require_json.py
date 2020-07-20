from falcon import HTTPNotAcceptable


class RequireJSON:
    def process_request(self, request, response):
        if not request.client_accepts_json:
            raise HTTPNotAcceptable("This API only supports responses encoded as JSON.")
