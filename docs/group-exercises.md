# Bài tập nhóm — Thảo luận & Nghiên cứu sâu

> 📖 **Textbook:** Paul Ammann & Jeff Offutt, *Introduction to Software Testing*, 2nd Edition.
>
> **Mục tiêu:** Hiểu các khái niệm mới: **RIPR Model**, **Model-Driven Test Design**, **Test Oracle**.

---

## Bài tập 1: Cuộc chiến của những chiếc hộp (The "Box" Debate)

> ⏱ **Thời gian:** 15–20 phút | **Chương liên quan:** Ch.2 §2.4–2.5, Ch.6

### Bối cảnh

Chúng ta thường chia kiểm thử thành **Hộp đen** (Black-box — chỉ nhìn SRS) và **Hộp trắng** (White-box — nhìn code). Nhưng tác giả cho rằng ranh giới này **lỗi thời**:

> *"Thus asking whether a coverage criterion is black-box or white-box is the wrong question. One more properly should ask from what level of abstraction is the structure drawn."*
> — Ammann & Offutt, Ch.2, p.58

### Nhiệm vụ nhóm

1. **Mở file** `docs/SRS-library-system.md` — đây là "Black-box model".

2. **Đọc đoạn trích code backend** dưới đây — đây là "White-box model" (code Dart xử lý nghiệp vụ mượn sách):

   ```dart
   // Trích từ library_service.dart — hàm borrowBook()
   ServiceResult<BorrowRecord> borrowBook({required String memberId, required String bookId}) {
     final member = getMemberById(memberId);
     if (member == null) return ServiceResult.error('Không tìm thấy thành viên.');

     // Kiểm tra trạng thái thành viên
     if (member.status == MemberStatus.expired)
       return ServiceResult.error('Thành viên đã hết hạn. Không thể mượn sách.');
     if (member.status == MemberStatus.suspended)
       return ServiceResult.error('Thành viên đang bị tạm ngưng. Không thể mượn sách.');

     final book = getBookById(bookId);
     if (book == null) return ServiceResult.error('Không tìm thấy sách.');
     if (book.status != BookStatus.available)
       return ServiceResult.error('Sách không có sẵn để mượn.');

     // Kiểm tra giới hạn mượn
     final currentBorrowCount = _records
         .where((r) => r.memberId == memberId && r.status == BorrowStatus.borrowing)
         .length;
     if (currentBorrowCount >= maxBooksPerMember)  // maxBooksPerMember = 3
       return ServiceResult.error('Đã đạt giới hạn mượn tối đa (3 sách).');

     // Tạo phiếu mượn, cập nhật trạng thái sách
     final record = BorrowRecord(
       memberId: memberId, bookId: bookId,
       borrowDate: DateTime.now(),
       dueDate: DateTime.now().add(Duration(days: 14)),  // borrowDurationDays = 14
     );
     return ServiceResult.ok(record);
   }
   ```

3. **Thiết kế 6 giá trị test cho tính năng "Mượn sách":**

| # | Nguồn gốc | Test Value (Mô tả) | Dữ liệu cụ thể |
|---|---|---|---|
| 1 | Từ SRS (Black-box) | Mượn sách thành công với tài khoản hoạt động và sách có sẵn | `memberId`: MEM003 (`dam.tran@email.com`), `bookId`: BOOK001 |
| 2 | Từ SRS (Black-box) | Từ chối mượn khi sách đang ở trạng thái "Đang mượn" | `memberId`: MEM003 (`dam.tran@email.com`), `bookId`: BOOK003 |
| 3 | Từ SRS (Black-box) | Từ chối mượn khi tài khoản thành viên ở trạng thái "Hết hạn" | `memberId`: MEM005 (`binh.pham@email.com`), `bookId`: BOOK001 |
| 4 | Từ Code (White-box) | Kiểm tra rẽ nhánh điều kiện `member == null` (Không tìm thấy thành viên) | `memberId`: "MEM_NON_EXIST", `bookId`: BOOK001 |
| 5 | Từ Code (White-box) | Kiểm tra rẽ nhánh điều kiện `book == null` (Không tìm thấy sách) | `memberId`: MEM003, `bookId`: "BOOK_NON_EXIST" |
| 6 | Từ Code (White-box) | Kiểm tra điều kiện chặn trên biên giới hạn mượn: `currentBorrowCount >= 3` | `memberId`: MEM001 (Đã mượn sẵn 3 sách), `bookId`: BOOK001 |

4. **Câu hỏi thảo luận:**

   a. Các giá trị test từ SRS và từ Code có **khác nhau** không? Có trùng nhau không?
    Các giá trị test số 1, 2, 3 sinh ra từ SRS hoàn toàn trùng khớp với các rẽ nhánh logic nghiệp vụ trong code (các dòng lệnh `if` kiểm tra trạng thái). Tuy nhiên, các giá trị số 4 và 5 (kiểm tra thực thể `null`) chỉ xuất hiện khi nhìn vào cấu trúc code bên dưới nhằm bảo vệ hệ thống không crash, SRS nghiệp vụ thuần túy không mô tả chi tiết các trường hợp dữ liệu khuyết thiếu này.

   b. Tại sao hỏi *"Test này là Black-box hay White-box?"* lại là **câu hỏi sai**? Ta nên hỏi gì thay thế?
    Vì ranh giới này tạo ra một sự phân chia giả tạo. Cả SRS và mã nguồn thực tế đều là các **Mô hình (Models)** đại diện cho hệ thống. Thay vì hỏi cách tiếp cận thuộc chiếc hộp nào, ta nên hỏi: *"Test được thiết kế từ model nào và cấu trúc cấu thành rút ra từ mức trừu tượng (level of abstraction) nào?"* để xác định chính xác tiêu chí bao phủ.
   c. **Gợi ý:** SRS là một **model** ở mức trừu tượng cao, code Dart là **model** ở mức thấp — cả hai đều là model. Câu hỏi đúng: *"Test được thiết kế từ model nào?"*

