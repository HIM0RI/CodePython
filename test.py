# ================================================================
# ĐỀ TÀI SỐ 38: QUẢN LÝ HỒ SƠ TUYỂN DỤNG BẰNG PYTHON
# Chương trình console, sử dụng list/dictionary và file TXT (JSON).
# Cách chạy: python quan_ly_tuyen_dung.py
# ================================================================
 
import json
import re
from datetime import date
from pathlib import Path
 
# ------------------------- CẤU HÌNH -------------------------------
DATA_FILE = Path(__file__).with_name("ho_so_tuyen_dung.txt")
 
# Trọng số điểm: điểm hồ sơ 40%, điểm phỏng vấn 60%.
PROFILE_WEIGHT = 0.40
INTERVIEW_WEIGHT = 0.60
 
# Ngưỡng đạt mặc định để thống kê.
PASS_THRESHOLD = 5.0
 
VALID_STATUSES = ["Mới", "Đang xử lý", "Đã tuyển", "Từ chối"]
 
# ---------------------- HÀM KIỂM TRA DỮ LIỆU ----------------------
def input_non_empty(prompt):
    """Nhập chuỗi không được để trống."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Dữ liệu không được để trống. Vui lòng nhập lại.")
 
 
def input_phone(prompt="Số điện thoại: "):
    """Số điện thoại được lưu dạng chuỗi để không mất số 0 ở đầu."""
    while True:
        value = input(prompt).strip().replace(" ", "")
        if value.isdigit() and 9 <= len(value) <= 11 and value.startswith("0"):
            return value
        print("Số điện thoại phải gồm 9-11 chữ số và bắt đầu bằng số 0.")
 
 
def input_email(prompt="Email: "):
    """Kiểm tra email ở mức cơ bản."""
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    while True:
        value = input(prompt).strip()
        if re.fullmatch(pattern, value):
            return value
        print("Email chưa đúng định dạng. Ví dụ: ten@example.com")
 
 
def input_int_min(prompt, minimum=0):
    """Nhập số nguyên không nhỏ hơn minimum."""
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
            if value >= minimum:
                return value
            print(f"Giá trị phải lớn hơn hoặc bằng {minimum}.")
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ.")
 
 
def input_float_range(prompt, minimum=0.0, maximum=None):
    """Nhập số thực trong khoảng cho phép; chấp nhận dấu phẩy thập phân."""
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            value = float(raw)
            if value < minimum:
                print(f"Giá trị không được nhỏ hơn {minimum}.")
                continue
            if maximum is not None and value > maximum:
                print(f"Giá trị không được lớn hơn {maximum}.")
                continue
            return value
        except ValueError:
            print("Vui lòng nhập một số hợp lệ.")
 
 
def input_interview_date(prompt="Ngày phỏng vấn (YYYY-MM-DD): "):
    """Kiểm tra ngày theo định dạng ISO YYYY-MM-DD và ngày có thật."""
    while True:
        raw = input(prompt).strip()
        try:
            parsed = date.fromisoformat(raw)
            return parsed.isoformat()
        except ValueError:
            print("Ngày không hợp lệ. Hãy nhập theo dạng YYYY-MM-DD, ví dụ 2026-11-25.")
 
 
def input_status(prompt="Trạng thái (1-Mới, 2-Đang xử lý, 3-Đã tuyển, 4-Từ chối): "):
    """Chọn trạng thái từ danh sách có sẵn để tránh nhập sai."""
    for index, status in enumerate(VALID_STATUSES, start=1):
        print(f"  {index}. {status}")
    while True:
        choice = input(prompt).strip()
        if choice in {"1", "2", "3", "4"}:
            return VALID_STATUSES[int(choice) - 1]
        print("Lựa chọn không hợp lệ. Vui lòng chọn từ 1 đến 4.")
 
 
def find_candidate_index_by_id(candidates, candidate_id):
    """Tìm vị trí ứng viên theo mã; trả về -1 nếu không tìm thấy."""
    target = candidate_id.strip().casefold()
    for index, candidate in enumerate(candidates):
        if candidate["ma_ung_vien"].casefold() == target:
            return index
    return -1
 
 
def calculate_total_score(candidate):
    """Tính điểm tổng hợp theo trọng số đã khai báo."""
    return (
        candidate["diem_ho_so"] * PROFILE_WEIGHT
        + candidate["diem_phong_van"] * INTERVIEW_WEIGHT
    )
 
 
def classify_result(candidate):
    """Xếp loại theo ngưỡng điểm tổng hợp."""
    return "Đạt" if calculate_total_score(candidate) >= PASS_THRESHOLD else "Không đạt"
 
 
def format_money(amount):
    """Định dạng số tiền theo cách viết thông dụng tại Việt Nam."""
    return f"{amount:,.0f}".replace(",", ".")
 
# ------------------------ HIỂN THỊ DỮ LIỆU -------------------------
def display_candidates(candidates):
    """In danh sách ứng viên ra màn hình dạng bảng."""
    if not candidates:
        print("Danh sách hiện đang trống.")
        return
 
    print("\n" + "=" * 150)
    print(
        f"{'Mã UV':<9} {'Họ tên':<22} {'Vị trí':<18} {'Kinh nghiệm':>11} "
        f"{'Điểm HS':>8} {'Điểm PV':>8} {'Tổng điểm':>10} {'Kết quả':<11} {'Trạng thái':<14}"
    )
    print("-" * 150)
    for candidate in candidates:
        total = calculate_total_score(candidate)
        print(
            f"{candidate['ma_ung_vien']:<9} "
            f"{candidate['ho_ten'][:21]:<22} "
            f"{candidate['vi_tri'][:17]:<18} "
            f"{candidate['so_nam_kinh_nghiem']:>11} "
            f"{candidate['diem_ho_so']:>8.1f} "
            f"{candidate['diem_phong_van']:>8.1f} "
            f"{total:>10.2f} "
            f"{classify_result(candidate):<11} "
            f"{candidate['trang_thai']:<14}"
        )
    print("=" * 150)
 
 
def display_candidate_detail(candidate):
    """In đầy đủ thông tin của một ứng viên."""
    print("\n--- THÔNG TIN CHI TIẾT ỨNG VIÊN ---")
    print(f"Mã ứng viên       : {candidate['ma_ung_vien']}")
    print(f"Họ tên            : {candidate['ho_ten']}")
    print(f"Số điện thoại     : {candidate['so_dien_thoai']}")
    print(f"Email             : {candidate['email']}")
    print(f"Vị trí ứng tuyển  : {candidate['vi_tri']}")
    print(f"Số năm kinh nghiệm: {candidate['so_nam_kinh_nghiem']}")
    print(f"Điểm hồ sơ        : {candidate['diem_ho_so']:.1f}")
    print(f"Điểm phỏng vấn    : {candidate['diem_phong_van']:.1f}")
    print(f"Điểm tổng hợp     : {calculate_total_score(candidate):.2f}")
    print(f"Kết quả đánh giá  : {classify_result(candidate)}")
    print(f"Ngày phỏng vấn    : {candidate['ngay_phong_van']}")
    print(f"Mức lương đề xuất : {format_money(candidate['muc_luong'])} VND")
    print(f"Trạng thái hồ sơ  : {candidate['trang_thai']}")
 
# -------------------------- THÊM MỚI -------------------------------
def add_candidate(candidates):
    """Thêm ứng viên mới sau khi kiểm tra mã và các trường dữ liệu."""
    print("\n========== THÊM HỒ SƠ ỨNG VIÊN ==========")
    while True:
        candidate_id = input_non_empty("Mã ứng viên: ").upper()
        if find_candidate_index_by_id(candidates, candidate_id) == -1:
            break
        print("Mã ứng viên đã tồn tại. Vui lòng chọn mã khác.")
 
    candidate = {
        "ma_ung_vien": candidate_id,
        "ho_ten": input_non_empty("Họ tên: "),
        "so_dien_thoai": input_phone(),
        "email": input_email(),
        "vi_tri": input_non_empty("Vị trí ứng tuyển: "),
        "so_nam_kinh_nghiem": input_int_min("Số năm kinh nghiệm: ", 0),
        "diem_ho_so": input_float_range("Điểm hồ sơ (0-10): ", 0, 10),
        "diem_phong_van": input_float_range("Điểm phỏng vấn (0-10): ", 0, 10),
        "ngay_phong_van": input_interview_date(),
        "trang_thai": input_status(),
        "muc_luong": input_float_range("Mức lương đề xuất (VND): ", 0),
    }
 
    candidates.append(candidate)
    print("Đã thêm hồ sơ ứng viên thành công.")
    print(f"Điểm tổng hợp tạm tính: {calculate_total_score(candidate):.2f}/10 - {classify_result(candidate)}")
 
# -------------------------- CẬP NHẬT --------------------------------
def update_candidate(candidates):
    """Cập nhật một trường thông tin của ứng viên theo mã."""
    print("\n========== CẬP NHẬT HỒ SƠ ==========")
    candidate_id = input_non_empty("Nhập mã ứng viên cần cập nhật: ")
    index = find_candidate_index_by_id(candidates, candidate_id)
    if index == -1:
        print("Không tìm thấy mã ứng viên.")
        return
 
    candidate = candidates[index]
    display_candidate_detail(candidate)
    while True:
        print("\nChọn thông tin muốn sửa:")
        print("1. Họ tên              2. Số điện thoại")
        print("3. Email               4. Vị trí ứng tuyển")
        print("5. Số năm kinh nghiệm  6. Điểm hồ sơ")
        print("7. Điểm phỏng vấn      8. Ngày phỏng vấn")
        print("9. Trạng thái          10. Mức lương đề xuất")
        print("0. Quay lại")
        choice = input("Lựa chọn: ").strip()
 
        if choice == "1":
            candidate["ho_ten"] = input_non_empty("Họ tên mới: ")
        elif choice == "2":
            candidate["so_dien_thoai"] = input_phone("Số điện thoại mới: ")
        elif choice == "3":
            candidate["email"] = input_email("Email mới: ")
        elif choice == "4":
            candidate["vi_tri"] = input_non_empty("Vị trí mới: ")
        elif choice == "5":
            candidate["so_nam_kinh_nghiem"] = input_int_min("Số năm kinh nghiệm mới: ", 0)
        elif choice == "6":
            candidate["diem_ho_so"] = input_float_range("Điểm hồ sơ mới (0-10): ", 0, 10)
        elif choice == "7":
            candidate["diem_phong_van"] = input_float_range("Điểm phỏng vấn mới (0-10): ", 0, 10)
        elif choice == "8":
            candidate["ngay_phong_van"] = input_interview_date("Ngày phỏng vấn mới (YYYY-MM-DD): ")
        elif choice == "9":
            candidate["trang_thai"] = input_status()
        elif choice == "10":
            candidate["muc_luong"] = input_float_range("Mức lương mới (VND): ", 0)
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ.")
            continue
 
        print("Đã cập nhật thông tin.")
        print(f"Điểm tổng hợp hiện tại: {calculate_total_score(candidate):.2f}/10")
 
# ---------------------------- XÓA -----------------------------------
def delete_candidate(candidates):
    """Xóa ứng viên theo mã và bắt buộc xác nhận."""
    print("\n========== XÓA HỒ SƠ ==========")
    candidate_id = input_non_empty("Nhập mã ứng viên cần xóa: ")
    index = find_candidate_index_by_id(candidates, candidate_id)
    if index == -1:
        print("Không tìm thấy mã ứng viên.")
        return
 
    display_candidate_detail(candidates[index])
    confirm = input("Bạn chắc chắn muốn xóa? (Y/N): ").strip().upper()
    if confirm == "Y":
        removed = candidates.pop(index)
        print(f"Đã xóa hồ sơ {removed['ma_ung_vien']}.")
    else:
        print("Đã hủy thao tác xóa. Dữ liệu được giữ nguyên.")
 
# --------------------------- TÌM KIẾM --------------------------------
def search_candidates(candidates):
    """Tìm kiếm theo mã/họ tên, vị trí hoặc ngày phỏng vấn."""
    print("\n========== TÌM KIẾM HỒ SƠ ==========")
    print("1. Tìm theo mã ứng viên hoặc họ tên")
    print("2. Tìm theo vị trí ứng tuyển")
    print("3. Tìm theo ngày phỏng vấn")
    choice = input("Lựa chọn: ").strip()
 
    results = []
    if choice == "1":
        keyword = input_non_empty("Nhập mã hoặc một phần họ tên: ").casefold()
        results = [c for c in candidates
                   if keyword in c["ma_ung_vien"].casefold()
                   or keyword in c["ho_ten"].casefold()]
    elif choice == "2":
        keyword = input_non_empty("Nhập vị trí cần tìm: ").casefold()
        results = [c for c in candidates if keyword in c["vi_tri"].casefold()]
    elif choice == "3":
        interview_day = input_interview_date("Nhập ngày cần tìm (YYYY-MM-DD): ")
        results = [c for c in candidates if c["ngay_phong_van"] == interview_day]
    else:
        print("Lựa chọn không hợp lệ.")
        return
 
    print(f"Tìm thấy {len(results)} hồ sơ.")
    display_candidates(results)
 
# ----------------------------- SẮP XẾP -------------------------------
def sort_candidates(candidates):
    """Sắp xếp theo điểm phỏng vấn, điểm tổng hợp hoặc kinh nghiệm."""
    print("\n========== SẮP XẾP HỒ SƠ ==========")
    print("1. Điểm tổng hợp")
    print("2. Điểm phỏng vấn")
    print("3. Số năm kinh nghiệm")
    criterion = input("Tiêu chí sắp xếp: ").strip()
    print("1. Tăng dần")
    print("2. Giảm dần")
    direction = input("Thứ tự: ").strip()
    if direction not in {"1", "2"}:
        print("Lựa chọn thứ tự không hợp lệ.")
        return
 
    if criterion == "1":
        key_function = calculate_total_score
    elif criterion == "2":
        key_function = lambda candidate: candidate["diem_phong_van"]
    elif criterion == "3":
        key_function = lambda candidate: candidate["so_nam_kinh_nghiem"]
    else:
        print("Tiêu chí không hợp lệ.")
        return
 
    sorted_list = sorted(candidates, key=key_function, reverse=(direction == "2"))
    print("Kết quả sắp xếp:")
    display_candidates(sorted_list)
 
# ---------------------- TÍNH TOÁN / THỐNG KÊ -------------------------
def show_statistics(candidates):
    """Tính điểm trung bình, tỷ lệ đạt/không đạt và thống kê theo vị trí."""
    print("\n========== TÍNH TOÁN VÀ THỐNG KÊ ==========")
    if not candidates:
        print("Chưa có dữ liệu để thống kê.")
        return
 
    total_candidates = len(candidates)
    scores = [calculate_total_score(candidate) for candidate in candidates]
    passed = sum(1 for candidate in candidates if classify_result(candidate) == "Đạt")
    failed = total_candidates - passed
    average_score = sum(scores) / total_candidates
    pass_rate = passed / total_candidates * 100
    best = max(candidates, key=calculate_total_score)
    worst = min(candidates, key=calculate_total_score)
 
    print(f"Tổng số ứng viên : {total_candidates}")
    print(f"Điểm trung bình  : {average_score:.2f}/10")
    print(f"Số ứng viên đạt  : {passed}")
    print(f"Số ứng viên rớt  : {failed}")
    print(f"Tỷ lệ đạt        : {pass_rate:.2f}%")
    print(f"Ngưỡng đạt       : {PASS_THRESHOLD:.1f}/10")
    print(f"Ứng viên cao nhất: {best['ho_ten']} ({calculate_total_score(best):.2f})")
    print(f"Ứng viên thấp nhất: {worst['ho_ten']} ({calculate_total_score(worst):.2f})")
 
    score_by_position = {}
    for candidate in candidates:
        position = candidate["vi_tri"]
        score_by_position.setdefault(position, []).append(calculate_total_score(candidate))
 
    print("\nĐiểm trung bình theo vị trí:")
    for position, position_scores in sorted(score_by_position.items()):
        position_average = sum(position_scores) / len(position_scores)
        print(f"- {position}: {position_average:.2f}/10 ({len(position_scores)} ứng viên)")
 
# -------------------------- LƯU DỮ LIỆU ------------------------------
def save_data(candidates):
    """Lưu danh sách vào file TXT theo định dạng JSON, mã hóa UTF-8."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(candidates, file, ensure_ascii=False, indent=4)
        print(f"Đã lưu {len(candidates)} hồ sơ vào file: {DATA_FILE.name}")
    except (OSError, TypeError) as error:
        print(f"Không thể ghi file. Chi tiết: {error}")
 
 
