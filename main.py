# Import necessary libraries
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from markdownlit import mdlit

def main():
    st.set_page_config(page_icon=":1234:")
    st.title("Event Funnel :green[Revenue] Estimator")
    mdlit("""This app gives you an example of how much you could make from hosting LinkedIn events depending on the amount of followers you have and how many accounts you have to promote it.""")  
    st.markdown("")
    col1, col2, col3 = st.columns(3)
    with col1:
        accounts = st.number_input("Number of LinkedIn accounts.", min_value=1, value=2, step=1, help="The number of Linkedin accounts inviting people to your LinkedIn event")
    with col2:
        avg_deal_size = st.number_input("Your average deal size ($)", min_value=0, value=3000, step=1000, help="What is the value of the your event offer?")
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
    mdlit(f"With [blue]{int(accounts)}[/blue] accounts promoting your event you should be able to send [blue]{int(total_invites)}[/blue] invites and get [blue]{int(registrants)}[/blue] registrants*.") 
    mdlit(f"Based on the conversion estimations this will result in [blue]{int(attendees)}[/blue] live attendees, [blue]{int(new_customers)}[/blue] new customers.")
    st.subheader(f"Projected Event Revenue: :green[${projected_revenue:,.2f}]")
    annual_projected_revenue = projected_revenue * 4
    mdlit(f"<span style=color:grey;>*_This is assuming you max out the 1k invites/week/account limit and promote for 2 weeks._</span>")
    st.success(f"That could be a ${annual_projected_revenue:,.2f} increase in revenue if you held even a quarterly event.")

    # Funnel Graphic
    funnel_data = {"Registrants": registrants, "Live Attendees": attendees, "New Customers": new_customers}
    funnel_data = dict(sorted(funnel_data.items(), key=lambda item: item[1], reverse=True))
    # Create a dataframe with labels, values and conversion percentages
    df = pd.DataFrame(list(funnel_data.items()), columns=['Stage', 'Total'])
    df['Total'] = df['Total'].astype(int)
    df['Conversion (%)'] = ((df['Total'] / df['Total'].shift()) * 100).fillna(0).astype(int)
    
    col6, col7, col8 = st.columns([4,1,1])
    with col6:
        with st.expander("Show event pipeline numbers"):
            st.dataframe(df, hide_index=True)
            st.caption("You can make edits to these conversation rates in the dropdown above")

    mdlit(f"")

if __name__ == "__main__":
    main()