---

## Bài tập 2: Phá án cùng mô hình RIPR (The RIPR Detective)

> ⏱ **Thời gian:** 15 phút | **Chương liên quan:** Ch.2 §2.1, Ch.14

### Kịch bản giả định

Nhóm bạn đang kiểm thử tính năng "Tìm kiếm sách" (TC-05: tìm kiếm không có kết quả). Bạn nhập từ khóa `"xyz_khong_ton_tai"` vào ô tìm kiếm. Kết quả:

- **Kết quả mong đợi**: Danh sách rỗng, không hiển thị sách nào
- **Kết quả thực tế**: Giao diện vẫn **hiển thị sách từ lần tìm trước** (lỗi UI!)
- **Kết quả test**: Bạn ghi **PASS** vì "không có thông báo lỗi"

→ Bug đã tồn tại và hiển thị trên giao diện, nhưng bạn không phát hiện!

### Nhiệm vụ nhóm

1. **Vẽ sơ đồ 4 bước RIPR:**

   ```
   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
   │ Reachability │ → │  Infection   │ → │ Propagation  │ → │ Revealability│
   │   Chạm tới   │   │ Nhiễm trạng  │   │ Lan truyền   │   │  Bộc lộ lỗi  │
   │              │   │  thái lỗi    │   │  ra output   │   │  cho tester  │
   └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
          ✅                 ✅                 ✅                 ❌ ← GÃY!
   ```

2. **Câu hỏi thảo luận:**

   a. Bug đã **Reach** → **Infect** → **Propagate** ra UI. Vậy **bước nào** bị gãy? Tại sao?
   Bước Revealability (Bộc lộ lỗi) bị gãy. Bởi vì mặc dù lỗi đã lan truyền ra ngoài giao diện (UI vẫn hiển thị danh sách sách cũ), nhưng Tester/Automated Test không có một cơ chế kiểm tra (Assert) đủ mạnh để phát hiện ra sự sai lệch giữa kết quả thực tế này và đặc tả yêu cầu.

   b. **Revealability** bị gãy vì **Test Oracle yếu**: "Kết quả mong đợi" quá chung chung. Hãy viết lại KQ mong đợi sao cho **rõ ràng, kiểm chứng được**:

   | | Trước (yếu) | Sau (mạnh) |
   |---|---|---|
   | KQ mong đợi | "Không có lỗi" | Giao diện phải hiển thị thông báo lỗi "Không tìm thấy sách" đồng thời toàn bộ danh sách card sách (flt-semantics[role="group"]) từ lần tìm kiếm trước phải bị xóa bỏ hoàn toàn khỏi màn hình. |

   c. Nếu bạn làm **automation** (bài A2), dòng `assert` trong code tương đương với điều gì trong manual testing? (Gợi ý: "Kết quả mong đợi" = Test Oracle)
   Dòng lệnh assert trong kiểm thử tự động chính là sự cụ thể hóa của Test Oracle (Kết quả mong đợi) trong kiểm thử thủ công. Nó đóng vai trò là trọng tài tối cao phán quyết tính đúng đắn của phần mềm tại thời điểm runtime.
---

## Bài tập 3: Ai bảo vệ phần mềm? (Test Suite vs SRS)

> ⏱ **Thời gian:** 15 phút | **Chương liên quan:** Ch.4 §4.2

### Bối cảnh

Theo góc nhìn Agile và TDD:

> *"In agile methods, test cases are the de facto specification for the system."*
> — Ammann & Offutt, Ch.4, p.99

### Nhiệm vụ nhóm

1. **Xem xét 12 Test Case** (TC-01 → TC-12) được mô tả trong SRS:

   | Nhóm chức năng | TCs | Chức năng |
   |---|---|---|
   | Đăng nhập | TC-01, TC-02, TC-03 | Đăng nhập thành công/thất bại |
   | Tìm kiếm & Lọc | TC-04 ~ TC-07 | Tìm theo tên/tác giả, lọc thể loại |
   | Mượn & Trả | TC-08, TC-09, TC-10 | Mượn sách, xem danh sách, trả sách |
   | Chức năng chung | TC-11, TC-12 | Đăng xuất, chuyển ngôn ngữ |

2. **Câu hỏi thảo luận:**

   a. Nếu file `SRS-library-system.md` **bị xóa mất**, liệu một lập trình viên mới có thể **chỉ nhìn** vào TC-08 ~ TC-10 để code lại tính năng mượn/trả sách không? Vì sao?
   Không thể hoàn toàn. Bởi vì kịch bản test case chỉ ghi lại hành vi đầu cuối (End-to-End) của một luồng dữ liệu cụ thể chứ không hiển thị toàn bộ các quy tắc ràng buộc biên ngầm định (ví dụ: logic tính toán ngày quá hạn chính xác, định dạng ràng buộc regex của email/số điện thoại, hay các trạng thái dữ liệu in-memory bị xóa sạch khi refresh tab).
   
   b. Liệt kê **những thông tin nghiệp vụ** mà TC-08 (Mượn sách) cho biết:

   | # | Thông tin (đọc được từ test) | Nguồn |