def load_data():
    """Đọc file; nếu file chưa tồn tại, tự động tạo dữ liệu mẫu để hiển thị kết quả ngay."""
    if not DATA_FILE.exists():
        print(f"Chưa tìm thấy file {DATA_FILE.name}. Đang tự động tạo dữ liệu mẫu...")
        default_sample_data = [
            {
                "ma_ung_vien": "UV001",
                "ho_ten": "Nguyen Minh Anh",
                "so_dien_thoai": "0900000001",
                "email": "minhanh@example.com",
                "vi_tri": "Lap trinh Python",
                "so_nam_kinh_nghiem": 2,
                "diem_ho_so": 8.5,
                "diem_phong_van": 8.0,
                "ngay_phong_van": "2026-11-20",
                "trang_thai": "Đã tuyển",
                "muc_luong": 15000000
            },
            {
                "ma_ung_vien": "UV002",
                "ho_ten": "Tran Gia Bao",
                "so_dien_thoai": "0900000002",
                "email": "giabao@example.com",
                "vi_tri": "Ke toan",
                "so_nam_kinh_nghiem": 1,
                "diem_ho_so": 7.0,
                "diem_phong_van": 6.5,
                "ngay_phong_van": "2026-11-21",
                "trang_thai": "Đang xử lý",
                "muc_luong": 12000000
            },
            {
                "ma_ung_vien": "UV003",
                "ho_ten": "Le Thi Thu Ha",
                "so_dien_thoai": "0900000003",
                "email": "thuha@example.com",
                "vi_tri": "Nhan vien kinh doanh",
                "so_nam_kinh_nghiem": 3,
                "diem_ho_so": 9.0,
                "diem_phong_van": 8.5,
                "ngay_phong_van": "2026-11-22",
                "trang_thai": "Đã tuyển",
                "muc_luong": 18000000
            }
        ]
        try:
            with DATA_FILE.open("w", encoding="utf-8") as file:
                json.dump(default_sample_data, file, ensure_ascii=False, indent=4)
            print(f"Đã tạo thành công file mẫu {DATA_FILE.name} với 3 hồ sơ.")
        except OSError as error:
            print(f"Không thể tạo file mẫu: {error}")
        return default_sample_data
 
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            raw_data = json.load(file)
        if not isinstance(raw_data, list):
            print("Dữ liệu trong file không đúng định dạng danh sách.")
            return []
 
        candidates = []
        for record in raw_data:
            if isinstance(record, dict):
                candidates.append(record)
        print(f"Đọc thành công {len(candidates)} hồ sơ từ {DATA_FILE.name}.")
        return candidates
    except Exception as error:
        print(f"Lỗi khi đọc file: {error}")
        return []
 
