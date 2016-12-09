from flask import Flask, render_template
from OSC import OSCClient, OSCMessage
import csnd6

app = Flask(__name__)

@app.route("/")
def index():
	# requests.post("http://127.0.0.1", data=6)
	return "6";

@app.route("/csound")
def csound():
	return "8";

if __name__ == "__main__":
	app.run(debug='true')




# client = OSCClient()
# client.connect( ("localhost", 5000) )

# client.send( OSCMessage("/csound", "6" ) )
# # client.send( OSCMessage("/user/2", [2.0, 3.0, 4.0 ] ) )
# # client.send( OSCMessage("/user/3", [2.0, 3.0, 3.1 ] ) )
# # client.send( OSCMessage("/user/4", [3.2, 3.4, 6.0 ] ) )

# client.send( OSCMessage("/quit") )