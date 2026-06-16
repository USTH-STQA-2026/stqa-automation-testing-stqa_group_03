# REPORT ON WEB UI AUTOMATED TESTING PROJECT RESULTS

**System:** Library Book Borrowing Management ABC (https://stqa.rbc.vn)
**Subject:** Software Testing and Quality Assurance (STQA)
**Execution Team:** Group 3 (Class: 252ICT2012.L1)

---

## 👥 1. Member List & Task Allocation Matrix

The system recognizes the fair contribution of all 5 members through Work Breakdown Structure (WBS) and cross-checking:

| No. | Full Name | Role | Automation Code Tasks | Theory & Responsibility Tasks | Contribution Ratio |
| --- | --- | --- | --- | --- | --- |
| 1 | Tran Duy Hoang Anh | **Team Leader** | Completed all `tests/test_borrow_return.py` (`TC-08`, `TC-09`, `TC-10`) | Git Setup (Fork repo, configure sample `.env`), Completed **BT4** (Drawing FSM Book Lifecycle state diagram) | 20% |
| 2 | Nguyen Le Hai Anh | **QA Lead** | Completed all `tests/test_general.py` (`TC-11`, `TC-12`) | Gatekeeper (Review Pull Request, scan `time.sleep()` traps, check Weak Oracle), Completed **BT5** & **BT9**, Compiled `REPORT.md` | 20% |
| 3 | Ta Hoang Duy | **Member 3** | Completed `tests/test_login.py` (`TC-02`, `TC-03`) | Researched data from `test-accounts.md`, applied Data-driven technique with `@pytest.mark.parametrize` for empty boundary fields | 20% |
| 4 | Hoang Gia Khanh | **Member 4** | Completed part of `tests/test_search.py` (`TC-04`, `TC-05`) | Researched system requirement specifications for Search Module testing (Part 1) | 20% |
| 5 | Nguyen Trung Hieu | **Member 5** | Completed part of `tests/test_search.py` (`TC-06`, `TC-07`) | Contributed theoretical answers for **BT1** (Box Debate) and **BT2** (RIPR Detective) | 20% |

---

## 📊 2. Test Execution Report

The automated test suite includes **15 scenarios** (12 mandatory scenarios according to the test scenario specification in `ASSIGNMENT.md` and 3 additional bonus scenarios for B1 bonus points).

### 2.1. Overview Statistics

* **Total designed scenarios:** 15
* **Number of PASSED scenarios:** 15
* **Number of FAILED scenarios:** 0
* **Success Rate:** 100%

### 2.2. Detailed Results per Scenario

The team configured to save screenshots as evidence in the `screenshots/` directory after each run flow.

| TC Code | Test Scenario Name | Status | Artifacts | Technical Notes |
| --- | --- | --- | --- | --- |
| **TC-01** | Successful login with valid account | ✅ PASSED | `login_success.png` | Used system default account |
| **TC-02** | Failed login – wrong password | ✅ PASSED | `login_fail_wrong_password.png` | Validated error message "Mật khẩu không đúng" |
| **TC-03** | Failed login – empty data fields | ✅ PASSED | `login_fail_empty_fields_*.png` | Applied `@pytest.mark.parametrize` to scan 3 boundary partitions |
| **TC-04** | Search for books by name — results returned | ✅ PASSED | `tc04_search_by_name.png` | Used keyword "Flutter", verified Semantics text |
| **TC-05** | Search for books by name — no results | ✅ PASSED | `tc05_search_no_result.png` | Cross-checked notification "Không tìm thấy sách" per REQ-03 |
| **TC-06** | Filter books by Category | ✅ PASSED | `tc06_filter_by_category.png` | Used loop to check `aria-label` attribute of cards |
| **TC-07** | Search for books by Author name | ✅ PASSED | `tc07_search_by_author.png` | Validated author keyword "Nguyễn Minh Đức" |
| **TC-08** | Successful book borrowing | ✅ PASSED | `tc08_borrow_success.png` | Used account `dam.tran@email.com` (no books borrowed) |
| **TC-09** | Verify displayed borrowed books list | ✅ PASSED | `TC09_view_borrowed_books.png` | Verified navigation tab switch "Mượn / Trả" |
| **TC-10** | Successful return of borrowed book | ✅ PASSED | `tc10_return_success.png` | Entity state transition cycle completed |
| **TC-11** | Successful Logout | ✅ PASSED | `tc11_logout_success.png` | Verified state returned to initial Login screen |
| **TC-12** | Switch interface language to English | ✅ PASSED | `tc12_switch_language_en.png` | Read Semantics tree structure to scan text "Logout" / "Borrow" |
| **TC-13** | Librarian adds new member successfully | ✅ PASSED | `tc13_add_member_success.png` | **[Bonus B1]** Logged in as Librarian (REQ-07) |
| **TC-14** | Librarian triggers overdue check process | ✅ PASSED | `tc14_check_overdue_triggered.png` | **[Bonus B1]** Executed Librarian special business logic (REQ-06) |
| **TC-15** | Add member failed due to invalid Email format | ✅ PASSED | `tc15_invalid_email_format.png` | **[Bonus B1]** Analyzed syntax error boundary values (REQ-07) |

---

## 🛠 3. Technical Solutions & Test Harness Infrastructure Optimization

Addressing the specific characteristics of the **Flutter Web (CanvasKit renderer)** application, the team thoroughly applied advanced infrastructure techniques to achieve perfect optimization criteria:

1. **Complete removal of `time.sleep()` anti-pattern:** Based on **BT9** research results, the team clearly recognized that `time.sleep()` creates an indeterminate state (non-deterministic), unnecessarily slowing down the CI/CD infrastructure. The team used a **Smart Wait** (`wait_for_flutter()`) function operating on a polling mechanism to synchronize precisely when the Semantics Tree finishes re-rendering.
2. **Building a Strong Oracle Strategy:** To increase the Revealability of the RIPR model, all check points (`assert`) do not stop at just checking the URL or crash-free status (Null/Weak Oracle). The team implemented extraction of all text strings exposed on `flt-semantics` via:
```python
sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
assert "Expected message from SRS" in sem_text

```



## 🛠 4. AI Usage Declaration

The team used the large language model **Gemini**.
Scope of use: AI was used as an assistant (coder) to speed up source code drafting, suggest test function syntax for the Playwright Python library, and assist in configuring HTML formatting for the report document.
Human role (Controller): All Assertions (Oracles) generated by AI were cross-checked and manually standardized by team members according to the software requirement specification document (SRS-library-system.md). The team personally removed all selectors incorrect for the CanvasKit nature and `wait_for_timeout()` functions proposed by AI to protect the deterministic nature of the test suite.