|---|---|---|
| 1 | Người dùng phải thực hiện Đăng nhập thành công trước khi có quyền nhấn nút mượn sách. | `login(page, test_config)` |
| 2 | Nút kích hoạt hành vi mượn sách ban đầu có nhãn văn bản hiển thị là `"Mượn sách này"`. | `has-text("Mượn sách này")` |
| 3 | Hệ thống yêu cầu một bước xác nhận trung gian thông qua việc nhấn nút `"Mượn"` trên cửa sổ Dialog. | `has-text("Mượn")` |

   c. **Giới hạn**: Góc nhìn "Test là tài liệu" yếu ở đâu?
      - Kịch bản người dùng thao tác sai (negative) mà chưa nghĩ tới?
      - Yêu cầu phi chức năng (hiệu suất, bảo mật)?
      - Nghiệp vụ thay đổi mà test chưa cập nhật?
    *Thiếu kịch bản tiêu cực nâng cao:* Test suite thường chỉ tập trung phủ các luồng chính, dễ bỏ sót các trường hợp thao tác sai dị biệt của người dùng nếu tester chưa quy hoạch hết.
     *Yêu cầu phi chức năng bị bỏ trống:* Bộ test code chức năng không thể mô tả các chỉ số về hiệu năng tải, bảo mật mã hóa dòng dữ liệu, hay độ tương thích thiết bị.
     *Độ trễ cập nhật tài liệu:* Khi quy trình nghiệp vụ thay đổi đột ngột nhưng kiểm thử viên chưa kịp sửa code test, tài liệu kiểm thử sẽ phản ánh sai lệch hoàn toàn trạng thái mong muốn của doanh nghiệp.
   d. **Kết luận nhóm:** SRS và Test Suite nên **cùng tồn tại** hay chỉ cần 1 trong 2? Giải thích.
    **Bắt buộc phải cùng song song tồn tại.** SRS giữ vai trò là "Nguồn sự thật gốc" (Source of Truth) định hình toàn bộ mục tiêu nghiệp vụ ở mức trừu tượng cao cho toàn bộ dự án. Trong khi đó, Test Suite đóng vai trò là "Người bảo vệ sống" (Living Guardian) giúp kiểm chứng cơ chế vận hành thực tế ở mức thấp một cách liên tục, đảm bảo code không bao giờ bị thoái lui (Regression).
---

## Bài tập 4: Vòng đời cuốn sách — Đồ thị trạng thái / The Book Lifecycle FSM

> ⏱ **Thời gian:** 20 phút | **Chương liên quan:** Ch.7 §7.5.2 (p.223–234)
>
> 🌐 **Song ngữ / Bilingual:** Thuật ngữ gốc tiếng Anh được giữ nguyên trong ngoặc.

### Bối cảnh / Context

Mỗi cuốn sách trong hệ thống trải qua các trạng thái khác nhau — đây chính là một **Finite State Machine (FSM)**:

> *"A Finite State Machine is a graph whose nodes represent states... and edges represent transitions among the states."*
> — Ammann & Offutt, Ch.7 §7.5.2, p.224

### Bước 1: Trạng thái (States) và Chuyển tiếp (Transitions)

| Ký hiệu | Trạng thái | State (EN) | Ví dụ trong seed data |
|----------|-----------|------------|----------------------|
| **S1** | Có sẵn | Available | BOOK001, BOOK002 |
| **S2** | Đang mượn | Borrowed | BOOK003 |
| **S3** | Quá hạn | Overdue | Khi quá 14 ngày chưa trả |
| **S4** | Thất lạc | Lost | BOOK007 |

| Ký hiệu | Sự kiện | Trigger (EN) | Từ → Đến |
|----------|---------|-------------|-----------|
| **T1** | Mượn sách | Borrow | S1 → S2 |
| **T2** | Trả sách (đúng hạn) | Return (on time) | S2 → S1 |
| **T3** | Kiểm tra quá hạn | Check overdue | S2 → S3 |
| **T4** | Trả sách (trễ hạn) | Return (late) | S3 → S1 |
| **T5** | Đánh dấu thất lạc | Mark as lost | S3 → S4 |

### Bước 2: Vẽ sơ đồ FSM trên giấy

```
                    T1: Mượn sách                T3: Quá hạn
              ┌─────────────────┐         ┌──────────────────┐
              │                 ▼         │                  ▼
         ┌─────────┐       ┌─────────┐       ┌─────────┐       ┌─────────┐
   ●───→ │   S1    │       │   S2    │       │   S3    │       │   S4    │
         │ Có sẵn  │ ◀──── │Đang mượn│       │ Quá hạn │ ────→ │Thất lạc │
         │Available│  T2:  │Borrowed │       │ Overdue │  T5:  │  Lost   │
         └─────────┘ Trả   └─────────┘       └────┬────┘ Lost  └─────────┘
              ▲              sách                  │
              │                                    │
              └────────────────────────────────────┘
                        T4: Trả sách trễ hạn
```

### Bước 3: Test Paths cho Edge Coverage

Suy ra test paths để **mỗi transition được thực hiện ít nhất 1 lần** (Transition Coverage = Edge Coverage, Ch.7 §7.2.1):

| Test Path | Chuỗi trạng thái | Transitions bao phủ |
|-----------|------------------|---------------------|
| **TP1** | $S1 \rightarrow S2 \rightarrow S1$ | $T1$ (Mượn sách), $T2$ (Trả sách đúng hạn) |
| **TP2** | $S1 \rightarrow S2 \rightarrow S3 \rightarrow S1$ | $T1$ (Mượn sách), $T3$ (Kiểm tra quá hạn), $T4$ (Trả sách trễ hạn) |
| **TP3** | $S1 \rightarrow S2 \rightarrow S3 \rightarrow S4$ | $T1$ (Mượn sách), $T3$ (Kiểm tra quá hạn), $T5$ (Đánh dấu thất lạc) |
### Bước 4: Ánh xạ với Test Case

| Test Path | TC tương ứng | Đã được cover? |
|-----------|-------------|---------------|
| **TP1** (mượn → trả) | `TC-08` (Mượn sách) kết hợp `TC-10` (Trả sách) | ✅ Đã bao phủ |
| **TP2** (quá hạn → trả) | `TC-14` (Thủ thư quét quá hạn) kết hợp kịch bản trả trễ | ✅ Đã bao phủ qua bộ test mở rộng |
| **TP3** (quá hạn → mất) | Kịch bản đánh dấu thất lạc từ phía Thủ thư | ❌ Chưa được bao phủ trong luồng cơ bản |

### Câu hỏi thảo luận

