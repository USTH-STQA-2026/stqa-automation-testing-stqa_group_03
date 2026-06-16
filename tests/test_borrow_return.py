
"""
Borrow & Return Tests  — Library Book Borrowing System
"""
"""Borrow & Return Tests (*Kiểm thử Mượn & Trả sách*) — Library Book Borrowing System

✅ OPTIMIZED FOR STABILITY (*ĐÃ TỐI ƯU HÓA LUỒNG LIÊN TỤC*)
"""
import os
import time
import pytest

from conftest import (
    enable_flutter_semantics, flutter_fill, flutter_click_button,
    login, SCREENSHOT_DIR, wait_for_flutter
)

def test_borrow_book(page, test_config):
    """TC-08: Borrow a book successfully"""

    # Login with a valid member account
    login(page, test_config)
    
    # Enable Flutter semantics for reliable element detection
    enable_flutter_semantics(page)

    # Click the borrow book button
    borrow_btn = page.locator('flt-semantics[role="button"]:has-text("Mượn sách này")').first
    borrow_btn.click()

    # Confirm the borrowing action
    confirm_btn = page.locator('flt-semantics[role="button"]:has-text("Mượn")').first
    confirm_btn.click()

    # Wait for the success message to appear
    wait_for_flutter(page, text="Mượn sách thành công")
    
    # Verify that the success message is displayed
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Mượn sách thành công" in sem_text, "Không tìm thấy thông báo mượn sách thành công!"
    
    # Capture screenshot as test evidence
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC08_borrow_book_success.png"))


def test_view_borrowed_books(page, test_config):
    """TC-09: Verify borrowed books are shown in 'Mượn / Trả' tab"""

    # Login with a valid member account
    login(page, test_config)

    # Enable Flutter semantics
    enable_flutter_semantics(page)

    # Open the Borrow / Return management tab
    borrow_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_tab.click()

    # Wait until borrowed book information is loaded
    wait_for_flutter(page, text="Trả sách")

    # Verify that borrowed books are displayed
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Đang mượn" in sem_text or "Trả sách" in sem_text, "Không tìm thấy sách đang mượn trong tab quản lý!"

    # Capture screenshot as test evidence
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC09_view_borrowed_books.png"))


def test_return_book(page, test_config):
    """TC-10: Return a borrowed book successfully"""

    # Login with a valid member account
    login(page, test_config)

    # Enable Flutter semantics
    enable_flutter_semantics(page)

    # Navigate to the Borrow / Return tab
    borrow_tab = page.locator('flt-semantics[role="tab"][aria-label="Mượn / Trả"]')
    borrow_tab.click()

    # Click the return book button
    return_btn = page.locator('flt-semantics[role="button"]:has-text("Trả sách")').first
    return_btn.click()

    # Wait for the return success message
    wait_for_flutter(page, text="Trả sách thành công")
    
    # Verify that the return operation completed successfully
    sem_text = " ".join(page.locator("flt-semantics").all_text_contents())
    assert "Trả sách thành công" in sem_text, "Không nhìn thấy thông báo trả sách thành công!"

    # Capture screenshot as test evidence
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "TC10_return_book_success.png"))
