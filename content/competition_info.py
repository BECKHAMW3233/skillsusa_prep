"""
Reference material on how the actual SkillsUSA Computer Programming contest
works, compiled from primary sources: the 2024-26 national Technical
Standards, the 2021 edition, real national contest packets from 2014 and
2021, and NC-specific guidance. This exists because knowing the FORMAT and
CONVENTIONS competitors are judged by is as much a part of prep as knowing
Python -- and it's the part no textbook covers.
"""

OVERVIEW = """SkillsUSA Computer Programming has stayed structurally the same for at
least a decade: you get a packet of 3-4 self-contained programs to write
under time pressure, each scored against the same six-criteria rubric,
plus a written knowledge test and a mock entry-level-programmer interview.
Python is a recent addition to the language roster (it wasn't listed as
recently as 2021 -- the roster back then was just Visual Basic, Java, C++,
or RPG). Because of that, the official "competencies" checklist is still
written around Java/C++/Visual Basic fundamentals. In practice that means
judges are grading transferable fundamentals -- correct output, validated
input, documented and efficient code -- not language trivia."""

SCOPE = """Everything on this page is sourced from the NATIONAL SkillsUSA
Championships Technical Standards and General Regulations, plus real
national-contest packets (2014, 2021), and confirmed directly against NC's
own materials -- specifically the 2026 SkillsUSA North Carolina State
Conference Program (skillsusanc.org) and NC's competition-guidelines page.
No other state's rules were used anywhere in this page.

Two concrete, NC-sourced confirmations that the national rules ARE what
governs you:
  - NC's own 2026 State Conference Program lists "COMPUTER PROGRAMMING"
    with the category tag "National Contest" (as opposed to the "State
    Contest" tag other competitions on that same schedule carry, e.g.
    Debate, Natural Hair Design). That tag means NC runs this specific
    competition straight off the National Technical Standards -- it isn't
    a separately-ruled NC variant.
  - NC's own competition-guidelines page says, for any contest without
    NC-specific rules posted (Computer Programming currently included):
    "If nothing has been posted yet, please refer to the National
    Technical Standards to begin your preparations."
If you advance to Nationals, it's the same National Technical Standards
again, directly -- no translation needed either way."""

PACKET_STRUCTURE = """You receive a packet of 3 or 4 programs in one sitting. Historically
each program in the packet is written for a specific language chosen by
the technical committee (so one project might specify Java, another SQL,
another Python) -- the packet doesn't let you pick your own language per
problem, though you bring your own reference manual for whichever
language(s) you'll be coding in. Work through them in order. The real
national-contest process (documented in a 2014 packet) is:
  1. Finish a program.
  2. Write your contestant number and the time on the judges' sign-up
     sheet for that program.
  3. A judge calls you up in turn to execute your program and confirm the
     output is correct.
  4. Once approved, print your code and the output/screen, mark it with
     your contestant number, and hand it to the judges' table.
  5. Move on to the next program.
This means pacing across the WHOLE packet matters more than perfecting
any single program -- a strong 3/4 beats one flawless program and two
unfinished ones."""

RUBRIC = [
    ("Completeness", "Did you finish everything the spec asked for -- every menu option, "
     "every output field, every edge case it described?"),
    ("Correctness of output", "Does the program actually produce the right numbers/text for "
     "the given inputs? This is checked live by a judge re-running your program."),
    ("Validation of input", "Does the program reject or handle bad input gracefully instead "
     "of crashing? Historically this is graded separately from correctness -- a program that "
     "works perfectly on good input but crashes on bad input loses points here specifically."),
    ("Internal documentation", "Comments and clear structure explaining what the code does and "
     "why -- judges read the printed source, not just run it."),
    ("Efficiency of code", "Reasonably direct code -- not wasteful loops, not copy-pasted "
     "blocks that should've been a function, not O(n^2) where O(n) was obvious."),
    ("Quality of work", "Overall polish: clean output formatting, sensible variable names, a "
     "program that looks like it was written by someone who does this for a living."),
]

KNOWLEDGE_TEST = """A written knowledge test covering (per the 2024-26 national standards)
Java, C, C++, C#, Python, Ruby, JavaScript, PHP, Objective-C, and SQL, plus
a separate SkillsUSA Professional Development Test (PDT). You won't be
deep-tested on all ten languages -- but core-syntax-level questions
("what does this keyword do," "what will this print") are fair game
across the list, which is why this trainer keeps light coverage of all of
them even though Python is the priority."""

INTERVIEW = """A mock interview "to assess competitors' ability to answer questions
typical of an entry-level position for a computer programmer." Expect
questions that test whether you can explain your OWN code and reasoning,
not just recite definitions -- e.g. being asked to walk through a program
you just wrote, explain a bug you hit, or distinguish a syntax error from
a logic error (that distinction is literally competency 2.10 in the
official standards). Dress and conduct expectations follow the general
SkillsUSA professional-development framework (Personal Skills, Workplace
Skills, Technical Skills)."""