a. **Những transition nào** chưa có TC cover? Thiết kế TC mới cho chúng.
   Chuyển dịch T5 (Đánh dấu thất lạc từ trạng thái quá hạn) chưa có test case bắt buộc bao phủ. Thiết kế TC mới: Đăng nhập tài khoản Thủ thư `librarian@library.com`, truy cập danh sách phiếu mượn quá hạn, chọn phiếu của thực thể đang quá hạn và nhấn nút hành động "Đánh dấu thất lạc" ==> Assert trạng thái sách chuyển sang `Lost`.
b. Hệ thống có **BUG-07** (off-by-one ở kiểm tra quá hạn) — BUG này nằm ở transition nào? Vì sao Edge Coverage **bắt buộc** phải test transition đó?
    Bug này nằm trực tiếp tại chuyển dịch **T3 (Kiểm tra quá hạn)**. Vì Edge Coverage (Bao phủ cạnh) đòi hỏi mọi mũi tên chuyển trạng thái phải được kích hoạt tối thiểu một lần, nó ép buộc tester phải thiết kế giá trị kiểm thử rơi đúng vào biên ngày đáo hạn (`dueDate == ngày hiện tại`). Nhờ đó, trạng thái nhiễm lỗi (Infection) của thuật toán so sánh ngày sẽ bị kích hoạt và bộc lộ ra ngoài output.
c. Nếu thêm tính năng "Tìm lại sách" (S4 → S1), FSM thay đổi thế nào?
    Đồ thị sẽ xuất hiện thêm một cạnh định hướng mới (Edge) đi từ nút trạng thái S4 (Thất lạc) quay ngược trở lại nút trạng thái S1 (Có sẵn). Sự kiện kích hoạt (Trigger) của cạnh này sẽ là hàm nghiệp vụ `"Tìm lại được sách/Khôi phục sách từ kho lẻ"`.
---

## Bài tập 5: Oracle mạnh vs Oracle yếu / The Oracle Strength Challenge

> ⏱ **Thời gian:** 15 phút | **Chương liên quan:** Ch.14 §14.1 (p.410–413)

### Bối cảnh

> *"Some software organizations only check to see whether the software produces a runtime exception, or crashes. This has been called the null oracle strategy. [...] only between 25% to 56% of software failures result in a crash."*
> — Ammann & Offutt, Ch.14 §14.1, p.412

### Kịch bản: TC-06 — Lọc sách theo thể loại "Công nghệ"

So sánh 3 cấp độ Oracle:

```python
# === Oracle A: Null Oracle — chỉ kiểm tra "không crash" ===
page.locator('flt-semantics[role="group"]').first.wait_for()
# Không có assert → PASS nếu không exception

# === Oracle B: Weak Oracle — kiểm tra "có kết quả" ===
results = page.locator('flt-semantics[role="group"]')
assert results.count() > 0, "Không có kết quả"

# === Oracle C: Strong Oracle — kiểm tra NỘI DUNG kết quả ===
results = page.locator('flt-semantics[role="group"]')
assert results.count() > 0, "Không có kết quả"
for i in range(results.count()):
    label = results.nth(i).get_attribute("aria-label")
    assert "Công nghệ" in label, f"Sách '{label}' không thuộc thể loại Công nghệ"
```

### Nhiệm vụ nhóm

1. **Phân loại:** Oracle nào phát hiện được BUG-06 (bộ lọc case-sensitive)?

   | Oracle | Loại | Phát hiện BUG-06? | Giải thích |
|--------|------|-------------------|------------|
| **A** | `Null Oracle` | ❌ **Không** | Bộ lọc phân biệt hoa/thường sai nghiệp vụ chỉ hiển thị danh sách rỗng chứ không gây sập mã nguồn hay sinh ra exception runtime. |
| **B** | `Weak Oracle` | ❌ **Không** | Nếu bộ lọc bị lỗi trả về số lượng card sách $> 0$ nhưng chứa toàn bộ các sách thuộc thể loại khác (ví dụ Kinh tế), assert check số lượng vẫn vượt qua sai lầm. |
| **C** | `Strong Oracle`| ✅ **Có** | Vòng lặp duyệt sâu sẽ bóc tách chuỗi nhãn `aria-label` của từng card kết quả hiển thị thực tế để đối chiếu chính xác từ khóa `"Công nghệ"`. Nếu sai lệch sẽ kích hoạt Fail ngay lập tức. |
2. Theo textbook, Oracle C có cần kiểm tra **tất cả** sách không? Hay chỉ cần output **liên quan trực tiếp** đến mục đích test?
    Theo giáo trình (Chapter 14), Oracle C không cần và không nên kiểm tra toàn bộ database tổng thể một cách lan man. Nó chỉ cần tập trung kiểm tra nghiêm ngặt tính toàn vẹn của tập dữ liệu đầu ra (Output Filtered System Space) **liên quan trực tiếp** đến mục đích và phạm vi kiểm thử của Test Case đó để đảm bảo hiệu năng CI/CD.
