from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def compare_strings():
    s1 = s2 = ""
    result = []
    summary = ""

    if request.method == "POST":
        s1 = request.form.get("string1", "")
        s2 = request.form.get("string2", "")

        max_len = max(len(s1), len(s2))

        match = True
        for i in range(max_len):
            c1 = s1[i] if i < len(s1) else ""
            c2 = s2[i] if i < len(s2) else ""

            equal = c1 == c2
            if not equal:
                match = False

            result.append({
                "c1": c1,
                "c2": c2,
                "ascii1": ord(c1) if c1 else "",
                "ascii2": ord(c2) if c2 else "",
                "hex1": hex(ord(c1)) if c1 else "",
                "hex2": hex(ord(c2)) if c2 else "",
                "equal": equal
            })

        summary = "Strings Match ✅" if match else "Strings Do Not Match ❌"

    return render_template("index.html", result=result, s1=s1, s2=s2, summary=summary)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")