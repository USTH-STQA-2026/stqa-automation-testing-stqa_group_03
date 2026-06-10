"""
Search & Filter Tests — Library Book Borrowing System
"""

import os

from conftest import (
    enable_flutter_semantics,
    flutter_fill,
    login,
    SCREENSHOT_DIR,
)


def test_search_book_by_name(page, test_config):
    """TC-04: Search book by name"""

    login(page, test_config)
    enable_flutter_semantics(page)

    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "Flutter"
    )

    page.wait_for_timeout(2000)

    books = page.locator(
        'flt-semantics[aria-label*="Flutter"]'
    )

    assert books.count() > 0

    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "tc04_search_by_name.png"
        )
    )


def test_search_book_no_result(page, test_config):
    """TC-05: Search book with no result"""

    login(page, test_config)
    enable_flutter_semantics(page)

    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "xyz_khong_ton_tai_12345"
    )

    page.wait_for_timeout(2000)

    books = page.locator(
        'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'
    )

    assert books.count() == 0

    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "tc05_search_no_result.png"
        )
    )


def test_filter_by_category(page, test_config):
    """TC-06: Filter books by category"""

    login(page, test_config)
    enable_flutter_semantics(page)

    flutter_fill(
        page,
        "Lọc theo thể loại (VD: Công nghệ, Kinh tế...)",
        "Công nghệ"
    )

    page.wait_for_timeout(2000)

    books = page.locator(
        'flt-semantics[role="group"][aria-label*="Mã: BOOK"]'
    )

    assert books.count() > 0

    for i in range(books.count()):
        label = books.nth(i).get_attribute("aria-label")
        assert "Công nghệ" in label

    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "tc06_filter_by_category.png"
        )
    )


def test_search_by_author(page, test_config):
    """TC-07: Search by author"""

    login(page, test_config)
    enable_flutter_semantics(page)

    flutter_fill(
        page,
        "Tìm kiếm theo tên sách hoặc tác giả...",
        "Nguyễn Minh Đức"
    )

    page.wait_for_timeout(2000)

    books = page.locator(
        'flt-semantics[aria-label*="Nguyễn Minh Đức"]'
    )

    assert books.count() > 0

    page.screenshot(
        path=os.path.join(
            SCREENSHOT_DIR,
            "tc07_search_by_author.png"
        )
    )