3. Trong file `tests/test_search.py`, tìm assertion hiện tại cho TC-06. Nó thuộc cấp Oracle nào? Có thể cải thiện không?
    Assertion hiện tại của `TC-06` trong dự án đã được nhóm nâng cấp lên cấp độ **Strong Oracle**. Nó sử dụng vòng lặp để quét và bóc tách thuộc tính nhãn:
    python
    for i in range(books.count()):
        label = books.nth(i).get_attribute("aria-label")
        assert "Công nghệ" in label
    ```
    Điểm cải thiện thêm là kết hợp với hàm Smart Wait `wait_for_flutter(page, text="Mã: BOOK")` ngay phía trên để thay thế triệt để các lệnh chờ cứng, tránh hiện tượng bất đồng bộ khi Flutter chưa render xong thuộc tính.
---

## Bài tập 6: Ai cần chạy lại test? — Regression Test Selection

> ⏱ **Thời gian:** 15 phút | **Chương liên quan:** Ch.13 (p.406–409)

### Bối cảnh

> *"Regression testing constitutes the vast majority of testing effort... small changes to one part of a system often cause problems in distant parts of the system."*
> — Ammann & Offutt, Ch.13, p.406

### Kịch bản giả định

> **Thay đổi V1.1:** Số lượng sách mượn tối đa giảm từ **3 cuốn** xuống **2 cuốn**.

```dart
// V1.0 (cũ): static const int maxBooksPerMember = 3;
// V1.1 (mới): static const int maxBooksPerMember = 2;
```

### Nhiệm vụ nhóm

1. **Phân loại 12 Test Cases:**

   | TC | Mô tả | Sẽ FAIL? | Phải chạy lại? | Lý do |
|-----|-------|---------|---------------|-------|
| **TC-01** | Đăng nhập thành công | ❌ Không | ✅ Có | Thuộc bộ Regression Test nền tảng (Sanity check) để đảm bảo tính năng cốt lõi không bị sập sau khi cập nhật hệ thống. |
| **TC-02** | Đăng nhập sai mật khẩu | ❌ Không | ❌ Không | Logic xác thực mật khẩu độc lập hoàn toàn với tham số giới hạn sách. |
| **TC-03** | Đăng nhập bỏ trống | ❌ Không | ❌ Không | Logic kiểm tra form trống không bị ảnh hưởng. |
| **TC-04** | Tìm kiếm có kết quả | ❌ Không | ❌ Không | Module Tìm kiếm độc lập với nghiệp vụ giới hạn mượn sách. |
| **TC-05** | Tìm kiếm không kết quả | ❌ Không | ❌ Không | Không bị tác động bởi cấu hình mượn sách. |
| **TC-06** | Lọc theo thể loại | ❌ Không | ❌ Không | Không bị tác động bởi cấu hình mượn sách. |
| **TC-07** | Tìm theo tác giả | ❌ Không | ❌ Không | Không bị tác động bởi cấu hình mượn sách. |
| **TC-08** | Mượn sách thông thường | ❌ Không | ✅ Có | Bắt buộc re-run vì đây là hàm trực tiếp thực thi nghiệp vụ mượn sách, cần đảm bảo mượn cuốn thứ 1 và 2 vẫn hoạt động mượt mà. |
| **TC-09** | Xem sách đang mượn | ❌ Không | ❌ Không | Chỉ hiển thị dữ liệu thô từ danh sách phiếu mượn sẵn có. |
| **TC-10** | Trả sách | ❌ Không | ❌ Không | Logic hoàn trả sách về kho không bị tác động bởi giới hạn chặn trên. |
| **TC-11** | Đăng xuất | ❌ Không | ❌ Không | Không liên quan đến tham số nghiệp vụ mượn sách. |
| **TC-12** | Chuyển ngôn ngữ | ❌ Không | ❌ Không | Không liên quan đến tham số nghiệp vụ mượn sách. |

2. **Câu hỏi thảo luận:**

   a. TC nào **chắc chắn FAIL** do thay đổi?
    Trong 12 kịch bản cơ bản trên giao diện **không có kịch bản nào chắc chắn FAIL**, vì `TC-08` chỉ kiểm thử luồng mượn 1 cuốn sách thành công (vẫn thỏa mãn giới hạn $\le 2$). Tuy nhiên, nếu có kịch bản nâng cao test chặn biên mượn cuốn thứ 4 (giả định hệ thống cũ chặn từ cuốn 4) thì kịch bản đó sẽ FAIL vì lỗi logic hệ thống mới phải chặn ngay từ cuốn thứ 3.
   b. TC-08 (mượn bình thường) không FAIL — nhưng vì sao vẫn **phải chạy lại**?
    Vì thay đổi cấu hình diễn ra ngay trong thân hàm xử lý của tính năng mượn sách. Việc chạy lại `TC-08` là bắt buộc để thực hiện nhiệm vụ kiểm thử hồi quy (Regression Testing), chứng minh rằng việc sửa đổi cấu hình hệ thống không vô tình làm hỏng hoặc làm sập luồng mượn sách ở các trường hợp thông thường.
   c. Nếu 12 TC được **tự động hóa** (chạy ~2–3 phút) vs **thủ công** (chạy ~2–3 giờ), chiến lược nào hợp lý hơn: Retest-All hay Selective?
    Nếu dùng **Tự động hóa (Automation):** Chiến lược **Retest-All (Chạy lại tất cả)** là tối ưu nhất vì chi phí thời gian cực nhỏ (~2-3 phút), giúp giải phóng áp lực phân tích và đảm bảo an toàn tuyệt đối.
   
   Nếu dùng **Thủ công (Manual):** Chiến lược **Selective (Chạy lại có chọn lọc)** là bắt buộc để tối ưu hóa nguồn lực nhân sự, tránh lãng phí thời gian vào các module cô lập hoàn toàn như Đăng nhập/Ngôn ngữ.
---

## Bài tập 7: Tư duy đột biến — Kill the Mutant

> ⏱ **Thời gian:** 15 phút | **Chương liên quan:** Ch.9 §9.1.2 (p.322), §9.2.2 (p.336)

### Bối cảnh

**ROR (Relational Operator Replacement)** — thay thế toán tử quan hệ:

> *"Replace each occurrence of one of the relational operators (<, ≤, >, ≥, ==, ≠) by each of the other operators."*
> — Ammann & Offutt, Ch.9 §9.2.2, p.336

### Tình huống 1: BUG-02 — Giới hạn mượn sách

```dart
// Code đúng (theo SRS): >= 3 → từ chối
if (currentBorrowCount >= maxBooksPerMember)

// Code thực tế (mutant ROR: >= → >): > 3 → cho mượn cuốn thứ 4!
if (currentBorrowCount > maxBooksPerMember)
```

| Số sách đang mượn | Code đúng (`>=`) | Code lỗi (`>`) | Kill mutant? |
|-------------------|-----------------|----------------|-------------|
| 2 | Cho mượn | Cho mượn | Không — cùng KQ |
| 3 | **Từ chối** | **Cho mượn** | ✅ **Có (Kill!)** — Trạng thái Output khác nhau. |
| 4 | Từ chối | Từ chối | Không — cùng KQ |

### Tình huống 2: BUG-07 — Kiểm tra quá hạn

```dart
// Code đúng: hôm nay >= ngày hẹn → quá hạn
if (!now.isBefore(record.dueDate))

