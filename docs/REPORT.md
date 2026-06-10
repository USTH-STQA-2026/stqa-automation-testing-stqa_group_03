# BÁO CÁO KẾT QUẢ DỰ ÁN KIỂM THỬ TỰ ĐỘNG WEB UI
**Hệ thống:** Quản lý mượn sách Thư viện ABC (https://stqa.rbc.vn)  
**Môn học:** Kiểm thử và Đảm bảo chất lượng phần mềm (STQA)  
**Nhóm thực hiện:** Nhóm 3 (Lớp: 252ICT2012.L1)  

---

## 👥 1. Danh sách thành viên & Bảng phân chia nhiệm vụ (Matrix)

Hệ thống ghi nhận sự đóng góp công bằng của cả 5 thành viên thông qua phân rã công việc (WBS) và kiểm duyệt chéo:

| STT | Họ và tên | Vai trò | Nhiệm vụ Code Automation | Nhiệm vụ Lý thuyết & Phụ trách | Tỷ lệ đóng góp |
|---|---|---|---|---|---|
| 1 | Trần Duy Hoàng Anh | **Trưởng nhóm (Team Leader)** | Hoàn thành toàn bộ `tests/test_borrow_return.py` (`TC-08`, `TC-09`, `TC-10`) | Git Setup (Fork repo, cấu hình `.env` mẫu), Làm **BT4** (Vẽ sơ đồ máy trạng thái FSM Book Lifecycle) | 20% |
| 2 | Nguyễn Lê Hải Anh | **Phó nhóm (QA Lead)** | Hoàn thành toàn bộ `tests/test_general.py` (`TC-11`, `TC-12`) | Gatekeeper (Review Pull Request, quét bẫy `time.sleep()`, check Weak Oracle), Làm **BT5** & **BT9**, Tổng hợp file `REPORT.md` | 20% |
| 3 | Tạ Hoàng Duy | **Thành viên 3** | Hoàn thành `tests/test_login.py` (`TC-02`, `TC-03`) | Nghiên cứu dữ liệu từ `test-accounts.md`, áp dụng kĩ thuật Data-driven với `@pytest.mark.parametrize` cho các trường biên rỗng | 20% |
| 4 | Hoàng Gia Khánh | **Thành viên 4** | Hoàn thành một phần `tests/test_search.py` (`TC-04`, `TC-05`) | Nghiên cứu tài liệu đặc tả hệ thống phục vụ kiểm thử Module Tìm kiếm (Phần 1) | 20% |
| 5 | Nguyễn Trung Hiếu | **Thành viên 5** | Hoàn thành một phần `tests/test_search.py` (`TC-06`, `TC-07`) | Đóng góp câu trả lời lý thuyết **BT1** (Box Debate) và **BT2** (RIPR Detective) | 20% |

---

## 📊 2. Kết quả thực thi kiểm thử (Test Execution Report)

Bộ kiểm thử tự động bao gồm **15 kịch bản** (12 kịch bản bắt buộc theo đặc tả kịch bản kiểm thử trong `ASSIGNMENT.md` và 3 kịch bản nâng cao viết thêm phục vụ Bonus điểm B1).

### 2.1. Thống kê tổng quan
* **Tổng số kịch bản thiết kế:** 15
* **Số kịch bản VƯỢT QUA (PASSED):** 15
* **Số kịch bản THẤT BẠI (FAILED):** 0
* **Tỷ lệ thành công (Success Rate):** 100%

### 2.2. Chi tiết kết quả từng kịch bản
Nhóm đã cấu hình lưu vết toàn bộ ảnh chụp minh chứng tại thư mục `screenshots/` sau khi kết thúc mỗi luồng chạy.

| Mã TC | Tên kịch bản kiểm thử | Trạng thái | Minh chứng (Artifacts) | Ghi chú kỹ thuật |
|---|---|---|---|---|
| **TC-01** | Đăng nhập thành công với tài khoản hợp lệ | ✅ PASSED | `login_success.png` | Sử dụng tài khoản mặc định hệ thống |
| **TC-02** | Đăng nhập thất bại – sai mật khẩu | ✅ PASSED | `login_fail_wrong_password.png` | Xác thực thông báo lỗi "Mật khẩu không đúng" |
| **TC-03** | Đăng nhập thất bại – để trống các trường dữ liệu | ✅ PASSED | `login_fail_empty_fields_*.png` | Áp dụng `@pytest.mark.parametrize` quét 3 phân vùng biên |
| **TC-04** | Tìm kiếm sách theo tên — có kết quả trả về | ✅ PASSED | `tc04_search_by_name.png` | Sử dụng từ khóa "Flutter", kiểm tra text Semantics |
| **TC-05** | Tìm kiếm sách theo tên — không có kết quả | ✅ PASSED | `tc05_search_no_result.png` | Đối chiếu thông báo "Không tìm thấy sách" theo REQ-03 |
| **TC-06** | Lọc sách theo Thể loại (Category) | ✅ PASSED | `tc06_filter_by_category.png` | Duyệt vòng lặp kiểm tra thuộc tính `aria-label` của các card |
| **TC-07** | Tìm kiếm sách theo tên Tác giả | ✅ PASSED | `tc07_search_by_author.png` | Xác thực từ khóa tác giả "Nguyễn Minh Đức" |
| **TC-08** | Mượn sách thành công | ✅ PASSED | `tc08_borrow_success.png` | Sử dụng tài khoản `dam.tran@email.com` (chưa mượn sách) |
| **TC-09** | Kiểm tra danh sách sách đã mượn hiển thị | ✅ PASSED | `TC09_view_borrowed_books.png` | Xác thực chuyển tab điều hướng "Mượn / Trả" |
| **TC-10** | Trả sách đang mượn thành công | ✅ PASSED | `tc10_return_success.png` | Chu trình chuyển đổi trạng thái thực thể hoàn tất |
| **TC-11** | Đăng xuất (Logout) thành công | ✅ PASSED | `tc11_logout_success.png` | Xác thực trạng thái quay về màn hình Login ban đầu |
| **TC-12** | Chuyển đổi ngôn ngữ giao diện sang Tiếng Anh | ✅ PASSED | `tc12_switch_language_en.png` | Đọc cấu trúc cây Semantics để quét text "Logout" / "Borrow" |
| **TC-13** | Thủ thư thêm thành viên mới thành công | ✅ PASSED | `tc13_add_member_success.png` | **[Bonus B1]** Đăng nhập tài khoản Thủ thư (REQ-07) |
| **TC-14** | Thủ thư kích hoạt tiến trình quét kiểm tra quá hạn | ✅ PASSED | `tc14_check_overdue_triggered.png` | **[Bonus B1]** Thực thi nghiệp vụ đặc biệt của Thủ thư (REQ-06) |
| **TC-15** | Thêm thành viên thất bại do định dạng Email sai | ✅ PASSED | `tc15_invalid_email_format.png` | **[Bonus B1]** Phân tích giá trị biên lỗi cú pháp (REQ-07) |

---

## 🛠 3. Giải pháp kỹ thuật & Tối ưu hóa hạ tầng (Test Harness Infrastructure)

Đối diện với đặc thù của ứng dụng **Flutter Web (CanvasKit renderer)**, nhóm đã áp dụng triệt để các kỹ thuật hạ tầng tiên tiến nhằm đạt điểm tuyệt đối tiêu chí tối ưu hóa:

1. **Loại bỏ hoàn toàn Anti-pattern `time.sleep()`:** Dựa trên kết quả nghiên cứu **BT9**, nhóm nhận thức rõ `time.sleep()` tạo ra trạng thái dừng không xác định (non-deterministic), làm chậm hạ tầng CI/CD một cách vô ích. Nhóm đã sử dụng hàm **Smart Wait** (`wait_for_flutter()`) hoạt động theo cơ chế polling tuần hoàn để đồng bộ hóa chính xác thời điểm cây Semantics Tree hoàn thành re-render.
2. **Xây dựng Chiến lược Strong Oracle:** Để tăng khả năng bộc lộ lỗi (Revealability) của mô hình RIPR, toàn bộ các điểm kiểm tra (`assert`) không chỉ dừng lại ở việc kiểm tra URL hay kiểm tra trạng thái không crash (Null/Weak Oracle). Nhóm đã triển khai trích xuất toàn bộ chuỗi text được phơi bày trên `flt-semantics` thông qua:
   ```python
   sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
   assert "Thông báo mong đợi từ SRS" in sem_text


## 🛠 4. Khai báo sử dụng AI (AI Usage Declaration)
Nhóm đã sử dụng mô hình ngôn ngữ lớn **Gemini**
Phạm vi sử dụng: AI được dùng như một trợ lý (thợ gõ) để tăng tốc độ soạn thảo mã nguồn, gợi ý cú pháp hàm kiểm thử của thư viện Playwright Python, và hỗ trợ cấu hình định dạng HTML cho tài liệu báo cáo.
Vai trò con người (Kiểm soát viên): Toàn bộ các Assertions (Oracle) sinh ra bởi AI đều được các thành viên trong nhóm đối chiếu và chuẩn hóa thủ công theo tài liệu đặc tả yêu cầu phần mềm (SRS-library-system.md). Nhóm đã tự tay loại bỏ hoàn toàn các selector sai bản chất CanvasKit và các hàm wait_for_timeout() do AI đề xuất để bảo vệ tính deterministic của bộ test.

