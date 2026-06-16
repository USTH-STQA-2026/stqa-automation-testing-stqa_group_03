# Group Exercises — Discussion & In-depth Research

> 📖 **Textbook:** Paul Ammann & Jeff Offutt, *Introduction to Software Testing*, 2nd Edition.
> **Objective:** Understand new concepts: **RIPR Model**, **Model-Driven Test Design**, **Test Oracle**.

---

## Exercise 1: The "Box" Debate

> ⏱ **Time:** 15–20 minutes | **Related Chapters:** Ch.2 §2.4–2.5, Ch.6

### Context

We often divide testing into **Black-box** (looking only at the SRS) and **White-box** (looking at the code). However, the authors argue that this boundary is **outdated**:

> *"Thus asking whether a coverage criterion is black-box or white-box is the wrong question. One more properly should ask from what level of abstraction is the structure drawn."*
> — Ammann & Offutt, Ch.2, p.58

### Group Tasks

1. **Open file** `docs/SRS-library-system.md` — this is the "Black-box model".
2. **Read the backend code excerpt** below — this is the "White-box model" (Dart code handling book borrowing business logic):
```dart
// Extracted from library_service.dart — borrowBook() function
ServiceResult<BorrowRecord> borrowBook({required String memberId, required String bookId}) {
  final member = getMemberById(memberId);
  if (member == null) return ServiceResult.error('Member not found.');

  // Check member status
  if (member.status == MemberStatus.expired)
    return ServiceResult.error('Member is expired. Cannot borrow book.');
  if (member.status == MemberStatus.suspended)
    return ServiceResult.error('Member is suspended. Cannot borrow book.');

  final book = getBookById(bookId);
  if (book == null) return ServiceResult.error('Book not found.');
  if (book.status != BookStatus.available)
    return ServiceResult.error('Book is not available for borrowing.');

  // Check borrowing limit
  final currentBorrowCount = _records
      .where((r) => r.memberId == memberId && r.status == BorrowStatus.borrowing)
      .length;
  if (currentBorrowCount >= maxBooksPerMember)  // maxBooksPerMember = 3
    return ServiceResult.error('Reached maximum borrowing limit (3 books).');

  // Create borrow record, update book status
  final record = BorrowRecord(
    memberId: memberId, bookId: bookId,
    borrowDate: DateTime.now(),
    dueDate: DateTime.now().add(Duration(days: 14)),  // borrowDurationDays = 14
  );
  return ServiceResult.ok(record);
}

```


3. **Design 6 test values for the "Borrow Book" feature:**

| # | Origin | Test Value (Description) | Specific Data |
| --- | --- | --- | --- |
| 1 | From SRS (Black-box) | Successful borrowing with active account and available book | `memberId`: MEM003 (`dam.tran@email.com`), `bookId`: BOOK001 |
| 2 | From SRS (Black-box) | Deny borrowing when book is in "Borrowed" status | `memberId`: MEM003 (`dam.tran@email.com`), `bookId`: BOOK003 |
| 3 | From SRS (Black-box) | Deny borrowing when member account status is "Expired" | `memberId`: MEM005 (`binh.pham@email.com`), `bookId`: BOOK001 |
| 4 | From Code (White-box) | Test `member == null` branch condition (Member not found) | `memberId`: "MEM_NON_EXIST", `bookId`: BOOK001 |
| 5 | From Code (White-box) | Test `book == null` branch condition (Book not found) | `memberId`: MEM003, `bookId`: "BOOK_NON_EXIST" |
| 6 | From Code (White-box) | Test upper boundary condition for borrow limit: `currentBorrowCount >= 3` | `memberId`: MEM001 (Already borrowed 3 books), `bookId`: BOOK001 |

4. **Discussion questions:**
a. Are the test values from the SRS and the Code **different**? Do they overlap?
The test values #1, #2, and #3 generated from the SRS perfectly match the business logic branches in the code (the `if` statements checking statuses). However, values #4 and #5 (testing for `null` entities) only appear when looking at the code structure below to protect the system from crashing; the pure business SRS does not describe these missing data cases in detail.
b. Why is asking *"Is this test Black-box or White-box?"* the **wrong question**? What should we ask instead?
Because this boundary creates an artificial division. Both the SRS and the actual source code are **Models** representing the system. Instead of asking which box the approach belongs to, we should ask: *"From which model is the test designed, and from what level of abstraction is the structure drawn?"* to determine the exact coverage criteria.
c. **Hint:** SRS is a **model** at a high level of abstraction, Dart code is a **model** at a low level — both are models. The correct question: *"From which model is the test designed?"*

