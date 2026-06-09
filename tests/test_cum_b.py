import pytest
from conftest import login, wait_for_flutter
from pages.search_page import SearchPage
from pages.cart_page import CartPage

# --- CHỨC NĂNG TÌM KIẾM & BỘ LỌC ---

def test_search_happy_path(page, test_config):
    """Tìm kiếm sản phẩm thông thường hợp lệ."""
    page.goto(test_config["base_url"])
    search_page = SearchPage(page)
    search_page.search_product("iPhone")
    assert page.locator('flt-semantics:has-text("iPhone")').first.is_visible()

def test_filter_bug_min_greater_than_max(page, test_config):
    """[BẪY BUG] BVA: Nhập Giá Tối Thiểu LỚN HƠN Giá Tối Đa."""
    page.goto(test_config["base_url"])
    search_page = SearchPage(page)
    search_page.apply_price_filter("5000000", "1000000") # Min 5tr > Max 1tr
    
    # Kỳ vọng: Hệ thống phải báo lỗi logic. Nếu không báo lỗi -> Thầy dính bug!
    error_msg = page.locator('flt-semantics:has-text("Khoảng giá không hợp lệ")').first
    assert error_msg.is_visible(), "BUG_FOUND: Hệ thống không chặn lỗi khi nhập giá Min > Max!"

# --- CHỨC NĂNG GIỎ HÀNG (Yêu cầu đăng nhập độc lập) ---

def test_cart_bug_negative_quantity(page, test_config):
    """[BẪY BUG] BVA: Cố tình sửa số lượng thành SỐ ÂM trong giỏ hàng."""
    login(page, test_config) # Gọi hàm login tự động độc lập của thầy
    page.goto(f"{test_config['base_url']}/#/cart")
    
    cart_page = CartPage(page)
    cart_page.update_quantity("-5") # Nhập số lượng âm
    
    # Kỳ vọng: Giao diện phải chặn lại và hiển thị cảnh báo lỗi
    error_alert = page.locator('flt-semantics:has-text("Số lượng không hợp lệ")').first
    assert error_alert.is_visible(), "BUG_FOUND: Hệ thống cho phép lưu số lượng âm trong giỏ hàng!"