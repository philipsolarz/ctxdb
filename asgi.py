from ctxdb.server.api import api

if __name__ == "__main__":

    import uvicorn
    uvicorn.run(api, host="0.0.0.0", port=8000)