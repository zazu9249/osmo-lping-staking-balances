import datetime as dt
from email.mime import image
import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
from dateutil import parser

theme_plotly = None

st.set_page_config(page_title='Osmosis - Analysis on Wallet Balances', page_icon= 'Images/osmo-logo.png', layout='wide')
st.title('Osmosis - Analysis on Wallet Balances')

st.image(Image.open('Images/OSMO-blockchain.png'))

st.subheader('What is Osmosis?')
st.write(
    """
    _The Osmosis automated market maker (AMM) affords users the ability to create new and unique liquidity pools that are controlled and voted on by participants. 
    The Osmosis token (OSMO) is used to vote, stake, and provide liquidity throughout its pools. Superfluid staking, a process novel to the Osmosis protocol, 
    allows users to stake assets to secure the network while simultaneously providing assets in a liquidity pool._

    **The Cosmos Ecosystem:**

    Osmosis is a decentralized exchange (DEX) and automated market maker (AMM) protocol for the Cosmos ecosystem. To understand the specifics of Osmosis, 
    it’s helpful for you to know the context of the Cosmos ecosystem upon which and for which it is built. Cosmos is an overarching ecosystem of blockchain 
    networks that can connect with one another as part of Cosmos’ mission to build an “internet of blockchains.” Interoperable decentralized applications (dApps) 
    on these various networks communicate with each other and send tokens and data back and forth via Cosmos’ Inter-Blockchain Communication (IBC) Protocol.

    **OSMO Token:**

    OSMO is the native token of the Osmosis network. Primarily, OSMO is used for staking to secure the Osmosis chain. As a PoS token, OSMO is inflationary. 
    Over time, new tokens will be minted and entered into circulation. 
    """
)

st.subheader('Liquidity, Locked Liquidity, Staking, Superfluid Staking')
st.write(
    """
    **Liquidity** refers to how quickly a financial asset may be turned into actual money. An asset is more valuable the more liquid it is. Without this liquidity, 
    investors might not be able to place buy or sell orders unless someone comes along and matches them. Tokens that can be used to withdraw money from the pool 
    are given to everyone who adds liquidity to it.

    **Locking liquidity** makes the funds immovable until they are unlocked. This means that a certain percentage of the asset has been locked and cannot be withdrawn 
    by the developers which gives investors a sense of security against their investments. Liquidity is locked using time-locked smart contracts.

    **Staking** is when you lock crypto assets for a set period of time to help support the operation of a blockchain. In return for staking your crypto, you earn 
    more cryptocurrency. Many blockchains use a proof of stake consensus mechanism.

    **Superfluid Staking** is described as “the biggest addition to Proof of Stake since slashing.” It applies a method by which those who provide liquidity to 
    certain pools can earn additional yield by also staking these bonded assets to a validator for staking rewards.
    """
)

st.header("Methodology")
with st.expander("Method details and data sources"):
    st.write(
        """
        There is a Balances table launched under Osmosis → _osmosis.core.fact_daily_balances_ In the table, we have 4 balance types:

        **liquid:**  Liquidity in cryptocurrency markets essentially refers to the ease with which tokens can be swapped to other tokens (or to government issued fiat currencies). This balance is the total liquidity provided by the wallet with the corresponding token.

        **locked liquidity:** Locking liquidity makes the funds immovable until they are unlocked. This means that a certain percentage of the asset has been locked and can not be withdrawn by the developers which give investors a sense of security against their investments.

        **staked:**  Staking is the process of locking up crypto holdings in order to obtain rewards or earn interest.

        **superfluid staked:** Superfluid Staking allows users to both stake tokens while simultaneously using them to provide assets to a liquidity pool. This means users are rewarded for helping secure the blockchain while staking, and receive reward fees associated with liquidity pool transactions.

        For this approach, we used the following three tables:

        Get the Daily Balances from the table _**osmosis.core.fact_daily_balances**_ by filtering with different currencies by different balance types.

        Join with the table _**osmosis.core.ez_prices**_ to get the price for the currency field in the balances table on daily basis so that we can calculate 
        the Balance in USD for all the wallets & their corresponding tokens.

        In this dashboard, the data has been selected from flipside crypto 
        (https://flipsidecrypto.xyz) data platform using its REST API. These queries are run every 
        12 hours to include the latest data, and the JSON file is imported directly into each visualization.
        This tool's source code is available in the 
        [**GitHub Repository**](https://github.com/zazu9249/near-mega-dashboard).

        Here are the queries for all the visualizations: 
        [**Flipside Collection**](https://app.flipsidecrypto.com/velocity/collections/558df0ca-470c-4f70-9554-f3f797ed15d7) 
        """
    )

