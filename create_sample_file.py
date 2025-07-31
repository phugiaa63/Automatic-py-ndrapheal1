#!/usr/bin/env python3
"""
Script tạo file Excel mẫu cho Gmail 2FA Changer
"""

import pandas as pd
import os

def create_sample_file():
    """Tạo file Excel mẫu"""
    
    # Tạo dữ liệu mẫu
    sample_data = {
        'email': [
            'example1@gmail.com',
            'example2@gmail.com', 
            'example3@gmail.com'
        ],
        'password': [
            'your_password_1',
            'your_password_2',
            'your_password_3'
        ],
        'current_2fa': [
            '123456',  # 6-digit code hiện tại
            '654321',
            '111111'
        ]
    }
    
    # Tạo DataFrame
    df = pd.DataFrame(sample_data)
    
    # Lưu file
    output_file = 'gmail_accounts_sample.xlsx'
    df.to_excel(output_file, index=False)
    
    print(f"✅ Đã tạo file mẫu: {output_file}")
    print("\n📋 Cấu trúc file:")
    print("- email: Địa chỉ Gmail")
    print("- password: Mật khẩu tài khoản")
    print("- current_2fa: Mã 2FA hiện tại (6 chữ số)")
    print("\n⚠️  Lưu ý:")
    print("- Thay thế dữ liệu mẫu bằng thông tin thật")
    print("- Đảm bảo mật khẩu và 2FA chính xác")
    print("- Backup file trước khi chạy script chính")

if __name__ == "__main__":
    create_sample_file() 