---

## Exercise 2: The RIPR Detective

> ⏱ **Time:** 15 minutes | **Related Chapters:** Ch.2 §2.1, Ch.14

### Scenario

Your team is testing the "Search Book" feature (`TC-05`: search with no results). You enter the keyword `"xyz_non_existent"` into the search box. Result:

* **Expected Result**: Empty list, no books displayed.
* **Actual Result**: The interface still **displays books from the previous search** (UI bug!).
* **Test Result**: You marked **PASS** because "no error message appeared".

→ The bug exists and is visible on the UI, but you didn't detect it!

### Group Tasks

1. **Draw the 4-step RIPR diagram:**
```
┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ Reachability │ → │  Infection   │ → │ Propagation  │ → │ Revealability│
│   Reach      │   │ Error state  │   │ Propagate to │   │ Reveal to    │
│              │   │  infection   │   │  output      │   │  tester      │
└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
       ✅                 ✅                 ✅                 ❌ ← BROKEN!

```


2. **Discussion questions:**
a. The bug **Reached** → **Infected** → **Propagated** to the UI. Which **step** is broken? Why?
The Revealability step is broken. Although the error propagated to the UI (the UI still displays the old book list), the Tester/Automated Test lacks a strong enough check (Assert) to detect the discrepancy between this actual result and the requirements specification.
b. **Revealability** is broken due to a **weak Test Oracle**: "Expected result" is too generic. Rewrite the Expected Result to be **clear and verifiable**:
|  | Before (weak) | After (strong) |
| --- | --- | --- |
| Expected result | "No error" | The interface must display the error message "Book not found," and the entire list of book cards (flt-semantics[role="group"]) from the previous search must be completely removed from the screen. |


c. If you are doing **automation** (Exercise A2), what does the `assert` line in the code correspond to in manual testing? (Hint: "Expected result" = Test Oracle)
The assert command in automated testing is the concrete realization of the Test Oracle (Expected Result) in manual testing. It acts as the ultimate judge determining the correctness of the software at runtime.

---

## Exercise 3: Who guards the software? (Test Suite vs SRS)

> ⏱ **Time:** 15 minutes | **Related Chapters:** Ch.4 §4.2

### Context

According to Agile and TDD perspectives:

> *"In agile methods, test cases are the de facto specification for the system."*
> — Ammann & Offutt, Ch.4, p.99

### Group Tasks

1. **Consider 12 Test Cases** (TC-01 → TC-12) described in the SRS:
| Functional Group | TCs | Function |
| --- | --- | --- |
| Login | TC-01, TC-02, TC-03 | Successful/Failed login |
| Search & Filter | TC-04 ~ TC-07 | Search by name/author, filter by category |
| Borrow & Return | TC-08, TC-09, TC-10 | Borrow book, view list, return book |
| General Functions | TC-11, TC-12 | Logout, switch language |


2. **Discussion questions:**
a. If `SRS-library-system.md` **is deleted**, could a new developer **only look** at TC-08 ~ TC-10 to recode the book borrow/return feature? Why?
Not entirely. Because test case scenarios only record end-to-end behavior of a specific data flow, not all implicit boundary constraints (e.g., precise overdue date calculation logic, email/phone regex constraints, or in-memory data states wiped when refreshing a tab).
b. List **business information** revealed by `TC-08` (Borrow Book):
| # | Information (read from test) | Source |
|---|---|---|
| 1 | The user must perform a successful login before having permission to click the borrow button. | `login(page, test_config)` |
| 2 | The button triggering the borrow behavior has the text label `"Borrow this book"`. | `has-text("Borrow this book")` |
| 3 | The system requires an intermediate confirmation step by clicking the `"Borrow"` button in a dialog window. | `has-text("Borrow")` |
c. **Limitations**: Where is the "Test as specification" perspective weak?
* Negative user interaction scenarios not thought of?
* Non-functional requirements (performance, security)?
* Business changes not reflected in tests?
*Lack of advanced negative scenarios:* Test suites usually focus on covering main flows, easily missing atypical user interaction cases if the tester hasn't planned for them.
*Non-functional requirements left empty:* Functional test code cannot describe load performance metrics, data encryption security, or device compatibility.
*Documentation update latency:* When business processes change suddenly but the tester hasn't updated the test code in time, the test documentation will completely inaccurately reflect the desired business state.
d. **Group conclusion:** Should SRS and Test Suite **coexist** or is only 1 of the 2 needed? Explain.
**They must coexist in parallel.** The SRS acts as the "Source of Truth" shaping all business objectives at a high level of abstraction for the entire project. Meanwhile, the Test Suite acts as a "Living Guardian," continuously verifying the actual operational mechanism at a low level, ensuring the code never regresses.