st.header("Overall Metrics by Liquidity & Staking")
tab2, tab1 = st.tabs(
        [
            "**Liquidity**",
            "**Staking**"
        ]
    )

with tab2:
    active_wallets = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/f5eca31b-1f20-4907-b41d-e4638df6c916/data/latest')
    c1, c2 = st.columns([1,1])
    with c1:
        st.metric(label='**Number of Active Wallets participated in Liquidity**', value=str(active_wallets['NO_OF_WALLETS'].values[0]))
    with c2:
        st.metric(label='**Number of Active Wallets Locked their Liquidity**', value=str(active_wallets['NO_OF_WALLETS'].values[1]))
    wallets_over_time = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/a14ce172-5b41-43f5-92bc-178725dbc79f/data/latest')
    df = wallets_over_time.query("(BALANCE_TYPE=='liquid') | (BALANCE_TYPE=='locked liquidity')")
    fig = px.line(df, title='Number of Active Wallets participated in Liquidity & Locked their Liquidity on Daily basis', x=df['DATE'], y=df['NO_OF_WALLETS'], color='BALANCE_TYPE')
    fig.update_layout(legend_title=None, xaxis_title='Day', yaxis_title='Active Wallets')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    balance = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/58bc9b5d-c1fe-491b-840d-078b17e92dae/data/latest')
    df = balance.query("(BALANCE_TYPE=='liquid')")
    st.metric(label='**Total Liquidity Balance (in $)**', value=str(df['BALANCE_USD'].values[0]))

    balance_usd = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/f20a4bd2-ffd0-4aa5-93a5-89233835c2a9/data/latest')
    df=balance_usd.query("(BALANCE_TYPE=='liquid')")
    fig = px.area(df, title='Total Balance of Liquidity over Time (in USD)', x=df['DAY'], y=df['BALANCE_USD'])
    fig.update_layout(legend_title=None, xaxis_title='Day', yaxis_title='Balance (in $)')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    c1, c2 = st.columns([1,1])
    with c1:
        top_wallets = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/cab246a6-1525-48ed-a967-f5f300b463a3/data/latest')
        fig = px.pie(top_wallets, values='BALANCE_USD', names='ADDRESS', title='Top Wallets with high Liquidity Balance (in USD)')
        fig.update_layout(showlegend= True)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
    with c2:
        top_wallets = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/9957f6c8-b88c-4088-9ccc-b298168437d7/data/latest')
        fig = px.pie(top_wallets, values='BALANCE', names='ADDRESS', title='Top Wallets with high Locked Liquidity Balance (in USD)')
        fig.update_layout(showlegend= True)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

with tab1:
    active_wallets = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/f5eca31b-1f20-4907-b41d-e4638df6c916/data/latest')
    c1, c2 = st.columns([1,1])
    with c1:
        st.metric(label='**Number of Active Wallets participated in Staking**', value=str(active_wallets['NO_OF_WALLETS'].values[2]))
    with c2:
        st.metric(label='**Number of Active Wallets participated in Superfluid Staking**', value=str(active_wallets['NO_OF_WALLETS'].values[3]))
    
    wallets_over_time = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/a14ce172-5b41-43f5-92bc-178725dbc79f/data/latest')
    df = wallets_over_time.query("(BALANCE_TYPE=='staked') | (BALANCE_TYPE=='superfluid staked')")
    fig = px.line(df, title='Number of Active Wallets participated in Staking & Superfluid Staking on Daily basis', x=df['DATE'], y=df['NO_OF_WALLETS'], color='BALANCE_TYPE')
    fig.update_layout(legend_title=None, xaxis_title='Day', yaxis_title='Active Wallets')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    balance = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/58bc9b5d-c1fe-491b-840d-078b17e92dae/data/latest')
    df = balance.query("(BALANCE_TYPE=='staked')")
    st.metric(label='**Total Staked Balance (in $)**', value=str(df['BALANCE_USD'].values[0]))

    balance_usd = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/f20a4bd2-ffd0-4aa5-93a5-89233835c2a9/data/latest')
    df=balance_usd.query("(BALANCE_TYPE=='staked')")
    fig = px.area(df, title='Total Balance of Staked Tokens over Time (in USD)', x=df['DAY'], y=df['BALANCE_USD'])
    fig.update_layout(legend_title=None, xaxis_title='Day', yaxis_title='Balance (in $)')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    c1, c2 = st.columns([1,1])
    with c1:
        top_wallets = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/b4df9c17-bcf8-4d11-8609-bb651f23c268/data/latest')
        fig = px.pie(top_wallets, values='BALANCE_USD', names='ADDRESS', title='Top Wallets with high Staked Balance (in USD)')
        fig.update_layout(showlegend= True)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

    with c2:
        top_wallets_superfluid = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/5270c4df-e1ab-4ff3-b158-3bf6d9ceb1c8/data/latest')
        fig = px.pie(top_wallets_superfluid, values='BALANCE', names='ADDRESS', title='Top Wallets with high Superfluid Staked Balance (in USD)')
        fig.update_layout(showlegend= True)
        st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.header('How the token OSMO affected?')
