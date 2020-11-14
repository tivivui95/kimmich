from flask import Flask, request, redirect, url_for, render_template, json

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def control_panel():
    if request.method == 'POST':
        if request.form['button'] == 'button-play':
            print("play button pressed")

        elif request.form['button'] == 'button-exit':
            print("exit button pressed")

        elif request.form['slider']:
            volume = request.form['slider']
            return json.dumps({'volume': volume})
            print(volume)

    return render_template('timxungquanh.html')

if __name__ == '__main__':
    app.run(debug=True)