INTERNET_AI_DEVICE_POLICY = """CONFIRMED, from national rules that NC runs Computer Programming under
(see Scope above) plus NC's own 2026 State Conference Program directly:

  - NC's own Code of Conduct, printed in the 2026 State Conference
    Program: "No cell phones are allowed into competition." That's NC's
    wording, not a national document's.
  - National Regulation #29 (Observer Rules, applies org-wide -- not
    trade-specific): "During the competition, participants must work
    independently, without assistance from judges, teachers, fellow
    students, and/or observers. Competitors may be disqualified for
    receiving such assistance."
  - National Regulation #13 (Prohibited Devices, applies org-wide):
    cellphones, electronic watches, and any other electronic device not
    specifically approved by the national technical committee are NOT
    allowed in the competition area. Being seen using one can get your
    scores pulled.
  - The Computer Programming equipment list itself (2021 AND 2024-26
    editions, both checked) is closed: the committee supplies a printer,
    the programming instructions, and judging procedures; you supply your
    own computer, your coding software, and ONE printed or digital copy of
    a language reference manual. Internet access is never listed as
    provided, and nothing mentions a second device, an AI assistant, or
    any outside tool.

Put together, that's about as close to "no internet, no AI, no outside
tools during skill performance" as it gets without those exact words
appearing -- an AI chatbot open in a browser tab is external assistance
under #29, and a phone or second device running one separately violates
#13 and NC's own no-cell-phones rule.

What's NOT nailed down: the word "AI" itself does not appear anywhere in
any document this trainer could read -- national or NC, including a full
text search of NC's actual 2026 conference program (checked directly, not
inferred). If SkillsUSA or NC has issued AI-specific guidance more
recently than what's indexed on the open web, it wasn't found here.

Bottom line: train assuming you'll have zero internet and zero AI
assistance during skill performance -- everything found points that way
and nothing found contradicts it. For a same-year, no-ambiguity answer,
ask your NC SkillsUSA advisor directly or check updates.skillsusa.org --
that's what the national rulebook itself tells every competitor to do
each year for exactly this kind of detail."""

REAL_PROBLEM_CONVENTIONS = """Patterns that show up over and over in actual contest problems
(drawn from real 2014 and 2021 national packets):
  - A reference table is usually embedded right in the problem: exchange
    rates, a pay-rate-code lookup, a calorie chart, a letter-grade scale.
    Your program is expected to encode that table (dict/list), not
    hardcode one path through it.
  - Specific rounding instructions are given and matter for grading --
    "rounded to the nearest hundredth," "rounded to the nearest whole
    number." Get the rounding wrong and correctness-of-output points are
    lost even if the logic is right.
  - Menu-driven problems traditionally offer Calculate / Clear / Exit (or
    an equivalent reset option) -- "Clear" resets for a new entry without
    restarting the whole program.
  - Multi-session problems (POS/checkout-style) often require the program
    to accumulate totals ACROSS multiple runs through the menu in one
    execution -- e.g. a "Manager" view showing the day's cumulative sales
    across every customer, sometimes gated behind a hardcoded access code.
  - "Find the max/min AND which entry it was" (e.g. "Test #3 was the
    highest score") is a recurring twist on top of plain min()/max() --
    you need the position/label, not just the value.
  - If the real contest project is GUI-based (common in the Visual
    Basic/Java tradition this contest grew out of), every screen must be
    clearly labeled with your contestant number, the program number, and
    the program title, and every input/output box must be labeled. This
    trainer's problems are console-based for auto-grading, but if your
    actual competition hands you a GUI spec, that labeling requirement is
    real and it's graded under "quality of work" and "completeness.\""""

SOURCES = [
    ("SkillsUSA Championships Technical Standards -- Computer Programming, 2024-26 edition",
     "Official national rules currently in force: packet structure, six-criteria rubric, "
     "knowledge-test language list, interview requirement."),
    ("SkillsUSA Championships Technical Standards -- Computer Programming, 2021 edition",
     "Shows the knowledge-test language list before Python was added (Visual Basic, Java, "
     "C++, RPG only) -- confirms Python is a recent addition to this contest."),
    ("2014 National SkillsUSA Computer Information Systems Programming Competition packet "
     "(Kansas City, MO)", "Real national contest programs (Currency Conversion, Payroll) plus "
     "the actual judge sign-off/hand-in process description."),
    ("SkillsUSA Computer Programming Virtual Project packet, 2021",
     "Three full real contest tasks (Calorie Calculator, Student Grade Calculator, Movie "
     "Theater Concessions) used during the pandemic-era virtual format."),
    ("SkillsUSA Championships General Regulations, 2023-24",
     "The baseline rulebook under every competition: independent-work rule (#29), prohibited "
     "electronic devices (#13), clothing/tiebreaker/eligibility rules that apply org-wide."),
    ("SkillsUSA North Carolina 2026 State Conference Program (skillsusanc.org)",
     "NC's own current-year document: confirms Computer Programming is tagged a 'National "
     "Contest' at NC State, and NC's own Code of Conduct wording on cell phones."),
]
