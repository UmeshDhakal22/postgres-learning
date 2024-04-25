from fastapi import FastAPI, Query
import uvicorn
from fastapi.responses import JSONResponse
from typing import Optional
from dotenv import load_dotenv

from start import DatabaseMaker

load_dotenv()

app = FastAPI()


@app.get("/issues", response_class=JSONResponse)
async def get_issues(
    ward: Optional[str] = Query(None, title="ward"),
    bbox: tuple = Query(None, title="bbox"),
    tags: str = Query(None, title="tags"),
):
    maker = DatabaseMaker(ward=ward, bbox=bbox, tags=tags)
    try:
        maker.create_project_table()
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    return JSONResponse(content={"message": "Project table created successfully."})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8009, workers=8)