---

## Exercise 4: The Book Lifecycle FSM

> ⏱ **Time:** 20 minutes | **Related Chapters:** Ch.7 §7.5.2 (p.223–234)

### Context

Each book in the system goes through different states — this is a **Finite State Machine (FSM)**:

> *"A Finite State Machine is a graph whose nodes represent states... and edges represent transitions among the states."*
> — Ammann & Offutt, Ch.7 §7.5.2, p.224

### Step 1: States and Transitions

| Symbol | State | State (EN) | Example in seed data |
| --- | --- | --- | --- |
| **S1** | Available | Available | BOOK001, BOOK002 |
| **S2** | Borrowed | Borrowed | BOOK003 |
| **S3** | Overdue | Overdue | When not returned after 14 days |
| **S4** | Lost | Lost | BOOK007 |

| Symbol | Event | Trigger (EN) | From → To |
| --- | --- | --- | --- |
| **T1** | Borrow | Borrow | S1 → S2 |
| **T2** | Return (on time) | Return (on time) | S2 → S1 |
| **T3** | Check overdue | Check overdue | S2 → S3 |
| **T4** | Return (late) | Return (late) | S3 → S1 |
| **T5** | Mark as lost | Mark as lost | S3 → S4 |

### Step 2: Draw the FSM diagram

```
                    T1: Borrow                  T3: Overdue
              ┌─────────────────┐         ┌──────────────────┐
              │                 ▼         │                  ▼
         ┌─────────┐       ┌─────────┐       ┌─────────┐       ┌─────────┐
   ●───→ │   S1    │       │   S2    │       │   S3    │       │   S4    │
         │ Available│ ◀──── │ Borrowed│       │ Overdue │ ────→ │  Lost   │
         │         │  T2:  │         │       │         │  T5:  │         │
         └─────────┘ Return└─────────┘       └────┬────┘ Lost  └─────────┘
              ▲              book                  │
              │                                    │
              └────────────────────────────────────┘
                        T4: Return (late)

```

### Step 3: Test Paths for Edge Coverage

Derive test paths so that **each transition is executed at least once** (Transition Coverage = Edge Coverage, Ch.7 §7.2.1):

| Test Path | State Sequence | Covered Transitions |
| --- | --- | --- |
| **TP1** | $S1 \rightarrow S2 \rightarrow S1$ | $T1$ (Borrow), $T2$ (Return on time) |
| **TP2** | $S1 \rightarrow S2 \rightarrow S3 \rightarrow S1$ | $T1$ (Borrow), $T3$ (Check overdue), $T4$ (Return late) |
| **TP3** | $S1 \rightarrow S2 \rightarrow S3 \rightarrow S4$ | $T1$ (Borrow), $T3$ (Check overdue), $T5$ (Mark as lost) |

### Step 4: Mapping with Test Cases

| Test Path | Corresponding TC | Covered? |
| --- | --- | --- |
| **TP1** (borrow → return) | `TC-08` (Borrow) combined with `TC-10` (Return) | ✅ Covered |
| **TP2** (overdue → return) | `TC-14` (Librarian check overdue) combined with late return scenario | ✅ Covered via extended test suite |
| **TP3** (overdue → lost) | Mark as lost scenario from Librarian side | ❌ Not covered in basic flow |

### Discussion questions