// Code thực tế (mutant): hôm nay > ngày hẹn
if (now.isAfter(record.dueDate))
```

Sách mượn 1/9, hạn trả 15/9. Ngày nào giết mutant?

| Ngày kiểm tra | Code đúng | Code lỗi | Kill? |
|--------------|----------|---------|-------|
| 14/9 | Chưa quá hạn | Chưa quá hạn | Không — cùng KQ |
| **15/9** | **Quá hạn** | **Chưa quá hạn** | ✅ **Có (Kill!)** — Trạng thái Output khác nhau tại biên. |
| 16/9 | Quá hạn | Quá hạn | Không — cùng KQ |

### Câu hỏi tổng kết

a. Giá trị test giết mutant luôn nằm ở đâu? (Gợi ý: **giá trị biên** — BVA, Ch.6)
   Giá trị kiểm thử dùng để diệt các đột biến toán tử quan hệ (ROR Mutants) luôn nằm chính xác tại **Giá trị biên nghiệp vụ (Boundary Values)**.
b. Tại sao *"thiết kế test data tốt bằng BVA tự động giết được hầu hết ROR mutants"*?
   Vì phương pháp phân tích giá trị biên (BVA) ép tester chọn các điểm dữ liệu nằm ngay trên đường ranh giới thay đổi quyết định của biểu thức logic. Các đột biến toán tử quan hệ (như chuyển `>=` thành `>`) chỉ làm dịch chuyển điểm ranh giới đi đúng 1 đơn vị, do đó dữ liệu biên sẽ ngay lập tức bắt được sự sai lệch hành vi này.
c. **Liên hệ RIPR:** Giá trị biên đảm bảo **Infection** (trạng thái khác nhau giữa code đúng và code lỗi). Nếu dùng giá trị xa biên (ví dụ: 0), tại sao mutant **sống sót**?
    Khi sử dụng giá trị kiểm thử xa biên (ví dụ: số sách đang mượn là 0 hoặc 1), cả biểu thức code đúng (`currentBorrowCount >= 3`) và biểu thức đột biến lỗi (`currentBorrowCount > 3`) đều cho ra cùng một kết quả logic là `False` (Hệ thống đều cho mượn). Do đó, trạng thái bộ nhớ không hề xuất hiện sự sai lệch dữ liệu => **Bước Infection (Nhiễm trạng thái lỗi) không xảy ra**, lỗi không thể lan truyền và bộc lộ, dẫn đến mutant sống sót.
---

## Bài tập 8: Chiếc bẫy Logic (The Logic Trap)

> ⏱ **Thời gian:** 20 phút | **Chương liên quan:** Ch.8 §8.1.1 (p.248), §8.1.2 (p.250–253)

### Bối cảnh lý thuyết

Textbook nhấn mạnh: chỉ test toàn bộ biểu thức đúng/sai (**Predicate Coverage**) là chưa đủ — vì các **mệnh đề con (clauses)** bên trong có thể ẩn chứa bug mà không bao giờ bị phát hiện:

> *"An obvious failing of this criterion is that the individual clauses are not always exercised."*
> — Ammann & Offutt, Ch.8 §8.1.1, p.248

Khái niệm **determination** (quyết định) cho phép phát hiện bug ở từng clause:

> *"The key notion is that of determination, the conditions under which a clause influences the outcome of a predicate. [...] if you flip the clause, and the predicate changes value, then the clause determines the predicate."*
> — Ammann & Offutt, Ch.8 §8.1.2, p.250

Đây là cơ sở của **Active Clause Coverage (ACC)** — còn được biết là **MC/DC (Modified Condition/Decision Coverage)**, tiêu chuẩn bắt buộc trong phần mềm hàng không (FAA DO-178C):

> *"Active Clause Coverage (ACC): For each p ∈ P and each major clause ci ∈ Cp, choose minor clauses cj, j ≠ i so that ci determines p. TR has two requirements for each ci: ci evaluates to true and ci evaluates to false."*
> — Ammann & Offutt, Ch.8, Definition 8.42, p.251

### Kịch bản: REQ-04 — Mượn sách

Điều kiện để **cho phép mượn sách thành công** là biểu thức logic gồm 3 mệnh đề (clauses):

$$P = A \wedge B \wedge C$$

| Clause | Ý nghĩa | Ví dụ True | Ví dụ False |
|--------|---------|-----------|------------|
| **A** | Sách có sẵn (`book.status == available`) | BOOK001 | BOOK003 (đang mượn) |
| **B** | Chưa đạt giới hạn mượn (`borrowCount < max`) | MEM002 (0 sách) | MEM001 (đã mượn 3 sách) |
| **C** | Thành viên hoạt động (`member.status == active`) | MEM001 | MEM004 (suspended) |

### Nhiệm vụ nhóm

1. **Bước 1 — Predicate Coverage (PC):** Chỉ cần 2 test cases:

   | TC | A | B | C | $P = A \wedge B \wedge C$ | Kết quả |
   |-----|---|---|---|---|---|
   | TC-α | T | T | T | **True** | Cho mượn ✅ |
   | TC-β | F | F | F | **False** | Từ chối ❌ |

   **Câu hỏi:** Với chỉ 2 TCs này, hệ thống có bug gì mà bạn **không phát hiện được**?
   Bạn sẽ bỏ sót hoàn toàn các bug ẩn náu sâu trong các mệnh đề con độc lập khi chúng bị gán đè logic. Ví dụ: Nếu lập trình viên viết sai code cố định giá trị mệnh đề $C$ luôn bằng `True` (bỏ qua việc check trạng thái thành viên bị tạm ngưng/hết hạn), thì hai kịch bản $TC-\alpha$ và $TC-\beta$ vẫn chạy PASS bình thường $\rightarrow$ Bug lọt lưới do độ bao phủ quá thô.

2. **Bước 2 — Active Clause Coverage (ACC):** Để test từng clause, phải **cô lập** nó — giữ các clause còn lại ở giá trị cho phép clause đang test **quyết định** (determine) kết quả.

   **Nhóm hãy điền bảng truth table sau:**

   | TC | A | B | C | $P$ | Major clause được test | Giải thích |
|----|---|---|---|-----|----------------------|-----------|
| 1 | **T** | T | T | True | A (True → P True) | Cặp với TC2 |
| 2 | **F** | T | T | **False** | A (False → P **False**) | Lật A, B và C giữ nguyên T: P thay đổi. |
| 3 | T | **T** | T | True | B (True → P True) | Cặp với TC4 |
| 4 | T | **F** | T | **False** | B (False → P **False**) | Lật B, A và C giữ nguyên T: P thay đổi. |
| 5 | T | T | **T** | True | C (True → P True) | Cặp với TC6 |
| 6 | T | T | **F** | **False** | C (False → P **False**) | Lật C, A và B giữ nguyên T: P thay đổi. |

   > **Lưu ý:** Nhiều TCs có thể trùng nhau. Sau khi loại bỏ trùng lặp, ACC cần tối thiểu bao nhiêu test cases cho `A AND B AND C`?
    Sau khi loại bỏ các dòng trùng lặp hoàn toàn về cấu hình (`TC 1`, `TC 3`, `TC 5` giống nhau), độ bao phủ ACC cho biểu thức logic thức `A AND B AND C` cần tối thiểu **4 test cases** độc lập để hoàn thành.

3. **Bước 3 — Phát hiện bug BUG-04:**

   Bug thực tế trong hệ thống: BUG-04 — thành viên "Tạm ngưng" nhận thông báo lỗi sai ("Thành viên đã hết hạn" thay vì "đang bị tạm ngưng"). TC nào trong bảng ACC ở trên sẽ **phát hiện** BUG-04? TC-α và TC-β của Predicate Coverage có phát hiện được không?

    Kịch bản **`TC 6`** trong bảng truth table của ACC (Cấu hình: $A=True$, $B=True$, $C=False$ - tương ứng trường hợp sách sẵn sàng, chưa quá giới hạn nhưng tài khoản bị tạm ngưng) sẽ **phát hiện ra BUG-04**. 
    Hai kịch bản TC-alpha và TC-beta của Predicate Coverage **hoàn toàn không thể phát hiện** ra bug này vì TC-alpha chỉ test luồng đúng hoàn toàn, còn TC-beta do lật đồng thời cả 3 biến sang `False` nên hệ thống sẽ rẽ nhánh và trả về thông báo lỗi của biến A hoặc B trước khi chạm tới phân đoạn kiểm tra lỗi của biến $C$.
### Câu hỏi thảo luận

a. Với `A AND B AND C`, Predicate Coverage cần 2 TCs, ACC cần bao nhiêu? Tại sao con số tăng lên là **xứng đáng**?
    Predicate Coverage cần 2 TCs, ACC cần tối thiểu 4 TCs. Sự gia tăng này hoàn toàn xứng đáng vì nó giúp cô lập và kiểm chứng độc lập sức mạnh quyết định của từng điều kiện nghiệp vụ riêng lẻ, đảm bảo không có bất kỳ dòng logic lỗi nào bị che khuất bởi các mệnh đề đứng trước.
b. Trong thực tế, FAA yêu cầu **MC/DC** (tương đương ACC) cho phần mềm điều khiển máy bay. Tại sao chỉ dùng Predicate Coverage cho phần mềm hàng không là **nguy hiểm**?
    Vì phần mềm hàng không đòi hỏi tính an toàn tuyệt đối cực hạn. Nếu chỉ dùng Predicate Coverage, các lỗi kết hợp logic ẩn (ví dụ: cảm biến góc nghiêng hỏng nhưng bị che lấp bởi điều kiện vận tốc) sẽ không bao giờ bị kích hoạt trong quá trình test. Khi ra điều kiện thực tế, chỉ cần các mệnh đề con đồng thời rơi vào điểm mù logic, hệ thống sẽ đưa ra quyết định sai lầm gây thảm họa phi cơ.
c. **Kết nối BT7 (Mutation):** Nếu lập trình viên viết `OR` thay vì `AND` — đây có phải là một loại **ROR mutant** không? Giá trị test nào giết mutant này?
   Đây không phải là ROR mutant mà thuộc loại **BOM Mutant (Boolean Operator Mutants)** - Thay thế toán tử logic. Để diệt mutant này, ta dùng các giá trị test có cấu hình làm cho hai biểu thức cho ra kết quả nghịch đảo nhau. Cụ thể là các cấu hình có 1 mệnh đề `False` và các mệnh đề còn lại `True` (ví dụ: `[F, T, T]`, `[T, F, T]`, `[T, T, F]`). Lúc này code đúng `AND` sẽ trả về `False`, còn code lỗi đột biến `OR` sẽ trả về `True` $\rightarrow$ Mutant bị tiêu diệt.
---

## Bài tập 9: Kẻ phá hoại bất ổn — Flaky Tests

> ⏱ **Thời gian:** 10 phút (Exit Ticket) | **Chương liên quan:** Ch.4 §4.2 (p.98–100)

### Bối cảnh lý thuyết

Theo textbook, test harness đóng vai trò "người bảo vệ" — nhưng chỉ khi nó **đáng tin cậy**:

> *"Test automation is a prerequisite for test-driven development. [...] the correctness of the system at any single point in time is subject to immediate verification simply by running the test set."*
> — Ammann & Offutt, Ch.4 §4.2, p.98

> *"Not only do our tests need to be good—they also need to be fast!"*
> — Ammann & Offutt, Ch.4 §4.2.1, p.100

Nhưng nếu test lúc **PASS**, lúc **FAIL** (không thay đổi code) — đó là **Flaky Test**. Flaky test **phá hủy** vai trò Guardian vì lập trình viên sẽ mất niềm tin: *"Lại fail nữa rồi, chắc lại do flaky thôi"* → bỏ qua cả lỗi thật.

### Kịch bản: Flutter Web CanvasKit

Hệ thống thư viện sử dụng Flutter Web với renderer **CanvasKit** (vẽ UI trên `<canvas>`). Không giống HTML DOM thông thường, Flutter cập nhật **Semantics Tree** với độ trễ không cố định.

File `conftest.py` hiện có hàm **Smart Wait**:

```python
def wait_for_flutter(page, text=None, selector=None, timeout=10000):
    """Smart Wait: chờ Flutter Semantics Tree cập nhật."""
    if text:
        page.locator(
            f'flt-semantics:has-text("{text}"), flt-semantics[aria-label*="{text}"]'
        ).first.wait_for(state="attached", timeout=timeout)
    elif selector:
        page.locator(selector).first.wait_for(state="attached", timeout=timeout)
    else:
        page.locator("flt-semantics").first.wait_for(state="attached", timeout=timeout)
