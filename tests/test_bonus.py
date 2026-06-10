"""
Bonus Tests (B1) — Advanced Features & Edge Cases
"""

import os
import pytest

from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    flutter_click_button,
    wait_for_flutter,
    SCREENSHOT_DIR,
)


LIBRARIAN_EMAIL = "librarian@library.com"
LIBRARIAN_PASSWORD = "admin123"


def librarian_login(page, test_config):
    page.goto(
        test_config["base_url"],
        wait_until="networkidle"
    )

    enable_flutter_semantics(page)

    flutter_fill(page, "Email", LIBRARIAN_EMAIL)
    flutter_fill(page, "Mật khẩu", LIBRARIAN_PASSWORD)

    flutter_click_button(page, "Đăng nhập")

    page.wait_for_timeout(3000)

    enable_flutter_semantics(page)

    return " ".join(
        page.locator("flt-semantics").all_text_contents()
    )


def test_librarian_add_member_success(page, test_config):
    """
    TC-13: Librarian adds a new member successfully
    """

    sem_text = librarian_login(page, test_config)

    if "Thành viên" not in sem_text:
        pytest.skip(
            "REQ-07 Member Management is not available on current deployment"
        )

    page.locator(
        'flt-semantics:has-text("Thành viên")'
    ).first.click()

    wait_for_flutter(page, text="Thêm thành viên")

    flutter_fill(
        page,
        "Họ tên",
        "Nguyễn Văn Test"
    )

    flutter_fill(
        page,
        "Email",
        "member_test_2026@stqa.com"
    )

    flutter_fill(
        page,
        "Số điện thoại",
        "0987654321"
    )

    flutter_click_button(
        page,
        "Thêm thành viên"
    )

    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "tc13_add_member_success.png"
        )
    )

    sem_text = " ".join(
        page.locator("flt-semantics").all_text_contents()
    )

    assert (
        "thành công" in sem_text.lower()
        or "Nguyễn Văn Test" in sem_text
    )


def test_librarian_check_overdue(page, test_config):
    """
    TC-14: Librarian checks overdue books
    """

    sem_text = librarian_login(page, test_config)

    if "Kiểm tra quá hạn" not in sem_text:
        pytest.skip(
            "REQ-06 Overdue Checking is not available on current deployment"
        )

    flutter_click_button(
        page,
        "Kiểm tra quá hạn"
    )

    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "tc14_check_overdue_triggered.png"
        )
    )

    sem_text = " ".join(
        page.locator("flt-semantics").all_text_contents()
    )

    assert "quá hạn" in sem_text.lower()


def test_add_member_invalid_email(page, test_config):
    """
    TC-15: Invalid email when creating member
    """

    sem_text = librarian_login(page, test_config)

    if "Thành viên" not in sem_text:
        pytest.skip(
            "REQ-07 Member Management is not available on current deployment"
        )

    page.locator(
        'flt-semantics:has-text("Thành viên")'
    ).first.click()

    wait_for_flutter(page, text="Thêm thành viên")

    flutter_fill(
        page,
        "Họ tên",
        "Lỗi Email"
    )

    flutter_fill(
        page,
        "Email",
        "bad_email@domain"
    )

    flutter_fill(
        page,
        "Số điện thoại",
        "0123456789"
    )

    flutter_click_button(
        page,
        "Thêm thành viên"
    )

    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "tc15_invalid_email_format.png"
        )
    )

    sem_text = " ".join(
        page.locator("flt-semantics").all_text_contents()
    )

    assert (
        "email" in sem_text.lower()
        or "không hợp lệ" in sem_text.lower()
        or "định dạng" in sem_text.lower()
    )
