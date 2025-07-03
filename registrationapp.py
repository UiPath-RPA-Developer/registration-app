import streamlit as st
import math, random
from pathlib import Path

# ───────────────────────────────────────────
#  Basic configuration
# ───────────────────────────────────────────
PASSWORD       = "AgenticAndRobotic"
CARDS_PER_PAGE = 4
TOTAL_CARDS    = random.randint(18, 26)     # 18-26 cards each run

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
TICKET_TYPES = ["Standard","Silver","Gold"]

# ───────────────────────────────────────────
#  Build a **randomised** participant list
# ───────────────────────────────────────────
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
#  One-time CSS (labels & values inline)
# ───────────────────────────────────────────
def add_css_once() -> None:
    if "css_added" in st.session_state:
        return
    st.session_state.css_added = True
    st.markdown(
        """
        <style>
        .card       {border:1px solid #DDD;border-radius:6px;padding:12px;margin-bottom:16px}
        .field      {display:flex;gap:6px;margin-bottom:4px}
        .label      {font-weight:700;min-width:100px}
        .value      {flex:1;word-break:break-word}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ───────────────────────────────────────────
#  Helper functions
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
    """Each value is its own <span class='value ...' data-column='…'> for UiPath."""
    st.markdown(
        f"""
        <div class="card" role="row">
          <div class="field">
            <span class="label">Name:</span>
            <span class="value name" data-column="name">{person['name']}</span>
          </div>
          <div class="field">
            <span class="label">Company:</span>
            <span class="value company" data-column="company">{person['company']}</span>
          </div>
          <div class="field">
            <span class="label">Role:</span>
            <span class="value role" data-column="role">{person['role']}</span>
          </div>
          <div class="field">
            <span class="label">Email:</span>
            <span class="value email" data-column="email">{person['email']}</span>
          </div>
          <div class="field">
            <span class="label">Ticket type:</span>
            <span class="value ticket" data-column="ticket_type">{person['ticket_type']}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def participants_page() -> None:
    st.title("Conference Participants")
    add_css_once()

    start = (st.session_state.page - 1) * CARDS_PER_PAGE
    end   = start + CARDS_PER_PAGE
    for p in participants[start:end]:
        participant_card(p)

    # Pagination controls
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
