import shutil
import subprocess

from fastapi import FastAPI, HTTPException
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

app: FastAPI = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI Scrapy integration"}


@app.post("/run-spider/{spider_name}")
async def run_spider(spider_name: str):
    # process = CrawlerProcess(get_project_settings())
    # await process.crawl(spider_name)
    # process.start()
    # return {"status:Success"}
    # Check if Scrapy is available
    if not shutil.which('scrapy'):
        raise HTTPException(status_code=500, detail="Scrapy not found in PATH")
    try:
        # Run Scrapy spider using subprocess
        process = subprocess.Popen(
            ['scrapy', 'crawl', spider_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = process.communicate()

        if process.returncode != 0:
            raise HTTPException(status_code=500, detail=stderr.decode())

        return {"status": "Scraping completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)