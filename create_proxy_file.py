#!/usr/bin/env python3
"""
Script tạo file proxy mẫu cho Gmail 2FA Changer Advanced
"""

def create_proxy_sample():
    """Tạo file proxy mẫu"""
    
    # Định dạng proxy mẫu
    proxy_formats = [
        "# HTTP Proxy",
        "http://username:password@proxy1.example.com:8080",
        "http://proxy2.example.com:3128",
        "",
        "# SOCKS5 Proxy", 
        "socks5://username:password@proxy3.example.com:1080",
        "socks5://proxy4.example.com:1080",
        "",
        "# HTTPS Proxy",
        "https://proxy5.example.com:443",
        "",
        "# Lưu ý:",
        "# - Thay thế example.com bằng proxy thật",
        "# - Thêm username:password nếu cần",
        "# - Mỗi dòng 1 proxy",
        "# - Dòng bắt đầu bằng # là comment"
    ]
    
    # Lưu file
    output_file = 'proxies_sample.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in proxy_formats:
            f.write(line + '\n')
    
    print(f"✅ Đã tạo file proxy mẫu: {output_file}")
    print("\n📋 Hướng dẫn:")
    print("1. Thay thế example.com bằng proxy thật")
    print("2. Thêm username:password nếu proxy yêu cầu auth")
    print("3. Mỗi dòng chỉ chứa 1 proxy")
    print("4. Dòng bắt đầu bằng # sẽ bị bỏ qua")
    print("\n🌐 Các loại proxy hỗ trợ:")
    print("- HTTP: http://proxy:port")
    print("- HTTPS: https://proxy:port") 
    print("- SOCKS5: socks5://proxy:port")
    print("- Với auth: protocol://user:pass@proxy:port")

if __name__ == "__main__":
    create_proxy_sample() 