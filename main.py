import streamlit as st
import csv
from pathlib import Path

st.markdown("# Spring Week Job Tracker", text_alignment="center")



company = st.text_input("Company name")
role = st.text_input("Role")
link = st.text_input("URL")
deadline = st.date_input("Deadline")
status = st.selectbox(
    "Status",
    ["None" ,"Interested", "Applied", "Online Assessment", "Interview", "Rejected", "Offer"]
)

add_clicked = st.button("Add application")

if add_clicked:
    if not company.strip():
        st.error("Company name is required.")
    elif not role.strip():
            st.error("role is required.")
    elif not link.strip():
            st.error("Link is required.")
    elif status == "None":
            st.error("Status is required.")
    else:

        job_application = {
            "company": company.strip(),
            "role": role.strip(),
            "link": link.strip(),
            "deadline": deadline.isoformat(),
            "status": status
            }

        csv_path = Path("applications.csv")

        file_is_empty = (
            not csv_path.exists()
            or csv_path.stat().st_size == 0
            )

        with csv_path.open("a", newline="", encoding="utf-8",) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=job_application.keys()
                )

            if file_is_empty:
                writer.writeheader()

            writer.writerow(job_application)
        
        
        st.success("The application successfully added.")
        


         