a. **Which transitions** lack TC coverage? Design new TCs for them.
Transition T5 (Mark as lost from overdue state) lacks mandatory test case coverage. New TC design: Log in as `librarian@library.com`, access the overdue loan list, select the record of the entity currently overdue, and click the "Mark as lost" action button ==> Assert book status changes to `Lost`.
b. The system has **BUG-07** (off-by-one in overdue check) — which transition does this bug lie in? Why does Edge Coverage **force** testing that transition?
This bug lies directly in transition **T3 (Check overdue)**. Since Edge Coverage requires every state transition arrow to be triggered at least once, it forces the tester to design test values that fall exactly on the due date boundary (`dueDate == current date`). Consequently, the infection state of the date comparison algorithm will be triggered and revealed in the output.
c. If adding a "Recover book" feature (S4 → S1), how does the FSM change?
The graph will include a new directed edge from node S4 (Lost) back to node S1 (Available). The trigger event for this edge would be the business function "Recover book/Restore book from warehouse."

---

## Exercise 5: The Oracle Strength Challenge

> ⏱ **Time:** 15 minutes | **Related Chapters:** Ch.14 §14.1 (p.410–413)

### Context

> *"Some software organizations only check to see whether the software produces a runtime exception, or crashes. This has been called the null oracle strategy. [...] only between 25% to 56% of software failures result in a crash."*
> — Ammann & Offutt, Ch.14 §14.1, p.412

### Scenario: TC-06 — Filter books by category "Technology"

Compare 3 oracle levels:

```python
# === Oracle A: Null Oracle — check "no crash" ===
page.locator('flt-semantics[role="group"]').first.wait_for()
# No assert → PASS if no exception

# === Oracle B: Weak Oracle — check "result exists" ===
results = page.locator('flt-semantics[role="group"]')
assert results.count() > 0, "No result"

# === Oracle C: Strong Oracle — check result CONTENT ===
results = page.locator('flt-semantics[role="group"]')
assert results.count() > 0, "No result"
for i in range(results.count()):
    label = results.nth(i).get_attribute("aria-label")
    assert "Technology" in label, f"Book '{label}' is not in Technology category"

```

### Group Tasks

1. **Classification:** Which Oracle detects BUG-06 (case-sensitive filter)?
| Oracle | Level | Detects BUG-06? | Explanation |
|--------|------|-------------------|------------|
| **A** | `Null Oracle` | ❌ **No** | The case-sensitive filter bug only returns an empty list rather than causing a source code crash or runtime exception. |
| **B** | `Weak Oracle` | ❌ **No** | If the filter incorrectly returns a count of book cards $> 0$ but contains only books from other categories (e.g., Economics), the count check assertion still passes incorrectly. |
| **C** | `Strong Oracle`| ✅ **Yes** | The deep traversal loop will extract the `aria-label` string of each displayed result card to precisely match the keyword "Technology." If there is a mismatch, it triggers Fail immediately. |
2. According to the textbook, does Oracle C need to check **all** books? Or only output **directly related** to the test objective?
According to the textbook (Chapter 14), Oracle C does not need to (and should not) check the entire global database aimlessly. It only needs to focus on strictly checking the integrity of the output data set (Output Filtered System Space) **directly related** to the goal and scope of that test case to ensure CI/CD performance.
3. In `tests/test_search.py`, find the current assertion for TC-06. What Oracle level is it? Can it be improved?
The current assertion for `TC-06` in the project has been upgraded by the team to **Strong Oracle**. It uses a loop to scan and extract label attributes:
```python
for i in range(books.count()):
    label = books.nth(i).get_attribute("aria-label")
    assert "Technology" in label

```


An improvement is to combine this with the `wait_for_flutter(page, text="Code: BOOK")` Smart Wait function immediately above to thoroughly replace hard waits, avoiding synchronization issues when Flutter has not finished rendering attributes.

---

## Exercise 6: Regression Test Selection

> ⏱ **Time:** 15 minutes | **Related Chapters:** Ch.13 (p.406–409)

### Context

> *"Regression testing constitutes the vast majority of testing effort... small changes to one part of a system often cause problems in distant parts of the system."*
> — Ammann & Offutt, Ch.13, p.406

### Hypothetical Scenario

> **Change V1.1:** Maximum number of borrowed books reduced from **3** to **2**.

```dart
// V1.0 (old): static const int maxBooksPerMember = 3;
// V1.1 (new): static const int maxBooksPerMember = 2;

```

### Group Tasks

