from conftest import smart_fill, smart_click, wait_for_flutter

class CartPage:
    def __init__(self, page):
        self.page = page

    def update_quantity(self, quantity_value):
        # Tìm ô Số lượng trong giỏ hàng để sửa
        smart_fill(self.page, "Số lượng", quantity_value)
        smart_click(self.page, "Cập nhật giỏ hàng")
        wait_for_flutter(self.page)