import streamlit as st
import csv
from pathlib import Path
from datetime import date

st.markdown("# Spring Week Job Tracker", text_alignment="center")


csv_path = Path("applications.csv")

if st.session_state.pop("clear_inputs", False):
    st.session_state["company"] = ""
    st.session_state["role"] = ""
    st.session_state["link"] = ""
    st.session_state["deadline"] = date.today()
    st.session_state["status"] = "None"


company = st.text_input("Company name", key="company")
role = st.text_input("Role", key="role")
link = st.text_input("URL", key="link")
deadline = st.date_input("Deadline", key="deadline")
status = st.selectbox(
    "Status",
    ["None" ,"Interested", "Applied", "Online Assessment", "Interview", "Rejected", "Offer"],
    key="status"
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

        st.session_state["clear_inputs"] = True
        st.rerun()


        



load_applications = []

if csv_path.exists() and csv_path.stat().st_size > 0:
    with csv_path.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        load_applications = list(reader)

st.subheader("Your Applications")

if load_applications:
     st.dataframe(
        load_applications,
        width="stretch",
        hide_index=True
     )
else:
     st.info("No applications saved yet.")


company_options = []

for application in load_applications:
     company_options.append(application["company"] +
                            " - " + application["role"]
                            )


selected_company = st.selectbox(
     "Delete",
    ["None"] + company_options
)



if selected_company != "None":
    delete_clicked = st.button(f"Are you sure to delete {selected_company} ?")

    if delete_clicked:
        remaining_applications = []

        selected_index = company_options.index(selected_company)
        load_applications.pop(selected_index)

        with csv_path.open("w", newline="", encoding="utf-8") as file:
             writer = csv.DictWriter(
                  file,
                  fieldnames=["company", "role", "link", "deadline", "status"]
             )

             writer.writeheader()
             writer.writerows(load_applications)

        st.session_state["success_message"] = (
            f"{selected_company} was deleted."
        )


        st.rerun()
     