1. **Classify 12 Test Cases:**
| TC | Description | Will FAIL? | Must Rerun? | Reason |
|-----|-------|---------|---------------|-------|
| **TC-01** | Successful Login | ❌ No | ✅ Yes | Part of the base Regression Test suite (Sanity check) to ensure core functionality is not broken after system update. |
| **TC-02** | Wrong Password Login | ❌ No | ❌ No | Password verification logic is completely independent of the book limit parameter. |
| **TC-03** | Empty Login | ❌ No | ❌ No | Empty form check logic is unaffected. |
| **TC-04** | Search with results | ❌ No | ❌ No | Search module is independent of the borrowing limit business logic. |
| **TC-05** | Search without results | ❌ No | ❌ No | Not affected by book borrowing configuration. |
| **TC-06** | Filter by category | ❌ No | ❌ No | Not affected by book borrowing configuration. |
| **TC-07** | Search by author | ❌ No | ❌ No | Not affected by book borrowing configuration. |
| **TC-08** | Normal Borrow | ❌ No | ✅ Yes | Must rerun because this function directly executes the borrow business logic; need to ensure borrowing 1st and 2nd books still works smoothly. |
| **TC-09** | View borrowed list | ❌ No | ❌ No | Only displays raw data from existing borrow records. |
| **TC-10** | Return book | ❌ No | ❌ No | Book return logic back to storage is not affected by the upper limit constraint. |
| **TC-11** | Logout | ❌ No | ❌ No | Unrelated to borrowing business parameters. |
| **TC-12** | Switch language | ❌ No | ❌ No | Unrelated to borrowing business parameters. |
2. **Discussion questions:**
a. Which TC is **certain to FAIL** due to the change?
Among the 12 basic interface scenarios, **no scenario is certain to FAIL**, because `TC-08` only tests the flow of successfully borrowing 1 book (which still satisfies the limit $\le 2$). However, if there were an advanced scenario testing the boundary of borrowing a 4th book (assuming the old system blocked from the 4th book), that scenario would FAIL because the new system logic must block from the 3rd book.
b. `TC-08` (normal borrow) doesn't FAIL — but why must it **still be rerun**?
Because the configuration change happens directly inside the handler function for the borrow feature. Rerunning `TC-08` is mandatory to perform Regression Testing, proving that the system configuration modification did not accidentally break or crash the borrow flow in normal cases.
c. If 12 TCs are **automated** (~2–3 minutes) vs **manual** (~2–3 hours), which strategy is more reasonable: Retest-All or Selective?
If using **Automation:** **Retest-All** is optimal because the time cost is negligible (~2-3 minutes), helping free up analysis pressure and ensuring absolute safety.
If using **Manual:** **Selective** is mandatory to optimize human resources, avoiding wasted time on completely isolated modules like Login/Language.

---

## Exercise 7: Kill the Mutant

> ⏱ **Time:** 15 minutes | **Related Chapters:** Ch.9 §9.1.2 (p.322), §9.2.2 (p.336)

### Context

**ROR (Relational Operator Replacement)**:

> *"Replace each occurrence of one of the relational operators (<, ≤, >, ≥, ==, ≠) by each of the other operators."*
> — Ammann & Offutt, Ch.9 §9.2.2, p.336

### Situation 1: BUG-02 — Borrowing Limit

```dart
// Code correct (per SRS): >= 3 → deny
if (currentBorrowCount >= maxBooksPerMember)

// Code actual (mutant ROR: >= → >): > 3 → allow borrowing 4th book!
if (currentBorrowCount > maxBooksPerMember)

```

| Current borrowed count | Code correct (`>=`) | Code faulty (`>`) | Kill mutant? |
| --- | --- | --- | --- |
| 2 | Allow | Allow | No — same result |
| 3 | **Deny** | **Allow** | ✅ **Yes (Kill!)** — Different output state. |
| 4 | Deny | Deny | No — same result |

### Situation 2: BUG-07 — Overdue Check

```dart
// Code correct: today >= due date → overdue
if (!now.isBefore(record.dueDate))

// Code actual (mutant): today > due date
if (now.isAfter(record.dueDate))

```

Borrowed 1/9, due 15/9. On what date do you kill the mutant?

| Check date | Code correct | Code faulty | Kill? |
| --- | --- | --- | --- |
| 14/9 | Not overdue | Not overdue | No — same result |
| **15/9** | **Overdue** | **Not overdue** | ✅ **Yes (Kill!)** — Different output state at boundary. |
| 16/9 | Overdue | Overdue | No — same result |

