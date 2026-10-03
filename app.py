import re
import streamlit as st

st.set_page_config(
    page_title="Supplier Follow-up Assistant",
    page_icon="📦",
    layout="wide",
)

SAMPLE = """Supplier: Hello, price is USD 4.80/pc for 1000 pcs. MOQ 1000 pcs. Sample can be ready in 5 days. Mass production takes around 25-30 days after deposit. We can make black and white. Custom logo is possible but packaging artwork is needed. Wireless charging version is still under testing.
Buyer: Please confirm packaging cost, certification, final sample date and whether the logo is included in the quoted price.
Supplier: Logo is included. Packaging cost I need to check with my colleague. We have CE report. I will confirm sample date tomorrow."""

def first(pattern, text, default="Not confirmed"):
    m = re.search(pattern, text, re.I | re.S)
    return m.group(1).strip() if m else default

def analyze(text):
    price = first(r"(USD\s*\d+(?:\.\d+)?\s*/?\s*(?:pc|pcs|piece)?)", text)
    moq = first(r"MOQ\s*(?:is|:)?\s*(\d+)", text)
    sample = first(r"sample(?:\s+\w+){0,4}\s+(?:in|within)\s+(\d+\s+days?)", text)
    lead = first(r"(?:mass\s+production|production)(?:\s+\w+){0,5}\s+(?:around\s+)?(\d+\s*[-–]\s*\d+\s+days?|\d+\s+days?)", text)
    colors = []
    low = text.lower()
    for c in ["black", "white", "blue", "red", "green", "silver", "gold"]:
        if c in low:
            colors.append(c.title())
    certification = "CE report mentioned" if re.search(r"\bCE\b", text, re.I) else "Not confirmed"

    risks = []
    if re.search(r"packaging cost.*(?:check|confirm|unknown|tbd)", text, re.I | re.S):
        risks.append(("Packaging", "Confirm final packaging cost and artwork requirements", "Open"))
    if "certif" in low or re.search(r"\bCE\b", text, re.I):
        risks.append(("Compliance", "Verify certification documents and market applicability", "Review"))
    if re.search(r"confirm sample date|sample date tomorrow|final sample date", text, re.I):
        risks.append(("Sample", "Confirm exact sample completion / shipment date", "Open"))
    if re.search(r"under testing|still testing|not final", text, re.I):
        risks.append(("Product", "Feature/version is still under testing and may affect launch timing", "Risk"))
    if not risks:
        risks.append(("General", "No obvious open items detected. Manual review recommended.", "Review"))

    readiness = "ACTION REQUIRED" if any(x[2] in ("Open", "Risk") for x in risks) else "REVIEW"
    return {
        "price": price,
        "moq": moq,
        "sample": sample,
        "lead": lead,
        "colors": ", ".join(colors) if colors else "Not confirmed",
        "cert": certification,
        "risks": risks,
        "readiness": readiness,
    }

def make_followup(data):
    questions = []
    labels = [r[0] for r in data["risks"]]
    if "Packaging" in labels:
        questions.append("confirm the final packaging cost and required artwork/specifications")
    if "Compliance" in labels:
        questions.append("share the available certification documents and confirm their applicability to the target market")
    if "Sample" in labels:
        questions.append("confirm the exact sample completion and shipment date")
    if "Product" in labels:
        questions.append("confirm the testing status and expected release date of the version currently under testing")
    if not questions:
        questions.append("confirm that the quoted commercial and production conditions remain valid")

    bullets = "\n".join(f"{i+1}. Please {q}." for i, q in enumerate(questions))
    return f"""Hi,

Thank you for the update. To keep the product launch on schedule, could you please help us close the following points:

{bullets}

Current information on our side:
- Price: {data['price']}
- MOQ: {data['moq']}
- Sample lead time: {data['sample']}
- Mass production lead time: {data['lead']}

Please let us know if any of these points may affect the current timeline.

Thank you!"""

st.title("📦 Supplier Follow-up Assistant")
st.caption("Turn supplier chats into a clear launch status, risks and a ready-to-send follow-up.")

with st.sidebar:
    st.subheader("Prototype scope")
    st.write(
        "Converts supplier communication into structured launch data, "
        "highlights missing information and risks, and prepares follow-up actions."
    )
    st.divider()
    st.caption("Designed for e-commerce and product launch workflows.")

text = st.text_area(
    "Paste supplier chat / email",
    value=SAMPLE,
    height=260,
    help="Paste an English supplier conversation or email thread.",
)

if st.button("Analyze supplier conversation", type="primary", use_container_width=False):
    st.session_state["analysis"] = analyze(text)

if "analysis" in st.session_state:
    d = st.session_state["analysis"]

    st.divider()
    status_col, note_col = st.columns([1, 3])
    with status_col:
        st.caption("LAUNCH READINESS")
        if d["readiness"] == "ACTION REQUIRED":
            st.error("⚠️ ACTION REQUIRED")
        else:
            st.info("REVIEW")
    with note_col:
        st.caption("DECISION SUPPORT")
        st.write("Close the open items below before confirming the launch timeline.")

    st.subheader("Launch snapshot")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Quoted price", d["price"])
    c2.metric("MOQ", d["moq"])
    c3.metric("Sample lead time", d["sample"])
    c4.metric("Production lead time", d["lead"])

    c5, c6 = st.columns(2)
    c5.write(f"**Available colors:** {d['colors']}")
    c6.write(f"**Certification:** {d['cert']}")

    st.subheader("Open items & risks")
    for category, item, status in d["risks"]:
        if status == "Risk":
            st.error(f"**{category} · {status}**  \n{item}")
        elif status == "Open":
            st.warning(f"**{category} · {status}**  \n{item}")
        else:
            st.info(f"**{category} · {status}**  \n{item}")

    st.subheader("Recommended next actions")
    for i, (category, item, status) in enumerate(d["risks"], 1):
        st.write(f"**{i}. {category}:** {item}")

    st.subheader("Ready-to-send supplier follow-up")
    followup = make_followup(d)
    st.text_area("Follow-up draft", followup, height=320)
    st.download_button(
        "Download follow-up as TXT",
        data=followup,
        file_name="supplier_followup.txt",
        mime="text/plain",
    )

    st.caption("Prototype output should be reviewed by the responsible product or sourcing manager before sending.")
