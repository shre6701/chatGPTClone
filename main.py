from flask import Flask, render_template, jsonify, request
from flask_pymongo import PyMongo
import openai

# openai.api_key = "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"




app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/chatgpt"
mongo = PyMongo(app)

@app.route("/")
def home():
    chats = mongo.db.chats.find({})
    myChats = [chat for chat in chats]
    print(myChats)
    return render_template("index.html", myChats= myChats)

@app.route("/api", methods=["GET", "POST"])
def qa():
    if request.method == "POST":
        print(request.json)
        question = request.json.get("question")
        chat = mongo.db.chats.find_one({"question": question})
        print(chat)
        if chat:
            data = {"question":question, "answer": f"{chat['answer']}"}
            return jsonify(data)
        else:
            
            response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k",
                    messages= question,
                    temperature=1,
                    max_tokens=256,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    )
            print(response)
            data = {{"question": question, "answer":response["choices"][0]["text"]}}
            mongo.db.chats.insert_one({"question": question, "answer":response})
            return jsonify(data)
    data = {"result": "Hello! It seems like your message might have been cut off. How can I assist you today?"} 
    
    return jsonify(data) 
   



app.run(debug=True)