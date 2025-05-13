from fastapi import FastAPI, Request
from fastapi_mcp import FastApiMCP

app = FastAPI()

mcp = FastApiMCP(app)

# Mount it to /mcp
mcp.mount()


@app.get("/sales-report")
def get_sales_report():
    with open("data/sales_report.txt") as f:
        return {"report": f.read()}


@app.get("/support-report")
def get_support_report():
    with open("data/support_report.txt") as f:
        return {"report": f.read()}


@app.get("/ops-report")
def get_ops_report():
    with open("data/ops_report.txt") as f:
        return {"report": f.read()}
