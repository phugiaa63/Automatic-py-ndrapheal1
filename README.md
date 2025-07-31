# Gmail 2FA Changer

Tool tự động thay đổi 2FA cho nhiều tài khoản Gmail từ file Excel/CSV.

## ⚠️ Cảnh báo quan trọng

- **Chỉ sử dụng cho tài khoản của chính bạn**
- **Backup dữ liệu trước khi chạy**
- **Google có thể phát hiện và chặn automation**
- **Sử dụng có trách nhiệm**

## 📋 Yêu cầu hệ thống

- Python 3.7+
- Chrome browser
- ChromeDriver (tự động tải)

## 🚀 Cài đặt

1. **Clone hoặc tải về project**
```bash
git clone <repository-url>
cd gmail-2fa-changer
```

2. **Cài đặt dependencies**
```bash
pip install -r requirements.txt
```

3. **Tạo file mẫu**
```bash
python create_sample_file.py
```

## 📁 Chuẩn bị dữ liệu

### Cấu trúc file Excel/CSV:

| email | password | current_2fa |
|-------|----------|-------------|
| example@gmail.com | your_password | 123456 |

### Các cột bắt buộc:
- **email**: Địa chỉ Gmail
- **password**: Mật khẩu tài khoản  
- **current_2fa**: Mã 2FA hiện tại (6 chữ số)

## 🔧 Sử dụng

### 1. Chuẩn bị file dữ liệu
- Sử dụng file mẫu `gmail_accounts_sample.xlsx`
- Thay thế dữ liệu mẫu bằng thông tin thật
- Backup file trước khi chạy

### 2. Chạy script
```bash
python gmail_2fa_changer.py
```

### 3. Nhập thông tin
- Đường dẫn file input
- Tên file output (mặc định: `updated_accounts.csv`)

## 📊 Kết quả

Script sẽ tạo file CSV với các cột:
- **email**: Địa chỉ Gmail
- **password**: Mật khẩu (giữ nguyên)
- **old_2fa**: 2FA cũ
- **new_2fa**: 2FA mới (backup codes)
- **status**: Trạng thái (success/error/need_password)
- **message**: Thông báo lỗi (nếu có)
- **timestamp**: Thời gian xử lý

## ⚙️ Tính năng

### 🔒 Bảo mật
- Random delays để tránh detection
- User agent thật
- Anti-automation bypass
- Session management

### 📝 Logging
- Log chi tiết vào file `gmail_2fa_changer.log`
- Backup kết quả tạm thời mỗi 10 tài khoản
- Timestamp cho mỗi thao tác

### 🛡️ Error Handling
- Xử lý captcha
- Retry mechanism
- Graceful error handling
- Keyboard interrupt support

## 🚨 Lưu ý quan trọng

### Rate Limiting
- Delay 5-10 giây giữa các tài khoản
- Random delays 2-5 giây cho mỗi thao tác
- Google có thể chặn nếu quá nhanh

### Captcha & Security
- Có thể gặp captcha khi đăng nhập nhiều lần
- Google có thể yêu cầu xác minh bổ sung
- Một số tài khoản có thể cần manual intervention

### Backup & Recovery
- Luôn backup file dữ liệu gốc
- Script tạo backup tạm thời mỗi 10 tài khoản
- Có thể resume từ điểm dừng

## 🔧 Troubleshooting

### Lỗi thường gặp:

1. **ChromeDriver không tìm thấy**
```bash
pip install webdriver-manager
```

2. **File không đúng format**
- Kiểm tra cấu trúc cột
- Đảm bảo file là CSV hoặc Excel

3. **Login failed**
- Kiểm tra email/password
- Đảm bảo 2FA code chính xác
- Tài khoản có thể bị khóa tạm thời

4. **Captcha xuất hiện**
- Dừng script và xử lý manual
- Đợi một thời gian rồi thử lại

## 📞 Hỗ trợ

Nếu gặp vấn đề:
1. Kiểm tra log file `gmail_2fa_changer.log`
2. Đảm bảo Chrome browser đã cài đặt
3. Kiểm tra kết nối internet
4. Thử với ít tài khoản trước

## ⚖️ Disclaimer

Tool này chỉ dành cho mục đích giáo dục và quản lý tài khoản cá nhân. Người dùng chịu trách nhiệm hoàn toàn về việc sử dụng tool này. Tác giả không chịu trách nhiệm về bất kỳ hậu quả nào phát sinh từ việc sử dụng tool.

## 📄 License

MIT License - Xem file LICENSE để biết thêm chi tiết.