### Summary questions

a. Where do test values that kill mutants always lie? (Hint: **boundary values** — BVA, Ch.6)
Test values used to kill relational operator mutants always lie exactly at **Business Boundary Values**.
b. Why *"good test data design using BVA automatically kills most ROR mutants"*?
Because Boundary Value Analysis (BVA) forces testers to select data points lying right on the edge of the logic expression's decision change. Relational operator mutants (like changing `>=` to `>`) only shift the boundary point by exactly one unit, so boundary data will immediately catch this behavioral discrepancy.
c. **RIPR connection:** Boundary values ensure **Infection** (different state between correct and faulty code). If using values far from the boundary (e.g., 0), why does the mutant **survive**?
When using test values far from the boundary (e.g., borrowed book count is 0 or 1), both the correct code expression (`currentBorrowCount >= 3`) and the faulty mutant expression (`currentBorrowCount > 3`) yield the same logic result of `False` (System allows borrowing). Consequently, no data discrepancy appears in memory => **The Infection step (Error state infection) does not occur**, the error cannot propagate and be revealed, leading the mutant to survive.

---

## Exercise 8: The Logic Trap

> ⏱ **Time:** 20 minutes | **Related Chapters:** Ch.8 §8.1.1 (p.248), §8.1.2 (p.250–253)

### Theoretical Context

The textbook emphasizes: only testing the entire true/false expression (**Predicate Coverage**) is not enough — because individual **clauses** inside may hide bugs that are never detected:

> *"An obvious failing of this criterion is that the individual clauses are not always exercised."*
> — Ammann & Offutt, Ch.8 §8.1.1, p.248

The concept of **determination** allows detecting bugs in individual clauses:

> *"The key notion is that of determination, the conditions under which a clause influences the outcome of a predicate. [...] if you flip the clause, and the predicate changes value, then the clause determines the predicate."*
> — Ammann & Offutt, Ch.8 §8.1.2, p.250

This is the basis of **Active Clause Coverage (ACC)** — also known as **MC/DC (Modified Condition/Decision Coverage)**, a mandatory standard in aviation software (FAA DO-178C):

> *"Active Clause Coverage (ACC): For each p ∈ P and each major clause ci ∈ Cp, choose minor clauses cj, j ≠ i so that ci determines p. TR has two requirements for each ci: ci evaluates to true and ci evaluates to false."*
> — Ammann & Offutt, Ch.8, Definition 8.42, p.251

### Scenario: REQ-04 — Borrow Book

The condition to **allow successful book borrowing** is a logic expression consisting of 3 clauses:

$$P = A \wedge B \wedge C$$

| Clause | Meaning | True Example | False Example |
| --- | --- | --- | --- |
| **A** | Book is available (`book.status == available`) | BOOK001 | BOOK003 (borrowed) |
| **B** | Not reached limit (`borrowCount < max`) | MEM002 (0 books) | MEM001 (borrowed 3 books) |
| **C** | Member active (`member.status == active`) | MEM001 | MEM004 (suspended) |

### Group Tasks

1. **Step 1 — Predicate Coverage (PC):** Only 2 test cases needed:
| TC | A | B | C | $P = A \wedge B \wedge C$ | Result |
| --- | --- | --- | --- | --- | --- |
| TC-α | T | T | T | **True** | Allow ✅ |
| TC-β | F | F | F | **False** | Deny ❌ |


**Question:** With only these 2 TCs, what system bug might you **not detect**?
You would completely overlook hidden bugs in independent clauses when they are overwritten by logic. For example: If the programmer incorrectly hardcodes clause $C$ to `True` (ignoring the check for suspended/expired member status), the two scenarios $TC-\alpha$ and $TC-\beta$ would still PASS normally → Bug slips through due to coarse coverage.
2. **Step 2 — Active Clause Coverage (ACC):** To test each clause, you must **isolate** it — keep the other clauses at values that allow the tested clause to **determine** the result.
**Fill in the following truth table:**
| TC | A | B | C | $P$ | Major clause tested | Explanation |
|----|---|---|---|-----|----------------------|-----------|
| 1 | **T** | T | T | True | A (True → P True) | Pair with TC2 |
| 2 | **F** | T | T | **False** | A (False → P **False**) | Flip A, B and C stay T: P changes. |
| 3 | T | **T** | T | True | B (True → P True) | Pair with TC4 |
| 4 | T | **F** | T | **False** | B (False → P **False**) | Flip B, A and C stay T: P changes. |
| 5 | T | T | **T** | True | C (True → P True) | Pair with TC6 |
| 6 | T | T | **F** | **False** | C (False → P **False**) | Flip C, A and B stay T: P changes. |
> **Note:** Many TCs may overlap. After removing duplicates, how many test cases does ACC need for `A AND B AND C` at minimum?
> After removing lines identical in configuration (`TC 1`, `TC 3`, `TC 5` are the same), ACC coverage for the logic expression `A AND B AND C` needs at least **4 independent test cases** to complete.


