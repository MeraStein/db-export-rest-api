from fastapi import FastAPI
from export_db import export_users
from config import HOST, PORT

app = FastAPI()

@app.post("/export")
def run_export():
    result = export_users()
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT, reload=False)
