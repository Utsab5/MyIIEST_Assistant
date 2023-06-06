from flask import Flask , render_template, request, jsonify
import chatbot
app = Flask(__name__)

@app.route('/')
def index():
    # return 'Hello WorLD'
    return render_template('chat.html')

@app.route("/get" , methods=["GET","POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    output = getChatResponse(input)
    # print(output)
    return output

def getChatResponse(text):
    #import chatbot.py and get the output from chat(text)
    return chatbot.chat(text)


if __name__ == "__main__":
    app.run(debug=True)    