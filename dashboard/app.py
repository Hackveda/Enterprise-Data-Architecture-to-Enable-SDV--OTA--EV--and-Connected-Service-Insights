import time
import pandas as pd
import streamlit as st
import plotly.express as px
from src.simulator.live_simulator import EventSimulator

st.set_page_config(page_title='Enterprise Data Platform | Live', layout='wide')
st.title('Enterprise Data Platform — Live 1.6M+ Events/sec')
st.caption('Logical event-rate simulation + governed Snowflake marts architecture')

rps = st.sidebar.number_input('Simulated records/sec', min_value=1_600_000, value=1_800_000, step=100_000)
refresh = st.sidebar.slider('Refresh seconds', .5, 5.0, 1.0, .5)
if 'sim' not in st.session_state or st.session_state.get('rps') != rps:
    st.session_state.sim = EventSimulator(int(rps)); st.session_state.rps = rps; st.session_state.history=[]

sim=st.session_state.sim
row=sim.logical_tick(refresh)
st.session_state.history.append(row)
st.session_state.history=st.session_state.history[-60:]
h=pd.DataFrame(st.session_state.history)

c1,c2,c3,c4=st.columns(4)
c1.metric('Event rate', f"{row['rps']/1e6:.2f}M/s")
c2.metric('Orders / tick', f"{row['order_created']:,}")
c3.metric('Revenue / tick', f"₹{row['gross_revenue']/1e6:.1f}M")
c4.metric('P95 pipeline latency', f"{row['p95_event_latency_ms']} ms")

st.plotly_chart(px.line(h, x='ts', y=['page_view','search','add_to_cart','order_created'], title='Live event mix'), use_container_width=True)

team=st.selectbox('Governed data mart', ['MARKETING','SALES','FINANCE','SUPPORT'])
if team=='MARKETING':
    data=pd.DataFrame({'KPI':['Impressions','Sessions','Conversions','ROAS'],'Value':[row['page_view'],row['search']+row['add_to_cart'],row['order_created'],4.7]})
elif team=='SALES':
    data=pd.DataFrame({'KPI':['Orders','Payment Auth','Gross Revenue','Payment Success %'],'Value':[row['order_created'],row['payment_authorized'],row['gross_revenue'],row['payment_success_rate']]})
elif team=='FINANCE':
    data=pd.DataFrame({'KPI':['Gross Revenue','Estimated COGS','Estimated Fees','Net Contribution'],'Value':[row['gross_revenue'],row['gross_revenue']*.62,row['gross_revenue']*.025,row['gross_revenue']*.355]})
else:
    data=pd.DataFrame({'KPI':['Contacts','Open-like workload','P95 Response proxy','SLA health %'],'Value':[row['support_contact'],int(row['support_contact']*.18),row['p95_event_latency_ms'],96.8]})
st.dataframe(data, use_container_width=True, hide_index=True)

st.info('For production, point BI tools at ENTERPRISE_DATA.MARTS secure views/dynamic tables; do not query RAW directly.')
time.sleep(refresh)
st.rerun()
