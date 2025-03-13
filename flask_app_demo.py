from flask import Flask
from flask import request
from flask import render_template
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

@app.route("/")
def main():
    if request.method == "GET":
        a = request.args.get("a")
        b = request.args.get("b")
        if a and b:
            x = np.linspace(int(a), int(b), 100)
            y = np.sin(x)
            plt.plot(x, y)
            plt.savefig("static/result.png")
            plt.close()

            return render_template('results.html', answer = int(a) + int(b))
        else:
            return render_template('main.html')
