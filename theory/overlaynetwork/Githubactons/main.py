from fastapi import FastAPI
app = FastAPI()
import uvicorn

@app.get("/")
def read_root():
    return dict(
        name="Mayank Thakur",
        sapid="500123412",
        Location="Dehradun"
    )

@app.get("/{data}")
def read_data(data):
    return dict(hi=data, Location="Dehradun")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)
