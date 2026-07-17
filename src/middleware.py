from fastapi import FastAPI, Request, status
import time
import logging
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# disabling uvicorn default logging
logger = logging.getLogger('uvicorn.access')
logger.disabled=True

def register_all_middleware(app:FastAPI):
    @app.middleware('http')
    async def custom_logging(request:Request,call_next):
        # Everything that needs to be done with the request
        start_time = time.time()

        response = await call_next(request)
        # Everything that needs to be done with thre response
        processing_time = time.time() - start_time

        message = f"{request.client.host}:{request.client.port} - {request.method} - {request.url.path} - {response.status_code} completed after {processing_time}s"
        print(message)

        return response

    # check aut authorization header, although already done via dependency
#     @app.middleware('http')
#     async def authorization(request:Request,call_next):
#         if not "Authorization" in request.headers:
# #             cannot raise exception in middleware, it will be raised but not be returned as a response.
#             return JSONResponse(
#                 content = {
#                     "message":"Unauthorized",
#                     "resolution":"please provide the right credentials to proceed"
#                 },
#                 status_code = status.HTTP_401_UNAUTHORIZED
#             )
#         response = await call_next(request)
#
#         return response

#     ASGI = Asynchronous Server Gateway Interface
# fastsapi is built on top of ASGI, in any middleware that can be used with asgi can work with fastapi

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost","127.0.0.1","bookly-whg8.onrender.com"]
    )