3. **Step 3 — Detect bug BUG-04:**
Actual system bug: BUG-04 — "Suspended" member receives wrong error message ("Member expired" instead of "Member suspended"). Which TC in the ACC table above will **detect** BUG-04? Do `TC-α` and `TC-β` of Predicate Coverage detect it?
Scenario **`TC 6`** in the ACC truth table (Configuration: $A=True$, $B=True$, $C=False$ — corresponding to the case where the book is available, limit not reached, but account is suspended) will **detect BUG-04**.
Both `TC-alpha` and `TC-beta` of Predicate Coverage **absolutely cannot detect** this bug because `TC-alpha` only tests the entirely correct flow, while `TC-beta`, by flipping all 3 variables to `False` simultaneously, causes the system to branch and return the error message of variable A or B before reaching the error-checking segment for variable $C$.

### Discussion questions

a. With `A AND B AND C`, Predicate Coverage needs 2 TCs, ACC needs how many? Why is the increase **worth it**?
Predicate Coverage needs 2 TCs, ACC needs at least 4 TCs. This increase is absolutely worth it because it helps isolate and independently verify the deciding power of each individual business condition, ensuring no faulty logic lines are hidden by preceding clauses.
b. In practice, FAA requires **MC/DC** (equivalent to ACC) for flight control software. Why is using only Predicate Coverage for aviation software **dangerous**?
Because aviation software requires extreme absolute safety. If only Predicate Coverage is used, hidden logic combinations (e.g., faulty pitch angle sensor hidden by velocity conditions) will never be triggered during testing. In real-world conditions, if sub-clauses fall into a logic blind spot simultaneously, the system will make wrong decisions leading to airplane disaster.
c. **Connect to Exercise 7 (Mutation):** If a programmer writes `OR` instead of `AND` — is this an **ROR mutant**? What test values kill this mutant?
This is not an ROR mutant but belongs to **BOM Mutants (Boolean Operator Mutants)** - replacing logical operators. To kill this mutant, we use test values with configurations that make the two expressions yield inverse results. Specifically, configurations with 1 `False` clause and the others `True` (e.g., `[F, T, T]`, `[T, F, T]`, `[T, T, F]`). At this point, the correct `AND` code returns `False`, while the faulty `OR` mutant code returns `True` $\rightarrow$ Mutant killed.

---

## Exercise 9: Flaky Tests

> ⏱ **Time:** 10 minutes (Exit Ticket) | **Related Chapters:** Ch.4 §4.2 (p.98–100)

### Theoretical Context

According to the textbook, the test harness acts as a "guardian" — but only if it is **reliable**:

> *"Test automation is a prerequisite for test-driven development. [...] the correctness of the system at any single point in time is subject to immediate verification simply by running the test set."*
> — Ammann & Offutt, Ch.4 §4.2, p.98

> *"Not only do our tests need to be good—they also need to be fast!"*
> — Ammann & Offutt, Ch.4 §4.2.1, p.100

But if a test **PASSes** sometimes and **FAILs** others (without changing code) — that is a **Flaky Test**. Flaky tests **destroy** the Guardian role because programmers will lose trust: *"It failed again, probably just flaky"* → ignoring real bugs.

### Scenario: Flutter Web CanvasKit

The library system uses Flutter Web with the **CanvasKit** renderer (drawing UI on `<canvas>`). Unlike regular HTML DOM, Flutter updates the **Semantics Tree** with non-fixed latency.

File `conftest.py` has a **Smart Wait** function:

