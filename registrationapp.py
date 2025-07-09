import streamlit as st
import random, math, textwrap

# ── App-wide constants ────────────────────────────────────────────────────────
PASSWORD       = "AgenticAndRobotic"
CARDS_PER_PAGE = 4
MIN_CARDS, MAX_CARDS = 18, 26         # range of participants per run

# ── One-time data generation (stored in session_state) ────────────────────────
def init_participants():
    """Generate the participant list only once per browser session."""
    if "participants" in st.session_state:
        return                                               # already done

    first_names = ["Alex","Blair","Casey","Dana","Evan","Finley","Gray",
                   "Hadley","Indigo","Jordan","Kai","Logan","Morgan",
                   "Nico","Oakley","Parker","Quinn","Reese","Sawyer",
                   "Taylor","Umber","Val","Winter","Xen","Yael","Zion"]
    last_names  = ["Archer","Bennett","Campbell","Diaz","Ellis","Foster",
                   "Garcia","Hayes","Iverson","Johnson","Keller","Lee",
                   "Morris","Nguyen","Olsen","Porter","Quintero","Robinson",
                   "Steele","Turner","Underwood","Vega","Walker","Xu",
                   "Young","Zimmerman"]
    companies   = ["Apex Dynamics","Brightpath AI","CloudForge Labs","Delta Quanta",
                   "Evolvix Solutions","FusionEdge Tech","GreenHill Analytics",
                   "Hyperion Robotics","IonSphere Ventures","JadeStream Inc",
                   "Kinetic Nodes","Luminary Works","MetaPulse Systems",
                   "NorthBridge Labs","Optima Robotics","Photon Creek",
                   "QuantumShift","RedOak Digital","StellarSight","TerraForge",
                   "UrbanMint","VaporTrail Tech","Waveform AI","XyloSoft",
                   "YieldSphere","ZenithWorks"]
    roles        = ["Software Engineer","Data Scientist","Automation Architect",
                    "Business Analyst","Product Manager","DevOps Engineer"]
    ticket_types = ["Standard","Silver","Gold"]

    # shuffle so pairings are random each browser session
    random.shuffle(first_names)
    random.shuffle(last_names)
    random.shuffle(companies)

    n_cards   = random.randint(MIN_CARDS, MAX_CARDS)
    people    = []
    for i in range(n_cards):
        first, last, company = first_names[i], last_names[i], companies[i]
        email = f"{first.lower()}.{last.lower()}@{company.lower().replace(' ','').replace('-','')}.com"
        people.append(
            {
                "name"       : f"{first} {last}",
                "company"    : company,
                "role"       : roles[i % len(roles)],
                "email"      : email,
                "ticket_type": ticket_types[i % len(ticket_types)],
            }
        )

    st.session_state.participants = people
    st.session_state.total_pages  = math.ceil(len(people) / CARDS_PER_PAGE)

# ── CSS injected on every render ──────────────────────────────────────────────
def add_css() -> None:
    st.markdown(
        """
        <style>
          table.participants{width:100%;border-collapse:separate;border-spacing:0 16px;}
          tr.card{
            background:#fff;
            border:1px solid #ddd;            /* single outer outline              */
            border-radius:6px;overflow:hidden;
          }
          td{
            display:block;
            padding:4px 8px;
            word-break:break-word;
            border:none;                      /* no inner borders between fields   */
          }
          td.name::before   {content:"Name: ";font-weight:700;}
          td.company::before{content:"Company: ";font-weight:700;}
          td.role::before   {content:"Role: ";font-weight:700;}
          td.email::before  {content:"Email: ";font-weight:700;}
          td.ticket::before {content:"Ticket type: ";font-weight:700;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ── Helper views ──────────────────────────────────────────────────────────────
def show_robot_icon() -> None:
    st.image("https://img.icons8.com/ios-filled/200/robot-2--v1.png", width=100)

def login_page() -> None:
    show_robot_icon()
    st.title("Event Registration App")
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

def participants_table(slice_) -> str:
    rows = []
    for p in slice_:
        rows.append(textwrap.dedent(f"""\
        <tr class="card" role="row">
          <td class="name"    data-column="name">{p['name']}</td>
          <td class="company" data-column="company">{p['company']}</td>
          <td class="role"    data-column="role">{p['role']}</td>
          <td class="email"   data-column="email">{p['email']}</td>
          <td class="ticket"  data-column="ticket_type">{p['ticket_type']}</td>
        </tr>"""))
    return "<table class='participants' role='table'><tbody>" + "".join(rows) + "</tbody></table>"

def participants_page() -> None:
    add_css()
    st.title("Conference Participants")

    start = (st.session_state.page - 1) * CARDS_PER_PAGE
    end   = start + CARDS_PER_PAGE
    st.markdown(participants_table(st.session_state.participants[start:end]),
                unsafe_allow_html=True)

    # ─ Pagination ────────────────────────────────────────────────────────────
    col_left, col_mid, col_right = st.columns([1,2,1])

    # Back button
    if st.session_state.page > 1:
        col_left.button("⬅ Back",
                        on_click=lambda: st.session_state.update(page=st.session_state.page-1))

    # Page indicator
    col_mid.markdown(f"**Page {st.session_state.page} of {st.session_state.total_pages}**",
                     unsafe_allow_html=True)

    # Next button – hidden on last page
    if st.session_state.page < st.session_state.total_pages:
        col_right.button("Next ➡",
                         on_click=lambda: st.session_state.update(page=st.session_state.page+1))

# ── Routing ───────────────────────────────────────────────────────────────────
init_participants()

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = 1

if not st.session_state.authenticated:
    login_page()
else:
    participants_page()