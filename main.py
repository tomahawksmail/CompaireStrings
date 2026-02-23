from flask import Flask, render_template, request
import whois
import validators


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def compare_strings():
    s1 = s2 = ""
    result = []
    summary = ""
    domain_info = None

    if request.method == "POST":
        s1 = request.form.get("string1", "")
        s2 = request.form.get("string2", "")

        # --- Check if input is a valid domain ---
        if validators.domain(s1):
            try:
                w = whois.whois(s1)
                domain_info = {
                    "domain": s1,
                    "registrar": w.registrar,
                    "creation_date": (w.creation_date[0].strftime("%Y-%m-%d") if w.creation_date[0] else "N/A"),
                    "expiration_date": (w.expiration_date[0].strftime("%Y-%m-%d") if w.expiration_date[0] else "N/A"),
                    "owner": getattr(w, "name", "Not available")
                }
            except Exception as e:
                domain_info = {"error": f"Could not fetch WHOIS info: {e}"}
            else:
                domain_info = "Could not fetch WHOIS info"
        # --- Compare strings character by character ---
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

    return render_template("index.html", result=result, s1=s1, s2=s2,
                           summary=summary, domain_info=domain_info)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=4999)