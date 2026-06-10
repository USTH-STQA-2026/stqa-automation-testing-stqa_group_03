"""
Login Tests (*Kiểm thử Đăng nhập*) — Library Book Borrowing System (*Hệ thống Mượn sách thư viện*)

📖 Textbook concepts in this file:
   - RIPR Model (Ch.2): See [R], [I], [P], [R✓] comments in TC-01
   - Data-Driven Testing / @parametrize (Ch.3 §3.3.2): See hint in TC-02/TC-03

This file contains 1 completed example (TC-01).
Students must complete TC-02 and TC-03.

(*File này chứa 1 ví dụ mẫu (TC-01) đã hoàn chỉnh.
Sinh viên cần hoàn thành TC-02 và TC-03.*)
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


def test_login_success(page, test_config):
    """TC-01: Login success with valid credentials"""

    # Arrange: Navigate to the login page
    page.goto(
        test_config["base_url"],
        wait_until="networkidle",
        timeout=60000
    )

    # Enable Flutter semantics for element interaction
    enable_flutter_semantics(page)

    # Act: Enter valid login credentials
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", test_config["password"])

    # Submit the login form
    flutter_click_button(page, "Đăng nhập")

    # Wait for successful login state
    wait_for_flutter(page, text="Đăng xuất")

    # Capture screenshot as test evidence
    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "login_success.png"
        )
    )

    # Assert: Verify successful login
    sem_text = " ".join(
        page.locator("flt-semantics").all_text_contents()
    )

    has_user_name = (
        test_config["display_name"] in sem_text
    )

    has_logout = (
        "Đăng xuất" in sem_text
        or "Logout" in sem_text
    )

    assert has_user_name or has_logout


def test_login_fail_wrong_password(page, test_config):
    """TC-02: Login fail – wrong password"""

    # Arrange: Navigate to the login page
    page.goto(
        test_config["base_url"],
        wait_until="networkidle",
        timeout=60000
    )

    # Enable Flutter semantics for element interaction
    enable_flutter_semantics(page)

    # Act: Enter a valid email and an invalid password
    flutter_fill(page, "Email", test_config["email"])
    flutter_fill(page, "Mật khẩu", "wrongpassword")

    # Submit the login form
    flutter_click_button(page, "Đăng nhập")

    # Wait for the error message to appear
    wait_for_flutter(
        page,
        text="Mật khẩu không đúng"
    )

    # Capture screenshot as test evidence
    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "login_fail_wrong_password.png"
        )
    )

    # Assert: Verify that the expected error message is displayed
    sem_text = " ".join(
        page.locator("flt-semantics").all_text_contents()
    )

    assert "Mật khẩu không đúng" in sem_text


@pytest.mark.parametrize(
    "email, password",
    [
        ("", ""),
    ]
)
def test_login_fail_empty_fields(
    page,
    test_config,
    email,
    password
):
    """TC-03: Login fail – empty fields"""

    # Arrange: Navigate to the login page
    page.goto(
        test_config["base_url"],
        wait_until="networkidle",
        timeout=60000
    )

    # Enable Flutter semantics for element interaction
    enable_flutter_semantics(page)

    # Act: Leave email and password fields empty
    flutter_fill(page, "Email", email)
    flutter_fill(page, "Mật khẩu", password)

    # Submit the login form
    flutter_click_button(page, "Đăng nhập")

    # Wait for the validation message to appear
    wait_for_flutter(
        page,
        text="Vui lòng nhập email và mật khẩu"
    )

    # Capture screenshot as test evidence
    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "login_fail_empty_fields.png"
        )
    )

    # Assert: Verify that the validation message is displayed
    sem_text = " ".join(
        page.locator("flt-semantics").all_text_contents()
    )

    assert (
        "Vui lòng nhập email và mật khẩu"
        in sem_text
    )
