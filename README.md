# Supplier Follow-up Assistant

A lightweight Streamlit prototype for e-commerce and product launch teams working with suppliers.

## What it does

- extracts key commercial and production information from a supplier conversation;
- shows launch readiness;
- highlights open items and launch risks;
- creates recommended next actions;
- prepares a ready-to-send supplier follow-up.

## Demo

The repository contains a sample supplier conversation so the workflow can be tested immediately.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Prototype scope

This version demonstrates the workflow and interface without requiring external API credentials. It can later be extended with an LLM, multilingual supplier chats, persistent SKU tracking and integrations with CRM/task-management systems.
