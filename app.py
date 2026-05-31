
from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import re

app = Flask(__name__)

SKILLS = ["python","java","sql","html","css","javascript","react","flask","django","aws","docker","git","machine learning","data analysis"]

def extract_text(pdf):
    text=""
    reader=PdfReader(pdf)
    for p in reader.pages:
        text += p.extract_text() or ""
    return text

@app.route("/", methods=["GET","POST"])
def index():
    result=None
    if request.method=="POST":
        pdf=request.files["resume"]
        text=extract_text(pdf)

        email = re.findall(r'\S+@\S+', text)
        phone = re.findall(r'\+?\d[\d\s-]{8,}', text)

        found=[s for s in SKILLS if s.lower() in text.lower()]
        missing=[s for s in SKILLS if s.lower() not in text.lower()]
        score=int((len(found)/len(SKILLS))*100)

        result={
            "email": email[0] if email else "Not Found",
            "phone": phone[0] if phone else "Not Found",
            "skills": found,
            "missing": missing,
            "score": score
        }

    return render_template("index.html", result=result)

if __name__=="__main__":
    app.run(debug=True)
