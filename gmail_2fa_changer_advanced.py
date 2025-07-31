#!/usr/bin/env python3
"""
Gmail 2FA Changer Advanced - Phiên bản nâng cao với xử lý captcha và proxy
Author: Assistant
Version: 2.0
"""

import pandas as pd
import time
import random
import json
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
from datetime import datetime
import threading
from queue import Queue
import pickle

class Gmail2FAChangerAdvanced:
    def __init__(self, input_file, output_file="updated_accounts_advanced.csv", 
                 use_proxy=False, proxy_list=None, max_workers=3):
        self.input_file = input_file
        self.output_file = output_file
        self.use_proxy = use_proxy
        self.proxy_list = proxy_list or []
        self.max_workers = max_workers
        self.driver = None
        self.session_cookies = {}
        self.setup_logging()
        
    def setup_logging(self):
        """Thiết lập logging nâng cao"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - [%(threadName)s] %(message)s',
            handlers=[
                logging.FileHandler('gmail_2fa_changer_advanced.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self, proxy=None):
        """Thiết lập Chrome driver với options nâng cao"""
        chrome_options = Options()
        
        # Basic options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Advanced anti-detection
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")
        chrome_options.add_argument("--disable-default-apps")
        
        # User agent rotation
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        # Proxy support
        if proxy and self.use_proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')
            
        # Window size
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Additional stealth
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": random.choice(user_agents)
        })
        
    def load_session_cookies(self, email):
        """Load session cookies nếu có"""
        cookie_file = f"cookies_{email.replace('@', '_').replace('.', '_')}.pkl"
        if os.path.exists(cookie_file):
            try:
                with open(cookie_file, 'rb') as f:
                    cookies = pickle.load(f)
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                self.logger.info(f"Đã load cookies cho {email}")
                return True
            except Exception as e:
                self.logger.warning(f"Không thể load cookies cho {email}: {e}")
        return False
        
    def save_session_cookies(self, email):
        """Lưu session cookies"""
        try:
            cookies = self.driver.get_cookies()
            cookie_file = f"cookies_{email.replace('@', '_').replace('.', '_')}.pkl"
            with open(cookie_file, 'wb') as f:
                pickle.dump(cookies, f)
            self.logger.info(f"Đã lưu cookies cho {email}")
        except Exception as e:
            self.logger.warning(f"Không thể lưu cookies cho {email}: {e}")
            
    def solve_captcha(self):
        """Xử lý captcha (cần manual intervention)"""
        try:
            # Tìm captcha element
            captcha_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.ID, "captchaimg"))
            )
            
            self.logger.warning("Phát hiện CAPTCHA! Cần xử lý manual")
            
            # Hiển thị captcha cho user
            captcha_src = captcha_element.get_attribute("src")
            print(f"\n🔒 CAPTCHA detected: {captcha_src}")
            print("Vui lòng mở link trên và giải captcha, sau đó nhấn Enter để tiếp tục...")
            input()
            
            return True
        except TimeoutException:
            return False
            
    def handle_security_challenge(self):
        """Xử lý các thử thách bảo mật"""
        try:
            # Kiểm tra các loại challenge
            challenge_types = [
                "//div[contains(text(), 'Verify it's you')]",
                "//div[contains(text(), 'Security check')]",
                "//div[contains(text(), 'Unusual activity')]"
            ]
            
            for xpath in challenge_types:
                try:
                    challenge = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                    self.logger.warning("Phát hiện security challenge!")
                    print("\n🔐 Security challenge detected!")
                    print("Vui lòng xử lý manual và nhấn Enter để tiếp tục...")
                    input()
                    return True
                except TimeoutException:
                    continue
                    
            return False
        except Exception as e:
            self.logger.error(f"Lỗi xử lý security challenge: {e}")
            return False
            
    def login_gmail_advanced(self, email, password):
        """Đăng nhập Gmail với xử lý nâng cao"""
        try:
            self.logger.info(f"Đang đăng nhập: {email}")
            
            # Truy cập trang đăng nhập
            self.driver.get("https://accounts.google.com/signin")
            self.random_delay(3, 6)
            
            # Load cookies nếu có
            self.load_session_cookies(email)
            
            # Refresh page sau khi load cookies
            self.driver.refresh()
            self.random_delay(2, 4)
            
            # Kiểm tra xem đã đăng nhập chưa
            if "myaccount.google.com" in self.driver.current_url:
                self.logger.info(f"Đã đăng nhập sẵn cho {email}")
                return "success"
                
            # Nhập email
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "identifier"))
            )
            self.type_like_human(email_input, email)
            
            # Click Next
            next_button = self.driver.find_element(By.ID, "identifierNext")
            next_button.click()
            self.random_delay(2, 4)
            
            # Xử lý captcha nếu có
            if self.solve_captcha():
                self.random_delay(3, 6)
                
            # Nhập password
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            self.type_like_human(password_input, password)
            
            # Click Next
            password_next = self.driver.find_element(By.ID, "passwordNext")
            password_next.click()
            self.random_delay(3, 6)
            
            # Xử lý security challenge
            if self.handle_security_challenge():
                self.random_delay(3, 6)
                
            # Kiểm tra 2FA
            try:
                totp_input = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "totpPin"))
                )
                self.logger.info("Cần nhập 2FA")
                return "need_2fa"
            except TimeoutException:
                # Kiểm tra đăng nhập thành công
                if "myaccount.google.com" in self.driver.current_url or "mail.google.com" in self.driver.current_url:
                    self.logger.info("Đăng nhập thành công")
                    self.save_session_cookies(email)
                    return "success"
                else:
                    self.logger.warning("Không thể xác định trạng thái đăng nhập")
                    return "unknown"
                    
        except Exception as e:
            self.logger.error(f"Lỗi đăng nhập {email}: {e}")
            return "error"
            
    def type_like_human(self, element, text):
        """Gõ text như người thật"""
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.15))
            
    def random_delay(self, min_seconds=2, max_seconds=5):
        """Delay ngẫu nhiên"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    def process_account_advanced(self, email, password, current_2fa):
        """Xử lý tài khoản với logic nâng cao"""
        try:
            # Setup driver với proxy ngẫu nhiên
            proxy = random.choice(self.proxy_list) if self.proxy_list else None
            self.setup_driver(proxy)
            
            # Đăng nhập
            login_status = self.login_gmail_advanced(email, password)
            
            if login_status == "need_2fa":
                # Nhập 2FA
                if not self.enter_current_2fa(current_2fa):
                    return {"status": "error", "message": "Không thể nhập 2FA"}
                    
            elif login_status == "error":
                return {"status": "error", "message": "Lỗi đăng nhập"}
                
            # Điều hướng và thay đổi 2FA
            if not self.navigate_to_security_settings():
                return {"status": "error", "message": "Không thể truy cập security settings"}
                
            new_2fa = self.change_2fa()
            
            if new_2fa == "need_password":
                return {"status": "need_password", "message": "Cần password để xác nhận"}
            elif new_2fa:
                return {"status": "success", "new_2fa": new_2fa}
            else:
                return {"status": "error", "message": "Không thể thay đổi 2FA"}
                
        except Exception as e:
            self.logger.error(f"Lỗi xử lý {email}: {e}")
            return {"status": "error", "message": str(e)}
        finally:
            if self.driver:
                self.driver.quit()
                
    def worker(self, queue, results):
        """Worker thread để xử lý tài khoản"""
        while True:
            try:
                account_data = queue.get_nowait()
            except:
                break
                
            email = account_data['email']
            password = account_data['password']
            current_2fa = account_data['current_2fa']
            
            self.logger.info(f"Worker {threading.current_thread().name} xử lý: {email}")
            
            result = self.process_account_advanced(email, password, current_2fa)
            
            result_data = {
                'email': email,
                'password': password,
                'old_2fa': current_2fa,
                'new_2fa': result.get('new_2fa', ''),
                'status': result['status'],
                'message': result.get('message', ''),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'worker': threading.current_thread().name
            }
            
            results.append(result_data)
            queue.task_done()
            
    def run_parallel(self):
        """Chạy script với multi-threading"""
        try:
            # Load accounts
            accounts_df = self.load_accounts()
            
            # Tạo queue và results
            queue = Queue()
            results = []
            
            # Thêm accounts vào queue
            for _, row in accounts_df.iterrows():
                queue.put({
                    'email': row['email'],
                    'password': row['password'],
                    'current_2fa': row['current_2fa']
                })
                
            # Tạo workers
            threads = []
            for i in range(min(self.max_workers, len(accounts_df))):
                thread = threading.Thread(
                    target=self.worker,
                    args=(queue, results),
                    name=f"Worker-{i+1}"
                )
                thread.start()
                threads.append(thread)
                
            # Đợi tất cả hoàn thành
            queue.join()
            for thread in threads:
                thread.join()
                
            # Lưu kết quả
            final_df = pd.DataFrame(results)
            final_df.to_csv(self.output_file, index=False)
            
            self.logger.info(f"Hoàn thành! Đã xử lý {len(results)} tài khoản")
            
        except Exception as e:
            self.logger.error(f"Lỗi trong quá trình chạy: {e}")
            
    def load_accounts(self):
        """Load danh sách tài khoản"""
        try:
            if self.input_file.endswith('.csv'):
                df = pd.read_csv(self.input_file)
            elif self.input_file.endswith('.xlsx'):
                df = pd.read_excel(self.input_file)
            else:
                raise ValueError("File không được hỗ trợ")
                
            required_columns = ['email', 'password', 'current_2fa']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Thiếu các cột: {missing_columns}")
                
            self.logger.info(f"Đã load {len(df)} tài khoản")
            return df
            
        except Exception as e:
            self.logger.error(f"Lỗi load file: {e}")
            raise
            
    # Các method khác giữ nguyên như phiên bản cơ bản
    def enter_current_2fa(self, current_2fa):
        """Nhập 2FA hiện tại"""
        try:
            totp_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "totpPin"))
            )
            self.type_like_human(totp_input, current_2fa)
            
            verify_button = self.driver.find_element(By.ID, "totpNext")
            verify_button.click()
            self.random_delay(3, 6)
            
            return True
        except Exception as e:
            self.logger.error(f"Lỗi nhập 2FA: {e}")
            return False
            
    def navigate_to_security_settings(self):
        """Điều hướng đến security settings"""
        try:
            self.driver.get("https://myaccount.google.com/security")
            self.random_delay(3, 5)
            
            two_step_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), '2-Step Verification')]"))
            )
            two_step_link.click()
            self.random_delay(2, 4)
            
            return True
        except Exception as e:
            self.logger.error(f"Lỗi điều hướng: {e}")
            return False
            
    def change_2fa(self):
        """Thay đổi 2FA"""
        try:
            try:
                change_app_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Change app') or contains(text(), 'Get backup codes')]"))
                )
                change_app_button.click()
                self.random_delay(2, 4)
            except TimeoutException:
                self.logger.info("Không tìm thấy nút thay đổi 2FA")
                return None
                
            try:
                password_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "password"))
                )
                self.logger.info("Cần password để xác nhận")
                return "need_password"
            except TimeoutException:
                pass
                
            try:
                backup_codes_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "backup-codes"))
                )
                backup_codes = backup_codes_element.text
                self.logger.info("Đã lấy backup codes mới")
                return backup_codes
            except TimeoutException:
                self.logger.warning("Không tìm thấy backup codes")
                return None
                
        except Exception as e:
            self.logger.error(f"Lỗi thay đổi 2FA: {e}")
            return None

