"""Static reference data: rubric, categories, topics, tracks, and the phase plan."""

RUBRIC_CRITERIA = [
    "Completeness",
    "Correctness",
    "Input Validation",
    "Documentation",
    "Efficiency",
    "Quality of Work",
]

PROBLEM_TYPES = [
    "Menu-driven console app",
    "File I/O & data parsing",
    "Input validation focus",
    "OOP / class-based model",
    "Search & sort algorithm",
    "String manipulation",
    "Recursion",
    "Full mock project (3-part)",
    "Speed drill (30 min)",
    "PCEP Skill Builder",
    "PCAP Skill Builder",
    "PCPP1 Skill Builder",
    "PCPP2 Skill Builder",
]

DIFFICULTIES = ["Easy", "Medium", "Hard"]

# Python is the primary focus (per training priorities); the rest stay
# lighter-weight since the objective knowledge test only samples them.
KNOWLEDGE_TOPICS = [
    "Python - core syntax",
    "Python - OOP",
    "Python - file I/O",
    "Python - algorithms",

    "Python - PCEP: Fundamentals & I/O",
    "Python - PCEP: Control Flow",
    "Python - PCEP: Data Collections",
    "Python - PCEP: Functions & Scope",

    "Python - slicing & sequences (PCAP)",
    "Python - comprehensions & generators (PCAP)",
    "Python - exceptions (PCAP)",
    "Python - modules & packages (PCAP)",
    "Python - string methods (PCAP)",

    "Python - PCPP1: Advanced OOP",
    "Python - PCPP1: Testing & Best Practices",
    "Python - PCPP1: File Formats (CSV/JSON/XML)",
    "Python - PCPP1: GUI & Networking Basics",

    "Python - PCPP2: Design Patterns",
    "Python - PCPP2: Databases & Advanced Networking",
    "Python - PCPP2: Packaging, Testing & Performance",

    "SQL - basics",
    "SQL - joins & aggregates",
    "Java - basics",
    "JavaScript - basics",
    "C - basics",
    "C++ - basics",
    "C# - basics",
    "PHP - basics",
    "Ruby - basics",
    "Objective-C - basics",
    "PDT - Professional Development",
]

PYTHON_TOPICS = {t for t in KNOWLEDGE_TOPICS if t.startswith("Python")}

# ── training tracks ─────────────────────────────────────────────────────
#
# A user can focus the whole app on one goal (SkillsUSA contest prep, or
# one rung of Python Institute's PCEP -> PCAP -> PCPP1 -> PCPP2 ladder) and
# have everything unrelated to it drop out of the Problem Bank, Knowledge
# Quiz, and Mock/Packet setup -- or leave it on "All" to see everything.

TRACKS = ["SkillsUSA", "PCEP", "PCAP", "PCPP1", "PCPP2"]

TRACK_LABELS = {
    "All": "All Content",
    "SkillsUSA": "SkillsUSA Computer Programming",
    "PCEP": "PCEP – Entry-Level Python Programmer",
    "PCAP": "PCAP – Certified Associate in Python Programming",
    "PCPP1": "PCPP1 – Certified Professional in Python Programming 1",
    "PCPP2": "PCPP2 – Certified Professional in Python Programming 2",
}

# Every knowledge-quiz topic's track membership. A topic with no entry here
# defaults to SkillsUSA-only (that covers the non-Python language topics
# and PDT). The four core Python topics count toward both SkillsUSA and
# PCAP, since PCAP's official blueprint assumes exactly that foundation
# (core syntax, OOP, file I/O, algorithmic thinking) on top of its own
# associate-level material.
TOPIC_TRACKS = {
    "Python - core syntax": {"SkillsUSA", "PCAP"},
    "Python - OOP": {"SkillsUSA", "PCAP"},
    "Python - file I/O": {"SkillsUSA", "PCAP"},
    "Python - algorithms": {"SkillsUSA", "PCAP"},

    "Python - PCEP: Fundamentals & I/O": {"PCEP"},
    "Python - PCEP: Control Flow": {"PCEP"},
    "Python - PCEP: Data Collections": {"PCEP"},
    "Python - PCEP: Functions & Scope": {"PCEP"},

    "Python - slicing & sequences (PCAP)": {"PCAP"},
    "Python - comprehensions & generators (PCAP)": {"PCAP"},
    "Python - exceptions (PCAP)": {"PCAP"},
    "Python - modules & packages (PCAP)": {"PCAP"},
    "Python - string methods (PCAP)": {"PCAP"},

    "Python - PCPP1: Advanced OOP": {"PCPP1"},
    "Python - PCPP1: Testing & Best Practices": {"PCPP1"},
    "Python - PCPP1: File Formats (CSV/JSON/XML)": {"PCPP1"},
    "Python - PCPP1: GUI & Networking Basics": {"PCPP1"},

    "Python - PCPP2: Design Patterns": {"PCPP2"},
    "Python - PCPP2: Databases & Advanced Networking": {"PCPP2"},
    "Python - PCPP2: Packaging, Testing & Performance": {"PCPP2"},
}

# Every Problem Bank category's track membership. A category with no entry
# here defaults to SkillsUSA-only.
CATEGORY_TRACKS = {
    "PCEP Skill Builder": {"PCEP"},
    "PCAP Skill Builder": {"PCAP"},
    "PCPP1 Skill Builder": {"PCPP1"},
    "PCPP2 Skill Builder": {"PCPP2"},
}


def topics_for_track(track):
    """KNOWLEDGE_TOPICS narrowed to one track, in their normal order."""
    if not track or track == "All":
        return list(KNOWLEDGE_TOPICS)
    return [t for t in KNOWLEDGE_TOPICS if track in TOPIC_TRACKS.get(t, {"SkillsUSA"})]


def categories_for_track(track):
    """PROBLEM_TYPES narrowed to one track, in their normal order."""
    if not track or track == "All":
        return list(PROBLEM_TYPES)
    return [c for c in PROBLEM_TYPES if track in CATEGORY_TRACKS.get(c, {"SkillsUSA"})]


# Categories excluded from randomly-generated SkillsUSA packet simulations:
# "Full mock project" is already a multi-part project (nesting one inside
# another multi-program packet isn't realistic), and every certification
# "Skill Builder" category is exam prep, not a SkillsUSA-style contest
# problem.
PACKET_EXCLUDED_CATEGORIES = {"Full mock project (3-part)"} | set(CATEGORY_TRACKS.keys())

PHASES = [
    ("Phase 1", "Foundations", "Sep-Oct 2026", "Core syntax, validation, file I/O, functions, OOP basics"),
    ("Phase 2", "Problem Types", "Nov-Dec 2026", "Menu apps, data parsing, search/sort, class models, algorithms"),
    ("Phase 3", "Mock Competition", "Jan-Feb 2027", "Full timed simulations, PDT & knowledge test, mock interview"),
    ("Phase 4", "Sharpen & Peak", "Mar 2027", "Eliminate weak spots, interview lock-in, final full run 1 week out"),
]