```python
def wait_for_flutter(page, text=None, selector=None, timeout=10000):
    """Smart Wait: wait for Flutter Semantics Tree update."""
    if text:
        page.locator(
            f'flt-semantics:has-text("{text}"), flt-semantics[aria-label*="{text}"]'
        ).first.wait_for(state="attached", timeout=timeout)
    elif selector:
        page.locator(selector).first.wait_for(state="attached", timeout=timeout)
    else:
        page.locator("flt-semantics").first.wait_for(state="attached", timeout=timeout)

```

### Group Tasks (Exit Ticket)

1. **Imaginary experiment:** If you replace `wait_for_flutter(page, text="Logout")` with `time.sleep(0.1)` and run `pytest -v` 10 times in a row, what will happen?
| Run | `wait_for_flutter` (Smart Wait) | `time.sleep(0.1)` (Hard Sleep) |
|----------|-------------------------------|-------------------------------|
| 1 | ✅ PASS | ❌ **FAIL** (If CPU is busy, Flutter hasn't loaded Semantics) |
| 2 | ✅ PASS | ✅ **PASS** (If CPU is idle, processing finished in 0.05s) |
| 3 | ✅ PASS | ❌ **FAIL** (Canvas render latency exceeds 0.12s) |
| ... | ✅ PASS | ✅ **PASS** |
| 10 | ✅ PASS | ❌ **FAIL** |
2. **Technical explanation:** Why is `wait_for_flutter` **deterministic** while `time.sleep(0.1)` is **non-deterministic**?
`wait_for_flutter` is a **Deterministic Polling** mechanism. It actively locks onto the state of the Semantics Tree, only proceeding when the target element actually attaches successfully to the hidden DOM tree.
`time.sleep(0.1)` is a **Non-deterministic Hard Sleep** mechanism. It is completely blind to system state, baselessly assuming all render tasks always finish under 100ms. In real CI/CD environments, hardware resources are shared, causing response times to vary continuously, creating flakiness.
3. **Connect to Ch.4:** The author says tests must *"be good AND fast"*. If you use `time.sleep(5)` (long wait) to avoid flakiness, which factor do you sacrifice? If the CI system runs 12 TCs × 5 seconds per step × 10 steps = how many minutes? Is there still **"immediate verification"**?
If using a solution that increases hard wait time to `time.sleep(5)`, we are **directly sacrificing the CI Speed** of the test harness.

* **Calculation of CI runtime:**
Wasted time = 12 TCs * 5 seconds/step * 10 steps = 600 seconds = 10 minutes.
The test suite now takes over 10 minutes just to run 12 simple scenarios. The system completely **loses the "Immediate verification" feature** — the core philosophy of Agile/TDD testing, turning CI/CD into a bottleneck that slows down the delivery progress of the entire project.

4. **Multiple choice question (choose 1):** Which test architecture component does `wait_for_flutter` belong to?
* (a) Test Oracle
* (b) Test Driver
* (c) Test Harness infrastructure   ==> correct
* (d) Test Data



---

## Appendix: Mapping Exercise ↔ Textbook

| Exercise | Main Concept | Chapter |
| --- | --- | --- |
| BT1: Box Debate | MDTD, Level of Abstraction | Ch.2 §2.4–2.5, Ch.6 |
| BT2: RIPR Detective | RIPR Model, Test Oracle, Revealability | Ch.2 §2.1, Ch.14 |
| BT3: Test as Guardian | Test Harness, De facto Specification | Ch.4 §4.2 |
| **BT4: Book Lifecycle FSM** | **FSM, State/Transition Coverage, Test Path** | **Ch.7 §7.5.2, §7.2.1** |
| **BT5: Oracle Strength** | **Null Oracle, Oracle Precision, Revealability** | **Ch.14 §14.1** |
| **BT6: Regression Selection** | **Regression Testing, Test Selection, CI** | **Ch.13, Ch.4 §4.2** |
| **BT7: Kill the Mutant** | **Mutation Testing, ROR, BVA ↔ Mutation** | **Ch.9 §9.1.2, §9.2.2, Ch.6** |
| **BT8: The Logic Trap** | **Predicate/Clause/Active Clause Coverage, MC/DC** | **Ch.8 §8.1.1, §8.1.2** |
| **BT9: Flaky Tests** | **Test Harness, Deterministic Testing, CI Speed** | **Ch.4 §4.2, §4.2.1** |
