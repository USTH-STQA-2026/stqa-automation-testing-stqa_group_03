
"""
Logout & Language Tests — Library Book Borrowing System
"""

import os

from conftest import (
    enable_flutter_semantics,
    login,
    SCREENSHOT_DIR,
)


def test_logout(page, test_config):
    """TC-11: Logout success"""

    # Login
    login(page, test_config)

    # Ensure semantics are enabled
    enable_flutter_semantics(page)

    # Click Logout button
    logout_btn = page.locator(
        'flt-semantics[role="button"]:has-text("Đăng xuất")'
    ).first

    logout_btn.click()

    # Wait for page navigation
    page.wait_for_timeout(3000)

    # Re-enable semantics after navigation
    try:
        enable_flutter_semantics(page)
    except Exception:
        pass

    # Verify login page appears again
    sem_text = " ".join(
        page.locator("flt-semantics").all_text_contents()
    )

    assert (
        "Đăng nhập" in sem_text
        or "Email" in sem_text
    )

    # Evidence
    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "tc11_logout_success.png"
        )
    )


def test_switch_language_to_english(page, test_config):
    """TC-12: Switch language to English"""

    # Login
    login(page, test_config)

    # Ensure semantics are enabled
    enable_flutter_semantics(page)

    # Click EN button
    en_btn = page.locator(
        'flt-semantics[role="button"]:has-text("EN")'
    ).first

    en_btn.click()

    # Wait for language switching
    page.wait_for_timeout(2500)

    # Re-enable semantics
    try:
        enable_flutter_semantics(page)
    except Exception:
        pass

    # Verify English UI
    sem_text = " ".join(
        page.locator("flt-semantics").all_text_contents()
    )

    assert (
        "Logout" in sem_text
        or "Borrow" in sem_text
        or "Library" in sem_text
    )

    # Evidence
    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "tc12_switch_language_en.png"
        )
    )