```

### Nhiệm vụ nhóm (Exit Ticket)

1. **Thí nghiệm tưởng tượng:** Nếu bạn thay `wait_for_flutter(page, text="Đăng xuất")` bằng `time.sleep(0.1)` và chạy `pytest -v` 10 lần liên tiếp, điều gì sẽ xảy ra?

   | Lần chạy | `wait_for_flutter` (Smart Wait) | `time.sleep(0.1)` (Hard Sleep) |
|----------|-------------------------------|-------------------------------|
| 1 | ✅ PASS | ❌ **FAIL** (Nếu CPU bận, Flutter chưa kịp nạp Semantics) |
| 2 | ✅ PASS | ✅ **PASS** (Nếu CPU rảnh, luồng xử lý xong trong 0.05s) |
| 3 | ✅ PASS | ❌ **FAIL** (Độ trễ render canvas kéo dài qua 0.12s) |
| ... | ✅ PASS | ✅ **PASS** |
| 10 | ✅ PASS | ❌ **FAIL** |

2. **Giải thích kỹ thuật:** Vì sao `wait_for_flutter` **ổn định** (deterministic) còn `time.sleep(0.1)` **bất ổn** (non-deterministic)?
      `wait_for_flutter` là cơ chế **Đồng bộ dựa trên sự kiện (Deterministic Polling)**. Nó chủ động bắt cứng trạng thái của Semantics Tree, chỉ đi tiếp khi phần tử đích thực sự gắn kết thành công vào cây DOM ẩn.
      `time.sleep(0.1)` là cơ chế **Đồng bộ dựa trên thời gian tuyến tính (Non-deterministic Hard Sleep)**. Nó hoàn toàn mù quáng trước trạng thái hệ thống, giả định vô căn cứ rằng mọi tác vụ render luôn kết thúc dưới 100ms. Trong thực tế môi trường CI/CD, tài nguyên phần cứng bị chia sẻ khiến thời gian phản hồi biến thiên liên tục, tạo ra sự flaky.
3. **Kết nối với Ch.4:** Tác giả nói test phải *"be good AND fast"*. Nếu bạn dùng `time.sleep(5)` (chờ dài) để tránh flaky, bạn hy sinh yếu tố nào? Nếu hệ thống CI chạy 12 TCs × 5 giây sleep mỗi bước × 10 bước = bao nhiêu phút? Có còn **"immediate verification"** không?
    Nếu dùng giải pháp tăng thời gian chờ cứng lên `time.sleep(5)`, chúng ta đang **trực tiếp hy sinh yếu tố Tốc độ (CI Speed)** của bộ test harness.
* **Bài toán tính toán thời gian chạy trên CI:**
    Thời gian lãng phí = 12TCs * 5giây/bước * 10 bước = 600 giây = 10 phút
    Bộ test lúc này mất tới hơn 10 phút chỉ để chạy 12 kịch bản đơn giản. Hệ thống hoàn toàn **đánh mất tính năng "Xác thực tức thời" (Immediate verification)** - triết lý cốt lõi của kiểm thử Agile/TDD, biến CI/CD thành một nút thắt cổ chai làm chậm tiến độ bàn giao của toàn dự án.

4. **Câu hỏi trắc nghiệm (chọn 1):** Hàm `wait_for_flutter` thuộc thành phần nào trong kiến trúc test?
   - (a) Test Oracle
   - (b) Test Driver
   - (c) Test Harness infrastructure   ==> đúng
   - (d) Test Data

---

## Phụ lục: Ánh xạ bài tập ↔ textbook

| Bài tập | Khái niệm chính | Chương |
|---|---|---|
| BT1: Box Debate | MDTD, Level of Abstraction | Ch.2 §2.4–2.5, Ch.6 |
| BT2: RIPR Detective | RIPR Model, Test Oracle, Revealability | Ch.2 §2.1, Ch.14 |
| BT3: Test as Guardian | Test Harness, De facto Specification | Ch.4 §4.2 |
| **BT4: Book Lifecycle FSM** | **FSM, State/Transition Coverage, Test Path** | **Ch.7 §7.5.2, §7.2.1** |
| **BT5: Oracle Strength** | **Null Oracle, Oracle Precision, Revealability** | **Ch.14 §14.1** |
| **BT6: Regression Selection** | **Regression Testing, Test Selection, CI** | **Ch.13, Ch.4 §4.2** |
| **BT7: Kill the Mutant** | **Mutation Testing, ROR, BVA ↔ Mutation** | **Ch.9 §9.1.2, §9.2.2, Ch.6** |
| **BT8: The Logic Trap** | **Predicate/Clause/Active Clause Coverage, MC/DC** | **Ch.8 §8.1.1, §8.1.2** |
| **BT9: Flaky Tests** | **Test Harness, Deterministic Testing, CI Speed** | **Ch.4 §4.2, §4.2.1** |
