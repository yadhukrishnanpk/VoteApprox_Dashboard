# VoteApprox - Dashboard 🗳️

**VoteApprox** is a specialized election tracking and estimation tool designed for local political party leaders. It bridges the gap between manual paper-based counting at polling booths and digital real-time analytics, allowing party representatives to gauge performance before the official results are declared.

## 📌 Overview
During an election, party booth agents often mark tallies on paper as voters cast their ballots. **VoteApprox** digitizes this ground-level data. By allowing leaders to input manual counts and "assumed party fields" (based on local intelligence), the platform generates an approximate overview of the voting trend in a specific area.

## ✨ Key Features
* **Real-Time Updates:** Input manual tallies directly from the polling station as the day progresses.
* **Leaderboard & Estimation:** Provides a live "approximate" count based on the data provided by local agents.
* **Party Field Assumptions:** Allows leaders to categorize and filter data based on party strongholds and local demographics.
* **Data Accuracy Management:** Designed to handle "rough" data to produce a reliable trend analysis rather than just raw numbers.
* **Mobile-Friendly Interface:** Built with Bootstrap 5 for use in the field, ensuring agents can update counts quickly on the go.
* **Automated Eligibility Logic:** The system automatically calculates voter eligibility based on birth dates (18+) and tracks voting status.
* **Visual Performance Indicators:** Real-time percentage tracking with color-coded status badges (Red for <30%, Warning for 30-70%, and Success for >70%).

## 🚀 How It Works
1. **Manual Input:** As agents mark paper tallies at the booth, they enter the figures into the **Voting** module.
2. **Data Processing:** The system aggregates these manual inputs against the "assumed" party leanings and candidate data associated with those booths.
3. **Trend Visualization:** The dashboard displays which party is leading in the approximation, helping leaders strategize moves like voter mobilization in real-time.

## ⚙️ Technical Architecture

### 🗃️ Data Models
* **Party:** Stores political entities, abbreviations, and official flags/logos.
* **Candidate:** Tracks contestants, their party affiliation, and constituency details.
* **Election:** Manages the lifecycle of voting events, including start and end timestamps.
* **Voter:** Handles citizen data, including automated age calculation and eligibility checks.
* **Vote:** Records the unique relationship between a voter, an election, and a candidate to prevent duplicate entries.

### 🧠 Logic & Views
* **Trend Calculation:** Uses Django's `Count` and `Q` expressions to calculate vote shares and percentages dynamically.
* **Session Management:** Persists the "Selected Election" context across different pages for a consistent user experience.
* **Security:** Implements `staff_member_required` decorators to protect administrative functions and uses Django's authentication system for secure access.

### 🎨 Frontend & UX
* **Searchable Dropdowns:** Integrated with **Select2.js** to allow agents to find voters quickly in high-traffic environments.
* **Crispy Forms:** Ensures all data entry points are professionally styled and accessible.
* **Responsive Design:** Utilizes a sidebar-based layout that adapts to both desktop and mobile screens.

## 📂 Project Structure
| Category | Components |
| :--- | :--- |
| **Backend Logic** | `models.py`, `views.py`, `forms.py`, `urls.py` |
| **Main Dashboard** | `index.html` (Stats & Leaderboard) |
| **Management** | `electionlist.html`, `candidatelist.html`, `partylist.html`, `voter_list.html` |
| **Field Operations** | `voting.html`, `voted.html` (Mobilization list) |

---
**Disclaimer:** *Voteapprox is a tool for internal party logistics and trend estimation. It is not an official government voting portal and does not interface with official election results.*
