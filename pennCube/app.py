from flask import Flask, render_template, redirect, url_for, request
from flask import make_response
app = Flask(__name__)
import pennCube, pennCubeSat
import json

# maybe wrong
py_to_js_move = [
    [3, False], # A+
    [3, True], # A-
    [3, True, 2, False], # B+
    [3, False, 2, True], # B-
    [2, True], # C+
    [2, False], # C-
    [4, False], # D+
    [4, True], # D-
    [4, True, 5, False], # E+
    [4, False, 5, True], # E-
    [5, True], # F+
    [5, False], # F-
    [0, False], # IV+ (assuming + means go down)
    [0, True], # IV-
    [0, True, 1, False], # V+
    [0, False, 1, True], # V-
    [1, True], # VI+
    [1, False], # VI-
]

# maybe have to shift this one due to gecis being 1-indexed
py_to_js_squares = [
    36,37,38,39,40,41,42,43,44,
    0,1,2,18,19,20,9,10,11,27,28,29,
    3,4,5,21,22,23,12,13,14,30,31,32,
    6,7,8,24,25,26,15,16,17,33,34,35,
    45,46,47,48,49,50,51,52,53,54
]

def solve(squares, alg):
    i = 1
    if alg == 'MIP':
        while True:
            testSolver = pennCube.cubeSolver(squares, i)
            soln = testSolver.solve()
            if soln is None:
                i += 1
                continue
            print(soln)
            return soln
    else:
         while True:
            try:
                testSolver = pennCubeSat.cubeSolver(squares, i)
                soln = testSolver.solve()
                print(soln)
                return soln
            except ValueError:
                i += 1
        
        

@app.route('/solve', methods=['GET', 'POST'])
def solve_route():
   message = None
   if request.method == 'POST':
        js_data = json.loads(request.form['cube'])
        js_alg = json.loads(request.form['alg'])
        print(js_data)
        print(js_alg)
        data = [int(js_data[py_to_js_squares[i]]) + 1 for i in range(54)]
        print(data)
        result = str([py_to_js_move[i[1]] for i in solve(data, js_alg)]).replace('T', 't').replace('F', 'f')
        print(result)

        resp = make_response('{"response": '+result+'}')
        resp.headers['Content-Type'] = "application/json"
        resp.headers['Access-Control-Allow-Origin'] = "*"
        return resp

if __name__ == "__main__":
    app.run(debug = True)