import sys
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/add")
def add(x, y):
    """ Add function. """
    return float(x) + float(y)

@app.get("/subtract")
def subtract(x, y):
    """ Subtract function. """
    return float(x) - float(y)

@app.get("/")
def root():
    """ root. """
    return "This is the calculator app"

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=9321)

    """operation = sys.argv[1]
    x = int(sys.argv[2])
    y = float(sys.argv[3])
    #print(f"x:{x}, y:{y}")
    print(f"value={add(x, y)}")"""


"""
x = 5
y = 10.5
# z = add(x, y)
print(add(x, y))
"""
