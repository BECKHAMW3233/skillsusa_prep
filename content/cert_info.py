"""Reference facts about the real Python Institute certification exams --
sourced directly from pythoninstitute.org (fetched Sept 2026), not
third-party dump/prep sites. Exists for the same reason
content/competition_info.py does: knowing the actual exam conditions
(time pressure especially) is part of prep, not just knowing the material.

Every Python Institute exam (PCEP through PCPP2) is Pearson VUE-delivered,
multiple-choice/gap-fill/scenario-based -- NOT a free-coding exam. The
"time limit" below is the exam itself; each also has a separate 5-10
minute block beforehand for the NDA and a tutorial, which does not count
against your answering time.
"""

CERT_EXAM_INFO = {
    "PCEP": {
        "full_name": "PCEP – Certified Entry-Level Python Programmer",
        "exam_code": "PCEP-30-02",
        "duration_min": 40,
        "nda_tutorial_min": 5,
        "questions": 30,
        "pass_pct": 70,
        "format": "Single- and multiple-select, drag & drop, gap-fill, sort, "
                  "code-fill, code-insertion, and interactive/scenario-based items.",
        "prerequisites": "None.",
    },
    "PCAP": {
        "full_name": "PCAP – Certified Associate in Python Programming",
        "exam_code": "PCAP-31-03",
        "duration_min": 65,
        "nda_tutorial_min": 10,
        "questions": 40,
        "pass_pct": 70,
        "format": "Single- and multiple-select, interactive, and scenario-based items.",
        "prerequisites": "None required (PCEP is a recommended, not mandatory, foundation).",
    },
    "PCPP1": {
        "full_name": "PCPP1 – Certified Professional in Python Programming 1",
        "exam_code": "PCPP-32-101",
        "duration_min": 65,
        "nda_tutorial_min": 10,
        "questions": 45,
        "pass_pct": 70,
        "format": "Single- and multiple-select, interactive, and scenario-based items.",
        "prerequisites": "None required (PCAP-level knowledge is assumed).",
    },
    "PCPP2": {
        "full_name": "PCPP2 – Certified Professional in Python Programming 2",
        "exam_code": "PCPP-32-201",
        "duration_min": 65,
        "nda_tutorial_min": 10,
        "questions": 45,
        "pass_pct": 70,
        "format": "Single- and multiple-select, interactive, and scenario-based items.",
        "prerequisites": "PCAP and PCPP1 certifications.",
    },
}

SOURCE_NOTE = ("Pulled directly from pythoninstitute.org's own PCEP, PCAP, PCPP1, and "
               "PCPP2 pages (checked Sept 2026), not a third-party prep site. Python "
               "Institute does occasionally revise exam versions (e.g. PCEP-30-02 "
               "superseding PCEP-30-01) -- if something here looks off versus what you "
               "see at registration, the current pythoninstitute.org page is the "
               "tiebreaker, not this trainer.")
