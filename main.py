from flask import Flask, render_template, request
import whois
import validators
import dns.resolver
from email_validator import validate_email, EmailNotValidError
from datetime import datetime

app = Flask(__name__)


# ------------------------------
# Helper: format WHOIS dates
# ------------------------------
def format_date(value):
    if isinstance(value, list):
        value = value[0]
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    return value


@app.route("/", methods=["GET", "POST"])
def compare_strings():
    s1 = s2 = ""
    result = []
    summary = ""
    domain_info = None
    email_info = None

    if request.method == "POST":
        s1 = request.form.get("string1", "").strip()
        s2 = request.form.get("string2", "").strip()

        input_value = s1
        domain_to_check = None

        # =====================================================
        # 1️⃣ EMAIL CHECK
        # =====================================================
        try:
            valid = validate_email(input_value)
            domain_to_check = valid.domain

            email_info = {
                "email": valid.email,
                "domain": domain_to_check,
                "valid": True
            }

        except EmailNotValidError:
            email_info = None

        # =====================================================
        # 2️⃣ DOMAIN CHECK (if not email)
        # =====================================================
        if not domain_to_check and validators.domain(input_value):
            domain_to_check = input_value

        # =====================================================
        # 3️⃣ DOMAIN INTELLIGENCE (MAX INFO)
        # =====================================================
        if domain_to_check:

            domain_info = {
                "domain": domain_to_check
            }

            # ---------- MX RECORDS ----------
            try:
                answers = dns.resolver.resolve(domain_to_check, 'MX')
                mx_records = sorted(
                    [(r.preference, r.exchange.to_text()) for r in answers]
                )
                domain_info["mx_found"] = True
                domain_info["mx_records"] = mx_records
            except Exception:
                domain_info["mx_found"] = False
                domain_info["mx_records"] = []

            # ---------- A RECORDS (IP) ----------
            try:
                a_records = dns.resolver.resolve(domain_to_check, 'A')
                domain_info["ip_addresses"] = [r.to_text() for r in a_records]
            except Exception:
                domain_info["ip_addresses"] = []

            # ---------- TXT RECORDS ----------
            try:
                txt_records = dns.resolver.resolve(domain_to_check, 'TXT')
                domain_info["txt_records"] = [r.to_text() for r in txt_records]
            except Exception:
                domain_info["txt_records"] = []

            # ---------- DMARC ----------
            try:
                dmarc_records = dns.resolver.resolve(f"_dmarc.{domain_to_check}", 'TXT')
                domain_info["dmarc"] = [r.to_text() for r in dmarc_records]
            except Exception:
                domain_info["dmarc"] = []

            # ---------- WHOIS ----------
            try:
                w = whois.whois(domain_to_check)

                domain_info.update({
                    "registrar": w.registrar,
                    "creation_date": format_date(w.creation_date),
                    "expiration_date": format_date(w.expiration_date),
                    "updated_date": format_date(getattr(w, "updated_date", None)),
                    "name_servers": w.name_servers,
                    "status": w.status,
                    "owner": getattr(w, "name", None)
                             or getattr(w, "org", None)
                             or "Not available"
                })

            except Exception as e:
                domain_info["whois_error"] = str(e)

        # =====================================================
        # 4️⃣ STRING COMPARISON
        # =====================================================
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
                "unicode1": f"U+{ord(c1):04X}" if c1 else "",
                "unicode2": f"U+{ord(c2):04X}" if c2 else "",
                "equal": equal
            })

        summary = "Strings Match ✅" if match else "Strings Do Not Match ❌"

    return render_template(
        "index.html",
        result=result,
        s1=s1,
        s2=s2,
        summary=summary,
        domain_info=domain_info,
        email_info=email_info
    )


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=4999)