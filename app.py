from dotenv import load_dotenv

from flask import Flask, render_template, request, jsonify
from ice_breaker import ice_break_with

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    summary, profile_pic_url = ice_break_with(name=name)
    return jsonify(
        {
            "summary_and_facts": summary.to_dict(),
            "picture_url": profile_pic_url,
        }
    )



if __name__ == "__main__":
    #Printing the output of the process function
    with app.test_client() as client:
        response = client.post("/process", data={"name": "Kharisma Rizki Wijanarko"})
        print(response.get_json())
    app.run(host="0.0.0.0", debug=True)