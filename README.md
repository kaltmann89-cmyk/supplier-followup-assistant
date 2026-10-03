# Supplier Follow-up Assistant

A lightweight prototype for e-commerce / product launch teams working with factories.

## What it does
- extracts price, MOQ, lead-time and basic product facts from supplier messages;
- highlights unresolved questions and launch risks;
- suggests next actions;
- generates a concise supplier follow-up message.

The demo deliberately runs without an API key. It uses simple extraction rules; an LLM can later be connected for Chinese/English/Russian conversations, richer entity extraction and persistent launch trackers.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Publish
Upload these files to a GitHub repository and deploy the repository with Streamlit Community Cloud. Then paste the public app URL into the application form.
