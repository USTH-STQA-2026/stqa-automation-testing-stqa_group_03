# AUTOMATED UI TESTING PROJECT REPORT

**System:** Library Book Borrowing Management System ([https://stqa.rbc.vn](https://stqa.rbc.vn))

**Subject:** Software Testing and Quality Assurance (STQA)

**Team:** Team 3 (Class: 252ICT2012.L1)

---

## 👥 1. Member List & Task Distribution Matrix

The system records the equitable contribution of all 5 members through Work Breakdown Structure (WBS) and cross-review:

| No. | Full Name | Role | Automation Coding Tasks | Theoretical & Responsibility Tasks | Contribution Ratio |
| --- | --- | --- | --- | --- | --- |
| 1 | Tran Duy Hoang Anh | **Team Leader** | Completed all `tests/test_borrow_return.py` (`TC-08`, `TC-09`, `TC-10`) | Git Setup (Fork repo, config sample `.env`), Completed **BT4** (Drawing FSM Book Lifecycle state diagram) | 20% |
| 2 | Nguyen Le Hai Anh | **QA Lead** | Completed all `tests/test_general.py` (`TC-11`, `TC-12`) | Gatekeeper (Review Pull Requests, scan for `time.sleep()` anti-patterns, check Weak Oracle), Completed **BT5** & **BT9**, Compiled `REPORT.md` | 20% |
| 3 | Ta Hoang Duy | **Member 3** | Completed `tests/test_login.py` (`TC-02`, `TC-03`) | Researched data from `test-accounts.md`, applied Data-driven techniques with `@pytest.mark.parametrize` for boundary conditions | 20% |
| 4 | Hoang Gia Khanh | **Member 4** | Completed part of `tests/test_search.py` (`TC-04`, `TC-05`) | Researched system requirement specification documents for the Search Module testing (Part 1) | 20% |
| 5 | Nguyen Trung Hieu | **Member 5** | Completed part of `tests/test_search.py` (`TC-06`, `TC-07`) | Contributed theoretical answers for **BT1** (Box Debate) and **BT2** (RIPR Detective) | 20% |

---

## 📊 2. Test Execution Report

The automated test suite includes **15 scenarios** (12 mandatory scenarios based on the testing specification in `ASSIGNMENT.md` and 3 advanced scenarios for Bonus B1).

### 2.1. Overview Statistics

* **Total test scenarios:** 15
* **PASSED scenarios:** 15
* **FAILED scenarios:** 0
* **Success Rate:** 100%

### 2.2. Detailed Scenario Results

The team configured screenshots to be saved in the `screenshots/` directory after each execution flow.

| TC ID | Test Scenario Name | Status | Artifacts | Technical Notes |
| --- | --- | --- | --- | --- |
| **TC-01** | Successful login with valid account | ✅ PASSED | `login_success.png` | Used system default account |
| **TC-02** | Failed login – wrong password | ✅ PASSED | `login_fail_wrong_password.png` | Validated error message "Mật khẩu không đúng" |
| **TC-03** | Failed login – empty fields | ✅ PASSED | `login_fail_empty_fields_*.png` | Applied `@pytest.mark.parametrize` for 3 boundary partitions |
| **TC-04** | Search book by title — result found | ✅ PASSED | `tc04_search_by_name.png` | Used keyword "Flutter", verified Semantics text |
| **TC-05** | Search book by title — no result | ✅ PASSED | `tc05_search_no_result.png` | Matched message "Không tìm thấy sách" per REQ-03 |
| **TC-06** | Filter books by Category | ✅ PASSED | `tc06_filter_by_category.png` | Iterated to check `aria-label` attribute of cards |
| **TC-07** | Search book by Author | ✅ PASSED | `tc07_search_by_author.png` | Verified author keyword "Nguyễn Minh Đức" |
| **TC-08** | Borrow book successfully | ✅ PASSED | `tc08_borrow_success.png` | Used account `dam.tran@email.com` (no prior loans) |
| **TC-09** | Verify displayed borrowed books list | ✅ PASSED | `TC09_view_borrowed_books.png` | Verified navigation tab "Mượn / Trả" |
| **TC-10** | Return borrowed book successfully | ✅ PASSED | `tc10_return_success.png` | Entity state transition cycle completed |
| **TC-11** | Logout successfully | ✅ PASSED | `tc11_logout_success.png` | Verified state returned to initial Login screen |
| **TC-12** | Switch interface language to English | ✅ PASSED | `tc12_switch_language_en.png` | Read Semantics tree to scan for "Logout" / "Borrow" text |
| **TC-13** | Librarian adds new member successfully | ✅ PASSED | `tc13_add_member_success.png` | **[Bonus B1]** Logged in as Librarian (REQ-07) |
| **TC-14** | Librarian triggers overdue check process | ✅ PASSED | `tc14_check_overdue_triggered.png` | **[Bonus B1]** Executed special Librarian operations (REQ-06) |
| **TC-15** | Add member failed due to invalid Email format | ✅ PASSED | `tc15_invalid_email_format.png` | **[Bonus B1]** Analyzed syntax error boundary values (REQ-07) |

---

## 🛠 3. Technical Solutions & Test Harness Infrastructure Optimization

To address the specific nature of the **Flutter Web (CanvasKit renderer)** application, the team applied advanced infrastructure techniques to achieve perfect scores in optimization criteria:

1. **Complete removal of `time.sleep()` anti-pattern:** Based on **BT9** research, the team acknowledged that `time.sleep()` creates non-deterministic pauses, unnecessarily slowing down the CI/CD pipeline. The team implemented **Smart Wait** (`wait_for_flutter()`) using a polling mechanism to synchronize precisely when the Semantics Tree completes re-rendering.
2. **Strong Oracle Strategy:** To enhance the revealability of the RIPR model, all assertions do not merely check URLs or crash status (Null/Weak Oracle). The team implemented extraction of all text displayed on `flt-semantics` via:
```python
sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
assert "Expected message from SRS" in sem_text

```



## 🛠 4. AI Usage Declaration

The team utilized the **Gemini** large language model.
Scope of use: AI was used as an assistant ("coder") to accelerate source code drafting, suggest Playwright Python library testing syntax, and assist in configuring HTML formatting for the report document.
Human role (Controller): All Assertions (Oracles) generated by AI were reviewed and manually standardized by team members according to the software requirement specification (SRS-library-system.md). The team manually removed all selectors incorrect for CanvasKit and `wait_for_timeout()` functions suggested by AI to ensure the deterministic nature of the test suite.
