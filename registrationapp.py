import streamlit as st
import math
import random          # NEW – for shuffling and randint
from pathlib import Path

# ───────────────────────────────────────────
#  Basic configuration
# ───────────────────────────────────────────
PASSWORD       = "AgenticAndRobotic"
CARDS_PER_PAGE = 4
TOTAL_CARDS    = random.randint(18, 26)      # NEW – 18-26 cards each run

# ───────────────────────────────────────────
#  Dummy-data pools (26 items each)
# ───────────────────────────────────────────
FIRST_NAMES = [
    "Alex","Blair","Casey","Dana","Evan","Finley","Gray","Hadley","Indigo","Jordan",
    "Kai","Logan","Morgan","Nico","Oakley","Parker","Quinn","Reese","Sawyer","Taylor",
    "Umber","Val","Winter","Xen","Yael","Zion"
]
LAST_NAMES = [
    "Archer","Bennett","Campbell","Diaz","Ellis","Foster","Garcia","Hayes","Iverson","Johnson",
    "Keller","Lee","Morris","Nguyen","Olsen","Porter","Quintero","Robinson","Steele","Turner",
    "Underwood","Vega","Walker","Xu","Young","Zimmerman"
]
COMPANIES = [
    "Apex Dynamics","Brightpath AI","CloudForge Labs","Delta Quanta","Evolvix Solutions","FusionEdge Tech",
    "GreenHill Analytics","Hyperion Robotics","IonSphere Ventures","JadeStream Inc",
    "Kinetic Nodes","Luminary Works","MetaPulse Systems","NorthBridge Labs","Optima Robotics",
    "Photon Creek","QuantumShift","RedOak Digital","StellarSight","TerraForge",
    "UrbanMint","VaporTrail Tech","Waveform AI","XyloSoft","YieldSphere","ZenithWorks"
]
ROLES        = ["Software Engineer","Data Scientist","Automation Architect",
                "Business Analyst","Product Manager","DevOps Engineer"]
TICKET_TYPES = ["Standard","VIP","Speaker"]

# ───────────────────────────────────────────
#  Build a **random** participant list
# ───────────────────────────────────────────
# Shuffle each attribute list independently to randomise pairings
random.shuffle(FIRST_NAMES)
random.shuffle(LAST_NAMES)
random.shuffle(COMPANIES)

participants = []
for i in range(TOTAL_CARDS):
    first, last, company = FIRST_NAMES[i], LAST_NAMES[i], COMPANIES[i]
    email  = f"{first.lower()}.{last.lower()}@{company.lower().replace(' ','').replace('-','')}.com"
    participants.append(
        {
            "name"       : f"{first} {last}",
            "company"    : company,
            "role"       : ROLES[i % len(ROLES)],
            "email"      : email,
            "ticket_type": TICKET_TYPES[i % len(TICKET_TYPES)],
        }
    )

TOTAL_PAGES = math.ceil(TOTAL_CARDS / CARDS_PER_PAGE)

# ───────────────────────────────────────────
#  Helper functions (unchanged except comments)
# ───────────────────────────────────────────
def show_logo() -> None:
    logo = Path("uipath_logo.png")
    if logo.is_file():
        st.image(str(logo), width=180)
    else:
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/UiPath_Logo.svg/512px-UiPath_Logo.svg.png",
            width=180,
        )

def login_page() -> None:
    show_logo()
    st.title("UiPath Fusion App")
    st.subheader("Log in")
    st.write("Enter your user name and password to log in.")

    user = st.text_input("User name", key="user")
    pwd  = st.text_input("Password", type="password", key="pwd")

    if st.button("Submit"):
        if user.strip() and pwd == PASSWORD:
            st.session_state.authenticated = True
            st.session_state.page = 1
        else:
            st.error("Invalid credentials, please try again.")

def participant_card(person: dict) -> None:
    st.markdown(
        f"""
        <div style="border:1px solid #DDD;border-radius:6px;padding:12px;margin-bottom:16px">
            <strong>Name:</strong> {person['name']}<br>
            <strong>Company:</strong> {person['company']}<br>
            <strong>Role:</strong> {person['role']}<br>
            <strong>Email:</strong> {person['email']}<br>
            <strong>Ticket type:</strong> {person['ticket_type']}
        </div>
        """,
        unsafe_allow_html=True,
    )

def participants_page() -> None:
    st.title("Conference Participants")

    start = (st.session_state.page - 1) * CARDS_PER_PAGE
    end   = start + CARDS_PER_PAGE
    for p in participants[start:end]:
        participant_card(p)

    # Pagination controls (bottom-center)
    col_left, col_mid, col_right = st.columns([1, 2, 1])

    with col_left:
        st.button(
            "⬅ Back",
            disabled = st.session_state.page == 1,
            on_click = lambda: st.session_state.update(page = st.session_state.page - 1),
        )

    with col_mid:
        st.markdown(f"**Page {st.session_state.page} of {TOTAL_PAGES}**", unsafe_allow_html=True)

    with col_right:
        st.button(
            "Next ➡",
            disabled = st.session_state.page == TOTAL_PAGES,
            on_click = lambda: st.session_state.update(page = st.session_state.page + 1),
        )

# ───────────────────────────────────────────
#  Page routing
# ───────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = 1

if not st.session_state.authenticated:
    login_page()
else:
    participants_page()