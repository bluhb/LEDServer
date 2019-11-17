from flask import Flask, render_template, redirect, request, jsonify
import time
import sys
import logging
import __main__


app = Flask(__name__)

# Disable request logging in terminal(doesn't matter in cpu usage that much for rpi 3b+)

# log = logging.getLogger('werkzeug')
# log.disabled = True



jsondata = {}
adata = {'color': '', 'wait': ''}
color_rgb = {'r':0,'g':0,'b':0}


@app.route('/')
def main():
    return redirect('/index', code=302)

@app.route('/index')
def hello():
	return render_template('index.html', page='home')

@app.route("/led")
def LED():
	return render_template('index.html',
		functdict=__main__.livingroom.functdict,
                color_rgb={'r':0,'g':0,'b':0},
		length=135,
		wait=1,
		page='led')

@app.route('/download')
def download():
    path = '../Database.json'
    return send_file(path, as_attachment = True)



@app.route("/led/<string:functions>")
def functions(functions):
	__main__.livingroom.function = str(functions)
	return redirect('/led', code=302)

@app.route("/led/<string:color>/<int:value>")
def colorcontrol(color, value):
        color_rgb[color] = int(value)
        __main__.livingroom.color_rgb = color_rgb
        return redirect('/led', code=302)

@app.route("/led/length/<int:value>")
def length(value):
	config.length = value
	return ('', 204)

@app.route("/led/wait/<float:value>")
def wait(value):
	__main__.livingroom.wait = value
	return redirect('/led', code=302)

@app.route("/led/brightness/<float:value>")
def brightness(value):
	config.brightness = value
	return ('', 204)


@app.route("/led/data")
def data():
	global jsondata
	try:
		jsondata['color'] = config.color_rgb
		jsondata['temp'] = config.temperature
		jsondata['wait'] = config.wait
		jsondata['cpu_load'] = config.cpu_load
		jsondata['roomTemp'] = config.roomTemp
		jsondata['roomHumid'] = config.roomHumid
		jsondata['roomLight'] = config.roomLDR
	except:
		for i in jsondata:
			jsondata[i] = 0
	return jsonify(jsondata), 200

@app.route("/led/arduino/<int:value>")
def arduino(value):
	global adata
	adata['led'] = config.color_rgb['b']
	return redirect('/led', code=302)

@app.route("/arduinodata")
def arduinodata():
	global adata
	adata['color'] = config.color_rgb_arduino
	adata['wait'] = config.wait
	return jsonify(adata), 200

@app.route("/color", methods=["POST"])
def JSONcolor():
        color_rgb = request.get_json(force=True)
        __main__.livingroom.color_rgb = color_rgb
        return ('', 204)
