from fastapi import FastAPI, Request
from fastapi_mcp import FastApiMCP


app = FastAPI()

# MCP server auto-generation
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


@app.post("/search-kpi")
async def search_kpi(request: Request):
    body = await request.json()
    kpi = body.get("kpi", "").lower()

    # דוגמה פשוטה – תחזירי תוצאה לפי מילות מפתח
    if "conversion" in kpi:
        return {"matches": [
            "New A/B tested landing page boosted conversions by 8%.",
            "Conversion from landing page remained stable at 2.5%."
        ]}
    else:
        return {"matches": [f"No results found for KPI: {kpi}"]}