st.write(
    """
    _Below are some metrics to get the insights on the **OSMO Token changes with the help of Wallet Balances**_
    """
)

c1, c2 = st.columns([1,2])
with c1:
    osmo_balance_usd = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/bf955846-da84-40df-a6f5-ba0c966e43da/data/latest')
    fig = px.pie(osmo_balance_usd, values='BALANCE_USD', names='BALANCE_TYPE', title='Total Liquidity Balance vs Staked Balance (in $)')
    fig.update_layout(showlegend= True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    osmo_balance_usd_time = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/dad15a19-42e6-4b4a-9909-e9b1f9aff6bd/data/latest')
    fig = px.area(osmo_balance_usd_time, title='Total Liquidity Balance vs Staked Balance over Time (in $)', x=osmo_balance_usd_time['DATE'], y=osmo_balance_usd_time['BALANCE_USD'], color='BALANCE_TYPE')
    fig.update_layout(legend_title=None, xaxis_title='Day', yaxis_title='Balance (in $)')
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

c1,c2,c3 = st.columns([1,1,1])
osmo_wallets = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/17cc440c-6e4f-491e-a928-472690328be5/data/latest')
with c1:
    st.metric(label='**Number of Wallets LPing/Staking OSMO**', value=str(osmo_wallets['TOTAL_WALLETS'].values[0]))
with c2:
    st.metric(label='**Total OSMO Balance by LPing/Staking**', value=str(osmo_wallets['TOTAL_OSMO_BALANCE'].values[0]))
with c3:
    st.metric(label='**Average OSMO per Wallet**', value=str(osmo_wallets['AVG_OSMO_PER_WALLET'].values[0]))

avg_osmo_per_wallet = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/dbf0c2ed-dabe-4de8-8ade-b13f8a6872b4/data/latest')
fig = px.line(avg_osmo_per_wallet, x="DATE", y="TOTAL_WALLETS", title="Average OSMO per Wallet vs The Wallets Growth", log_y=True)
fig.add_trace(go.Bar(x=avg_osmo_per_wallet["DATE"], y=avg_osmo_per_wallet["AVG_OSMO_PER_WALLET"]))
fig.update_layout(showlegend=False, legend_title=None, xaxis_title='DATE', yaxis_title='Avg OSMO/Wallet vs No of Wallets')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

holding_osmo_other = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/d895db51-1613-4608-89b2-4b0f56649766/data/latest')
fig = px.area(holding_osmo_other, title='Average Balance of Lping/Staking OSMO vs Other Tokens', x="DATE", y=["AVG_BALANCE_OSMO","AVG_BALANCE_OTHER"])
fig.update_layout(legend_title=None, xaxis_title='Day', yaxis_title='Balance (in $)')
st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.subheader('Top Tokens Lping/Staking by most Wallets and with the most Balances')
c1, c2 = st.columns([1,1])
with c1:
    top_tokens_wallets = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/28f0ef75-6dea-441e-b110-420acd9a3bec/data/latest')
    fig = px.pie(top_tokens_wallets, values='WALLETS', names='PROJECT_NAME', title='Top Tokens that Lping/Staking by most of the Wallets')
    fig.update_layout(showlegend= True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    top_tokens_wallets = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/8268ae93-7fe0-4a8c-9522-dcd400158952/data/latest')
    fig = px.pie(top_tokens_wallets, values='BALANCE_USD', names='PROJECT_NAME', title='Top Tokens that hold the most Liquidity/Staked Balance')
    fig.update_layout(showlegend= True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

st.subheader('Top Pools with most Locked Liquidity & Superfluid Staked Balances')
c1, c2 = st.columns([1,1])
with c1:
    top_pools_locked_liquid = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/c0e8a857-0577-4fa6-93f2-d55971c8f861/data/latest')
    fig = px.pie(top_pools_locked_liquid, values='BALANCE', names='POOL_ID', title='Top Pools with the most Locked Liquidity Balance')
    fig.update_layout(showlegend= True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)
with c2:
    top_pools_superfluid_staked = pd.read_json('https://node-api.flipsidecrypto.com/api/v2/queries/bb7314d1-7f25-4460-824c-6e554be3d7c3/data/latest')
    fig = px.pie(top_pools_superfluid_staked, values='BALANCE', names='POOL_ID', title='Top Pools with the most Superfluid Staked Balance')
    fig.update_layout(showlegend= True)
    st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)


