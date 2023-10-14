# Import necessary libraries
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Streamlit app
def main():
    st.title("LinkedIn Event Funnel Estimator")
    st.markdown("")
    col1, col2, col3 = st.columns(3)
    with col1:
        accounts = st.number_input("Number of LinkedIn accounts.", min_value=1, value=2, step=1, help="The number of Linkedin accounts inviting people to your LinkedIn event")
    with col2:
        avg_deal_size = st.number_input("Your average deal size ($)", min_value=0, value=5000, step=1000)
    with col3:
        pass
    col3, col4, col5 = st.columns([4,1,1])
    with col3:
        with st.expander("Event Funnel Conversion Estimates"):
            invites_to_reg_rate = st.slider("Invites to registrants conversion rate (%)", 0, 100, 10)
            reg_to_attend_rate = st.slider("Registrants to attendees conversion rate (%)", 0, 100, 30)
            attend_to_cust_rate = st.slider("Attendees to new customers conversion rate (%)", 0, 100, 5)

    # Calculations
    total_invites = accounts * 2000  # for 2 weeks
    registrants = (invites_to_reg_rate / 100) * total_invites
    attendees = (reg_to_attend_rate / 100) * registrants
    new_customers = (attend_to_cust_rate / 100) * attendees
    projected_revenue = new_customers * avg_deal_size

    # Dynamic sentence
    st.markdown(f"With <span style='color:blue;'>{accounts}</span> accounts promoting your LinkedIn event you should be able to send <span style='color:blue;'>{total_invites}</span> invites and get <span style='color:blue;'>{int(registrants)}</span> registrants (assuming you max out the 1k invites/week/account limit and promote for 2 weeks).", unsafe_allow_html=True) 
    st.markdown(f"Based on the estimations this will result in <span style='color:blue;'>{int(attendees)}</span> live attendees, <span style='color:blue;'>{int(new_customers)}</span> new customers.", unsafe_allow_html=True)
    st.markdown(f"<b>Projected Event Revenue:</b> <span style='color:blue;'>${projected_revenue:,.2f}</span>", unsafe_allow_html=True)
    # Funnel Graphic
    funnel_data = {"Registrants": registrants, "Live Attendees": attendees, "New Customers": new_customers}
    funnel_data = dict(sorted(funnel_data.items(), key=lambda item: item[1], reverse=True))
    # Create a dataframe with labels, values and conversion percentages
    df = pd.DataFrame(list(funnel_data.items()), columns=['Stage', 'Total'])
    df['Conversion (%)'] = (df['Total'] / df['Total'].shift()) * 100
    st.dataframe(df)
    # fig = go.Figure(data=[
    #     go.Bar(
    #         x=list(funnel_data.keys()),
    #         y=list(funnel_data.values()),
    #         text=[int(value) for value in funnel_data.values()],
    #         textposition='auto',
    #     )
    # ])
    # fig.update_layout(autosize=False, width=500)  # Adjust the width of the chart to be 2/3 of the full column
    # st.plotly_chart(fig)
if __name__ == "__main__":
    main()
