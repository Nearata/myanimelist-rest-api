from falcon import HTTPNotAcceptable, Request, Response


class RequireJSON:
    def process_request(self, request: Request, response: Response) -> None:
        if not request.client_accepts_json:
            raise HTTPNotAcceptable("This API only supports responses encoded as JSON.")