# ---------------------------- MENU -----------------------------------
def show_menu():
    """Hiển thị menu chính."""
    print("\n" + "=" * 55)
    print("       CHƯƠNG TRÌNH QUẢN LÝ HỒ SƠ TUYỂN DỤNG")
    print("=" * 55)
    print("1. Thêm hồ sơ ứng viên")
    print("2. Hiển thị danh sách")
    print("3. Cập nhật hồ sơ")
    print("4. Xóa hồ sơ")
    print("5. Tìm kiếm")
    print("6. Sắp xếp")
    print("7. Tính toán / Thống kê")
    print("8. Lưu dữ liệu")
    print("9. Đọc dữ liệu từ file")
    print("0. Thoát")
    print("-" * 55)
 
 
def main():
    """Hàm điều khiển chính: nạp dữ liệu và hiển thị kết quả khởi động."""
    print("KHỞI ĐỘNG CHƯƠNG TRÌNH QUẢN LÝ TUYỂN DỤNG")
    candidates = load_data()
    
    # Tự động hiển thị kết quả danh sách ngay khi khởi động chương trình
    print("\n[KẾT QUẢ] Hiển thị danh sách hồ sơ hiện tại:")
    display_candidates(candidates)
 
    while True:
        show_menu()
        choice = input("Nhập lựa chọn của bạn: ").strip()
 
        if choice == "1":
            add_candidate(candidates)
        elif choice == "2":
            display_candidates(candidates)
        elif choice == "3":
            update_candidate(candidates)
        elif choice == "4":
            delete_candidate(candidates)
        elif choice == "5":
            search_candidates(candidates)
        elif choice == "6":
            sort_candidates(candidates)
        elif choice == "7":
            show_statistics(candidates)
        elif choice == "8":
            save_data(candidates)
        elif choice == "9":
            confirm = input("Đọc lại file sẽ thay thế danh sách đang có. Tiếp tục? (Y/N): ").strip().upper()
            if confirm == "Y":
                candidates = load_data()
        elif choice == "0":
            save_choice = input("Bạn có muốn lưu dữ liệu trước khi thoát? (Y/N): ").strip().upper()
            if save_choice == "Y":
                save_data(candidates)
            print("Cảm ơn bạn đã sử dụng chương trình. Tạm biệt!")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại từ 0 đến 9.")
 
 
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nChương trình đã được dừng bởi người dùng.")
