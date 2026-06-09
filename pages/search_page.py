from conftest import smart_fill, smart_click, wait_for_flutter

class SearchPage:
    def __init__(self, page):
        self.page = page

    def search_product(self, keyword):
        # Điền từ khóa và click nút Tìm (Hàm thầy viết sẵn tự nhận diện Flutter)
        smart_fill(self.page, "Tìm kiếm sản phẩm", keyword)
        smart_click(self.page, "Tìm")
        wait_for_flutter(self.page)

    def apply_price_filter(self, min_price, max_price):
        # Điền khoảng giá và click Áp dụng
        smart_fill(self.page, "Giá tối thiểu", min_price)
        smart_fill(self.page, "Giá tối đa", max_price)
        smart_click(self.page, "Áp dụng bộ lọc")
        wait_for_flutter(self.page)