def main():
    """Hàm main"""
    print("=== Gmail 2FA Changer Advanced ===")
    print("⚠️  Phiên bản nâng cao với multi-threading và proxy support")
    print()
    
    # Nhập thông tin
    input_file = input("Nhập đường dẫn file Excel/CSV: ").strip()
    
    if not os.path.exists(input_file):
        print("❌ File không tồn tại!")
        return
        
    output_file = input("Nhập tên file output (mặc định: updated_accounts_advanced.csv): ").strip()
    if not output_file:
        output_file = "updated_accounts_advanced.csv"
        
    # Hỏi về proxy
    use_proxy = input("Sử dụng proxy? (y/N): ").strip().lower() == 'y'
    proxy_list = []
    
    if use_proxy:
        proxy_file = input("Nhập đường dẫn file proxy (mỗi dòng 1 proxy): ").strip()
        if os.path.exists(proxy_file):
            with open(proxy_file, 'r') as f:
                proxy_list = [line.strip() for line in f if line.strip()]
            print(f"Đã load {len(proxy_list)} proxy")
        else:
            print("❌ File proxy không tồn tại!")
            return
            
    # Số worker threads
    max_workers = input("Số worker threads (mặc định: 3): ").strip()
    max_workers = int(max_workers) if max_workers.isdigit() else 3
    
    # Xác nhận
    print(f"\n📁 Input: {input_file}")
    print(f"📁 Output: {output_file}")
    print(f"🔧 Workers: {max_workers}")
    print(f"🌐 Proxy: {'Có' if use_proxy else 'Không'}")
    
    confirm = input("\nBạn có chắc chắn muốn tiếp tục? (y/N): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Đã hủy!")
        return
        
    # Chạy script
    changer = Gmail2FAChangerAdvanced(
        input_file=input_file,
        output_file=output_file,
        use_proxy=use_proxy,
        proxy_list=proxy_list,
        max_workers=max_workers
    )
    
    try:
        changer.run_parallel()
    except KeyboardInterrupt:
        print("\n⚠️  Đã dừng bởi người dùng")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")

if __name__ == "__main__":
    main() 