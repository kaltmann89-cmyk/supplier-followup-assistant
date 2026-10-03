import streamlit as st
import re

st.set_page_config(page_title='Supplier Follow-up Assistant', page_icon='📦', layout='wide')
st.title('📦 Supplier Follow-up Assistant')
st.caption('Turn supplier chats into a clear launch status, risks and a ready-to-send follow-up.')

sample = '''Supplier: Hello, price is USD 4.80/pc for 1000 pcs. MOQ 1000 pcs. Sample can be ready in 5 days. Mass production takes around 25-30 days after deposit. We can make black and white. Custom logo is possible but packaging artwork is needed. Wireless charging version is still under testing.\nBuyer: Please confirm packaging cost, certification, final sample date and whether the logo is included in the quoted price.\nSupplier: Logo is included. Packaging cost I need to check with my colleague. We have CE report. I will confirm sample date tomorrow.'''

text = st.text_area('Paste supplier chat / email', value=sample, height=260)

if st.button('Analyze supplier conversation', type='primary'):
    low=text.lower()
    price=re.search(r'(?:usd|\$)\s?([0-9]+(?:\.[0-9]+)?)', low)
    moq=re.search(r'moq\s*(?:is|:)?\s*([0-9,]+)', low)
    lead=re.search(r'(\d+\s*(?:-|–|to)\s*\d+\s*days|\d+\s*days)', low)
    colors=[]
    for c in ['black','white','blue','red','green','silver','gold']:
        if c in low: colors.append(c.title())

    c1,c2=st.columns(2)
    with c1:
        st.subheader('Launch snapshot')
        st.metric('Quoted price', f"USD {price.group(1)} / pc" if price else 'Not confirmed')
        st.metric('MOQ', moq.group(1) if moq else 'Not confirmed')
        st.write('**Lead time:**', lead.group(1) if lead else 'Not confirmed')
        st.write('**Colors mentioned:**', ', '.join(colors) if colors else 'Not specified')
        st.write('**Custom logo:**', 'Mentioned / available' if 'logo' in low else 'Not confirmed')
    with c2:
        st.subheader('Open items & risks')
        items=[]
        if 'packaging' in low: items.append('Confirm final packaging cost / artwork requirements')
        if 'certif' in low or ' ce ' in f' {low} ': items.append('Verify certification documents and applicability')
        if 'sample' in low: items.append('Confirm exact sample completion / shipment date')
        if 'testing' in low: items.append('Feature still under testing — potential launch risk')
        if not items: items=['Confirm price, MOQ, lead time, sample timing and compliance documents']
        for i in items: st.warning(i)

    st.subheader('Suggested next actions')
    actions=[
        'Get written confirmation of final commercial terms.',
        'Lock the sample completion and shipment date.',
        'Collect packaging requirements and final artwork deadline.',
        'Request certification / quality evidence before production approval.',
        'Track unresolved product features separately and escalate schedule risk early.'
    ]
    for n,a in enumerate(actions,1): st.write(f'{n}. {a}')

    st.subheader('Ready-to-send follow-up')
    follow='''Hi! Thanks for the update. To keep the launch on schedule, could you please confirm the following outstanding points:\n\n1. Final packaging cost and artwork requirements.\n2. Exact sample completion / shipment date.\n3. Available certification documents.\n4. Current status and expected completion date of the feature still under testing.\n5. Confirmation that the quoted price includes the custom logo.\n\nPlease send the available documents/photos together with your confirmation. Thank you!'''
    st.code(follow, language=None)

with st.sidebar:
    st.header('Why this prototype')
    st.write('Designed for product launch teams working with factories and suppliers.')
    st.write('It demonstrates workflow thinking: extracting facts, spotting missing information, surfacing risks and preparing follow-ups.')
    st.info('Demo version uses lightweight rule-based extraction so it runs without API keys. An LLM can be connected later for multilingual chats and deeper analysis.')
