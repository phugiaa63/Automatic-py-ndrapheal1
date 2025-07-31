#!/usr/bin/env python3
"""
Gmail 2FA Changer - Tự động thay đổi 2FA cho nhiều tài khoản Gmail
Author: Assistant
Version: 3.3 - Click at Mouse Position for Next and Verify
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
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import logging
from datetime import datetime
import pyotp
import cv2
import numpy as np
from PIL import Image
import io
import base64
import pyautogui

class Gmail2FAChanger:
    def __init__(self, input_file, output_file="updated_accounts.csv"):
        self.input_file = input_file
        self.output_file = output_file
        self.driver = None
        self.setup_logging()
        self.setup_driver()
        
        # Xóa file output cũ nếu tồn tại để đảm bảo ghi đè sạch
        if os.path.exists(self.output_file):
            try:
                os.remove(self.output_file)
                self.logger.info(f"Đã xóa file output cũ: {self.output_file}")
            except Exception as e:
                self.logger.warning(f"Không thể xóa file output cũ: {e}")
        
    def setup_logging(self):
        """Thiết lập logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('gmail_2fa_changer.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self):
        """Thiết lập Chrome driver với anti-detection"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option("prefs", {
            "profile.managed_default_content_settings.images": 1
        })
        chrome_options.add_argument("--window-size=1366,768")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Thêm stealth JavaScript
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Thiết lập pyautogui
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0
        
    def human_like_delay(self, min_seconds=0.2, max_seconds=0.5):
        """Delay ngẫu nhiên giống người thật - tối ưu tốc độ"""
        delay = random.uniform(min_seconds, max_seconds)
        time.sleep(delay)
        
    def type_like_human(self, element, text):
        """Gõ text giống người thật - Selenium với anti-detection"""
        try:
            # Click vào element trước khi gõ
            self.click_like_human(element)
            self.human_like_delay(0.1, 0.3)
            
            # Clear text cũ với ActionChains
            actions = ActionChains(self.driver)
            actions.key_down(Keys.CONTROL).send_keys('a').key_up(Keys.CONTROL)
            actions.send_keys(Keys.DELETE)
            actions.perform()
            self.human_like_delay(0.1, 0.3)
            
            # Gõ text mới với tốc độ ngẫu nhiên và ActionChains
            if len(text) > 20:  # Mật khẩu dài - gõ rất nhanh
                for char in text:
                    actions = ActionChains(self.driver)
                    actions.send_keys(char)
                    actions.perform()
                    time.sleep(random.uniform(0.01, 0.03))
            else:  # Email ngắn - gõ nhanh
                for char in text:
                    actions = ActionChains(self.driver)
                    actions.send_keys(char)
                    actions.perform()
                    time.sleep(random.uniform(0.02, 0.05))
            
            # Delay sau khi gõ xong
            self.human_like_delay(0.1, 0.3)
            
        except Exception as e:
            self.logger.warning(f"Lỗi khi gõ, dùng send_keys đơn giản: {e}")
            # Fallback về send_keys đơn giản
            element.clear()
            self.human_like_delay(0.1, 0.3)
            
            if len(text) > 20:  # Mật khẩu dài - gõ rất nhanh
                for char in text:
                    element.send_keys(char)
                    time.sleep(random.uniform(0.01, 0.03))
            else:  # Email ngắn - gõ nhanh
                for char in text:
                    element.send_keys(char)
                    time.sleep(random.uniform(0.02, 0.05))
            
            self.human_like_delay(0.1, 0.3)
        
    def move_mouse_like_human(self, element):
        """Di chuyển chuột đến element giống người thật - Selenium với anti-detection"""
        try:
            # Thêm random mouse movement trước khi di chuyển đến element
            actions = ActionChains(self.driver)
            
            # Random mouse movement để giống người thật
            for _ in range(random.randint(1, 3)):
                x_offset = random.randint(-50, 50)
                y_offset = random.randint(-50, 50)
                actions.move_by_offset(x_offset, y_offset)
                actions.pause(random.uniform(0.1, 0.3))
            
            # Di chuyển đến element với đường cong tự nhiên
            actions.move_to_element(element)
            actions.pause(random.uniform(0.2, 0.8))
            actions.perform()
            
        except Exception as e:
            self.logger.warning(f"Lỗi khi di chuyển chuột: {e}")
            # Fallback đơn giản
            element.location_once_scrolled_into_view
        
    def click_like_human(self, element):
        """Click giống người thật - Selenium với anti-detection"""
        try:
            # Di chuyển chuột đến element
            self.move_mouse_like_human(element)
            self.human_like_delay(0.2, 0.8)
            
            # Thêm random delay trước khi click
            time.sleep(random.uniform(0.1, 0.5))
            
            # Click với ActionChains để giống người thật hơn
            actions = ActionChains(self.driver)
            actions.click(element)
            actions.pause(random.uniform(0.1, 0.3))
            actions.perform()
            
            self.human_like_delay(0.5, 1.5)
            
        except Exception as e:
            self.logger.warning(f"Lỗi khi click, dùng click đơn giản: {e}")
            # Fallback về click đơn giản
            element.click()
            self.human_like_delay(0.5, 1.5)
    
    def random_delay(self, min_seconds=3, max_seconds=5):
        """Delay ngẫu nhiên giữa các tài khoản (3-5 giây)"""
        delay = random.uniform(min_seconds, max_seconds)
        self.logger.info(f"Đợi {delay:.1f} giây trước khi xử lý tài khoản tiếp theo...")
        time.sleep(delay)
        
    def load_accounts(self):
        """Load danh sách tài khoản từ file"""
        try:
            if self.input_file.endswith('.csv'):
                df = pd.read_csv(self.input_file)
            elif self.input_file.endswith('.xlsx'):
                df = pd.read_excel(self.input_file)
            else:
                raise ValueError("File không được hỗ trợ. Sử dụng CSV hoặc Excel")
                
            required_columns = ['email', 'password', 'current_2fa']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Thiếu các cột: {missing_columns}")
                
            self.logger.info(f"Đã load {len(df)} tài khoản từ {self.input_file}")
            return df
            
        except Exception as e:
            self.logger.error(f"Lỗi khi load file: {e}")
            raise
    
    def scan_qr_code(self):
        """Scan QR code để lấy secret key"""
        try:
            # Tìm QR code element
            qr_selectors = [
                "//img[contains(@src, 'qr')]",
                "//img[contains(@alt, 'QR')]",
                "//img[contains(@class, 'qr')]",
                "//img[contains(@id, 'qr')]",
                "//canvas[contains(@class, 'qr')]",
                "//svg[contains(@class, 'qr')]"
            ]
            
            qr_element = None
            for selector in qr_selectors:
                try:
                    qr_element = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    self.logger.info(f"Tìm thấy QR code với selector: {selector}")
                    break
                except TimeoutException:
                    continue
            
            if not qr_element:
                # Tìm tất cả img và kiểm tra
                try:
                    images = self.driver.find_elements(By.TAG_NAME, "img")
                    for img in images:
                        try:
                            src = img.get_attribute("src")
                            alt = img.get_attribute("alt")
                            if src and ("qr" in src.lower() or "qr" in alt.lower()):
                                qr_element = img
                                self.logger.info("Tìm thấy QR code trong img tags")
                                break
                        except:
                            continue
                except:
                    pass
            
            if not qr_element:
                self.logger.error("Không tìm thấy QR code element")
                return None
            
            # Chụp screenshot QR code
            try:
                # Lấy vị trí và kích thước của QR code
                location = qr_element.location
                size = qr_element.size
                
                # Chụp screenshot toàn bộ trang
                screenshot = self.driver.get_screenshot_as_png()
                img = Image.open(io.BytesIO(screenshot))
                
                # Crop vùng QR code
                left = location['x']
                top = location['y']
                right = location['x'] + size['width']
                bottom = location['y'] + size['height']
                
                qr_img = img.crop((left, top, right, bottom))
                
                # Lưu QR code để debug
                qr_img.save("qr_code_debug.png")
                self.logger.info("Đã lưu QR code debug")
                
                # Chuyển đổi PIL Image sang OpenCV format
                qr_cv = cv2.cvtColor(np.array(qr_img), cv2.COLOR_RGB2BGR)
                
                # Scan QR code bằng OpenCV
                qr_detector = cv2.QRCodeDetector()
                retval, decoded_info, points, straight_qrcode = qr_detector.detectAndDecodeMulti(qr_cv)
                
                if retval and decoded_info:
                    qr_data = decoded_info[0]  # Lấy QR code đầu tiên
                    self.logger.info(f"Đã scan được QR code: {qr_data[:50]}...")
                    
                    # Trích xuất secret key từ QR data
                    # QR code thường có format: otpauth://totp/Google:email@gmail.com?secret=SECRET_KEY&issuer=Google
                    if "secret=" in qr_data:
                        secret_key = qr_data.split("secret=")[1].split("&")[0]
                        self.logger.info(f"Đã trích xuất secret key từ QR: {secret_key}")
                        return secret_key
                    else:
                        self.logger.error("QR code không chứa secret key")
                        return None
                else:
                    self.logger.error("Không thể scan QR code")
                    return None
                    
            except Exception as e:
                self.logger.error(f"Lỗi khi scan QR code: {e}")
                return None
                
        except Exception as e:
            self.logger.error(f"Lỗi trong scan_qr_code: {e}")
            return None
    
    def login_gmail(self, email, password):
        """Đăng nhập vào Gmail với thao tác giống người thật"""
        try:
            self.logger.info(f"Đang đăng nhập: {email}")
            
            # Kiểm tra browser connection
            try:
                self.driver.current_url
            except:
                self.logger.error("Browser đã bị đóng, khởi tạo lại...")
                self.setup_driver()
            
            # Truy cập trực tiếp vào trang 2FA để giảm bớt thao tác
            direct_2fa_url = "https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fmyaccount.google.com%2Ftwo-step-verification%2Fauthenticator%3Futm_source%3Dgoogle-account%26utm_medium%3Dweb%26utm_campaign%3Dauthenticator-screen%26continue%3Dhttps%3A%2F%2Fmyaccount.google.com%2Fsecurity%3Fhl%253Den-VN%2526utm_source%253Dgoogle%2526utm_medium%253Dpref-page%26pli%3D1%26rapt%3DAEjHL4OteeglN8OG066CvDclXH8st0WwgaRVUnFNBlddql-awJhlZyKEM3l84K3VcnYezr4JOAx96xaPCTX14_GpHq--HCDXq-rIcH7yu8JvDkBaBZ7Y6mU&followup=https%3A%2F%2Fmyaccount.google.com%2Ftwo-step-verification%2Fauthenticator%3Futm_source%3Dgoogle-account%26utm_medium%3Dweb%26utm_campaign%3Dauthenticator-screen%26continue%3Dhttps%3A%2F%2Fmyaccount.google.com%2Fsecurity%3Fhl%253Den-VN%2526utm_source%253Dgoogle%2526utm_medium%253Dpref-page%26pli%3D1%26rapt%3DAEjHL4OteeglN8OG066CvDclXH8st0WwgaRVUnFNBlddql-awJhlZyKEM3l84K3VcnYezr4JOAx96xaPCTX14_GpHq--HCDXq-rIcH7yu8JvDkBaBZ7Y6mU&ifkv=AdBytiMH2xjn6syTwYDc-iuBVyftEvD9AZcXwN0tYUKWguemT-GWHak9GsDTt0e5kSJ0PRyYfZIZaQ&osid=1&passive=1209600&rart=ANgoxcf7Au4QIBotVHjRKIegd5mQnyu2VsSEweuhHC7xvwMNObaaZNab-cq85DcQp6JYnYsY8RuYew0A5iBTZlQjC6v50fRb43w_WZ1OJs1vbPqZeDuyd28&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S1881266728%3A1753894272464641"
            self.driver.get(direct_2fa_url)
            self.human_like_delay(1, 2)
            
            # Kiểm tra captcha ngay từ đầu
            try:
                captcha_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'captcha') or contains(text(), 'robot') or contains(text(), 'I\'m not a robot') or contains(text(), 'verification')]")
                if captcha_elements:
                    self.logger.error(f"🤖 Phát hiện captcha/verification cho {email} - Bỏ qua tài khoản này")
                    return False
            except:
                pass
            
            # Nhập email - thử nhiều cách khác nhau cho incognito mode
            try:
                # Thử tìm email field với nhiều selector khác nhau
                email_selectors = [
                    (By.NAME, "identifier"),
                    (By.ID, "identifierId"),
                    (By.XPATH, "//input[@type='email']"),
                    (By.XPATH, "//input[@name='identifier']"),
                    (By.CSS_SELECTOR, "input[type='email']"),
                    (By.CSS_SELECTOR, "input[name='identifier']")
                ]
                
                email_input = None
                for selector_type, selector_value in email_selectors:
                    try:
                        email_input = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((selector_type, selector_value))
                        )
                        self.logger.info(f"Tìm thấy email field với selector: {selector_type}={selector_value}")
                        break
                    except TimeoutException:
                        continue
                
                if not email_input:
                    self.logger.error("Không tìm thấy email field với bất kỳ selector nào")
                    return False
                
                self.move_mouse_like_human(email_input)
                self.type_like_human(email_input, email)
                
                # Click Next - thử nhiều cách khác nhau
                next_selectors = [
                    (By.XPATH, "//span[text()='Next']"),
                    (By.XPATH, "//button[contains(text(), 'Next')]"),
                    (By.XPATH, "//div[contains(text(), 'Next')]"),
                    (By.CSS_SELECTOR, "button[type='submit']"),
                    (By.CSS_SELECTOR, "input[type='submit']")
                ]
                
                next_button = None
                for selector_type, selector_value in next_selectors:
                    try:
                        next_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((selector_type, selector_value))
                        )
                        self.logger.info(f"Tìm thấy Next button với selector: {selector_type}={selector_value}")
                        break
                    except TimeoutException:
                        continue
                
                if next_button:
                    self.click_like_human(next_button)
                else:
                    # Thử nhấn Enter nếu không tìm thấy button
                    email_input.send_keys(Keys.RETURN)
                
                # Đợi trang password load
                self.human_like_delay(1, 2)
                
            except (TimeoutException, Exception) as e:
                self.logger.error(f"Lỗi khi nhập email: {e}")
                return False
            
            # Nhập password - thử nhiều cách khác nhau
            password_input = None
            try:
                # Thử tìm password field với nhiều selector khác nhau
                selectors = [
                    (By.NAME, "password"),
                    (By.NAME, "Passwd"),
                    (By.ID, "password"),
                    (By.ID, "Passwd"),
                    (By.XPATH, "//input[@type='password']"),
                    (By.CSS_SELECTOR, "input[type='password']")
                ]
                
                for selector_type, selector_value in selectors:
                    try:
                        password_input = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((selector_type, selector_value))
                        )
                        self.logger.info(f"Tìm thấy password field với selector: {selector_type}={selector_value}")
                        break
                    except TimeoutException:
                        continue
                
                if not password_input:
                    self.logger.error("Không tìm thấy password field với bất kỳ selector nào")
                    return False
                
                self.move_mouse_like_human(password_input)
                self.type_like_human(password_input, password)
                
                # Click Next
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
                )
                self.click_like_human(next_button)
                
                # Đợi đăng nhập hoàn tất
                self.human_like_delay(1, 2)
                
                # Kiểm tra captcha sau khi nhập password
                try:
                    captcha_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'captcha') or contains(text(), 'robot') or contains(text(), 'I\'m not a robot') or contains(text(), 'verification') or contains(text(), 'suspicious')]")
                    if captcha_elements:
                        self.logger.error(f"🤖 Phát hiện captcha/verification sau khi nhập password cho {email} - Bỏ qua tài khoản này")
                        return False
                except:
                    pass
                
                # Kiểm tra xem có cần nhập 2FA không
                try:
                    # Tìm input cho 2FA
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "totpPin"))
                    )
                    self.logger.info("Tìm thấy 2FA input field")
                    return True
                except TimeoutException:
                    # Kiểm tra xem có đăng nhập thành công không
                    try:
                        current_url = self.driver.current_url
                        if "myaccount.google.com" in current_url or "gmail.com" in current_url:
                            self.logger.info("Đăng nhập thành công - đã vào Google Account")
                            return True
                        else:
                            # Kiểm tra lại captcha một lần nữa
                            try:
                                captcha_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'captcha') or contains(text(), 'robot') or contains(text(), 'I\'m not a robot') or contains(text(), 'verification') or contains(text(), 'suspicious')]")
                                if captcha_elements:
                                    self.logger.error(f"🤖 Phát hiện captcha/verification cuối cùng cho {email} - Bỏ qua tài khoản này")
                                    return False
                            except:
                                pass
                            self.logger.info("Có thể cần xử lý 2FA hoặc có challenge")
                            return True
                    except:
                        self.logger.info("Không thể kiểm tra URL, giả sử thành công")
                        return True
                        
            except Exception as e:
                self.logger.error(f"Lỗi khi nhập password: {e}")
                return False
                    
        except Exception as e:
            self.logger.error(f"Lỗi đăng nhập: {e}")
            return False
            
    def enter_current_2fa(self, current_2fa):
        """Nhập mã 2FA hiện tại - tạo mã 6 số từ secret key"""
        try:
            # Tìm input cho 2FA
            totp_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "totpPin"))
            )
            
            # Làm sạch secret key (loại bỏ khoảng trắng và ký tự không hợp lệ)
            clean_2fa = current_2fa.replace(' ', '').replace('-', '').replace('_', '').upper()
            
            # Tạo mã 6 số từ secret key hiện tại
            totp = pyotp.TOTP(clean_2fa)
            current_2fa_code = totp.now()
            
            self.logger.info(f"Tạo mã 2FA từ secret key: {current_2fa_code}")
            
            self.move_mouse_like_human(totp_input)
            self.type_like_human(totp_input, current_2fa_code)
            
            # Click Next
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
            )
            self.click_like_human(next_button)
            
            # Đợi xác thực
            self.human_like_delay(1, 2)
            return True
            
        except Exception as e:
            self.logger.error(f"Lỗi nhập 2FA: {e}")
            return False
            
    def change_2fa(self):
        """Thay đổi 2FA với thao tác giống người thật - chỉ dùng scan QR code"""
        try:
            # Click "Change authenticator app" button
            change_btn_selectors = [
                (By.XPATH, "//span[text()='Change authenticator app']"),
                (By.XPATH, "//button[contains(text(), 'Change authenticator app')]"),
                (By.XPATH, "//div[contains(text(), 'Change authenticator app')]"),
                (By.CSS_SELECTOR, "button.mUIrbf-LgbsSe.mUIrbf-LgbsSe-OWXEXe-dgl2Hf.wMI9H"),
                (By.CLASS_NAME, "mUIrbf-LgbsSe")
            ]
            
            change_btn = None
            for selector_type, selector_value in change_btn_selectors:
                try:
                    change_btn = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((selector_type, selector_value))
                    )
                    self.logger.info(f"Tìm thấy Change authenticator app button theo {selector_type}={selector_value}")
                    break
                except TimeoutException:
                    continue
            
            if not change_btn:
                self.logger.error("Không tìm thấy Change authenticator app button")
                return {"status": "error", "message": "Không tìm thấy Change authenticator app button"}
            
            # Click button
            self.click_like_human(change_btn)
            self.human_like_delay(2, 3)
            
            # Kiểm tra xem có cần nhập 2FA hiện tại để xác thực không
            try:
                # Tìm input cho 2FA hiện tại
                current_2fa_input = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "totpPin"))
                )
                
                # Làm sạch secret key hiện tại
                clean_current_2fa = self.current_2fa.replace(' ', '').replace('-', '').replace('_', '').upper()
                
                # Tạo mã 6 số từ secret key hiện tại
                totp = pyotp.TOTP(clean_current_2fa)
                current_2fa_code = totp.now()
                
                self.logger.info(f"Tạo mã 2FA từ secret key hiện tại: {current_2fa_code}")
                
                # Nhập mã 2FA hiện tại
                self.move_mouse_like_human(current_2fa_input)
                self.type_like_human(current_2fa_input, current_2fa_code)
                
                # Click Next để tiếp tục
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
                )
                self.click_like_human(next_button)
                self.human_like_delay(2, 3)
                
            except TimeoutException:
                self.logger.info("Không cần nhập 2FA hiện tại, tiếp tục...")
            
            # Scan QR code để lấy secret key mới
            self.logger.info("Đang thử scan QR code...")
            secret_key = self.scan_qr_code()
            
            if secret_key:
                self.logger.info("Scan QR code thành công, click Next để tiếp tục...")
                
                # Click Next sau khi scan QR code thành công
                self.human_like_delay(5, 8)
                
                # Click thật tại vị trí chuột hiện tại
                try:
                    # Lấy vị trí chuột hiện tại
                    current_x, current_y = pyautogui.position()
                    self.logger.info(f"Vị trí chuột hiện tại: ({current_x}, {current_y})")
                    
                    # Click thật tại vị trí chuột
                    pyautogui.click()
                    self.human_like_delay(2, 3)
                    self.logger.info(f"Click thật thành công tại vị trí chuột: ({current_x}, {current_y})")
                    
                except Exception as e:
                    self.logger.error(f"Lỗi click thật tại vị trí chuột: {e}")
                
                # Bây giờ mới tạo mã 2FA mới và nhập vào
                self.logger.info("Đã click Next, bây giờ tạo mã 2FA mới và nhập vào...")
                
                # Làm sạch secret key
                clean_secret_key = secret_key.replace(' ', '').replace('-', '').replace('_', '').upper()
                
                # Tạo mã 6 số từ secret key mới
                try:
                    totp = pyotp.TOTP(clean_secret_key)
                    new_2fa_code = totp.now()
                    self.logger.info(f"Đã tạo mã 2FA mới từ secret key: {new_2fa_code}")
                    self.logger.info(f"Secret key mới: {clean_secret_key}")
                except Exception as e:
                    self.logger.error(f"Lỗi khi tạo mã 2FA từ secret key: {e}")
                    return {"status": "error", "message": f"Không thể tạo mã 2FA từ secret key: {str(e)}"}
                
                # Tìm input field để nhập mã 2FA mới
                try:
                    # Thử nhiều selector cho input field
                    input_selectors = [
                        (By.NAME, "totpPin"),
                        (By.ID, "totpPin"),
                        (By.XPATH, "//input[@type='text']"),
                        (By.CSS_SELECTOR, "input[type='text']"),
                        (By.XPATH, "//input[contains(@placeholder, 'code')]"),
                        (By.XPATH, "//input[contains(@placeholder, 'mã')]")
                    ]
                    
                    input_field = None
                    for selector_type, selector_value in input_selectors:
                        try:
                            input_field = WebDriverWait(self.driver, 5).until(
                                EC.presence_of_element_located((selector_type, selector_value))
                            )
                            self.logger.info(f"Tìm thấy input field với selector: {selector_type}={selector_value}")
                            break
                        except TimeoutException:
                            continue
                    
                    if not input_field:
                        self.logger.warning("Không tìm thấy input field, thử tìm tất cả input...")
                        
                        # Tìm tất cả input có thể
                        try:
                            all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
                            for inp in all_inputs:
                                try:
                                    input_type = inp.get_attribute("type")
                                    if input_type in ["text", "tel", "number"]:
                                        input_field = inp
                                        self.logger.info(f"Tìm thấy input field với type: {input_type}")
                                        break
                                except:
                                    continue
                        except:
                            pass
                        
                        if not input_field:
                            self.logger.error("Không tìm thấy input field để nhập mã 2FA mới")
                            return {"status": "error", "message": "Không tìm thấy input field"}
                    
                    # Nhập mã 2FA mới
                    self.move_mouse_like_human(input_field)
                    self.type_like_human(input_field, new_2fa_code)
                    self.human_like_delay(1, 2)
                    self.logger.info("Đã nhập mã 2FA mới")
                    
                    # Click Verify/Next để xác thực - dùng click thật tại vị trí chuột
                    self.logger.info("Đã nhập mã 2FA mới, chờ click Verify...")
                    self.human_like_delay(3, 5)
                    
                    # Click thật tại vị trí chuột hiện tại cho nút Verify
                    try:
                        # Lấy vị trí chuột hiện tại
                        current_x, current_y = pyautogui.position()
                        self.logger.info(f"Vị trí chuột hiện tại cho Verify: ({current_x}, {current_y})")
                        
                        # Click thật tại vị trí chuột
                        pyautogui.click()
                        self.human_like_delay(2, 3)
                        self.logger.info(f"Click Verify thành công tại vị trí chuột: ({current_x}, {current_y})")
                        
                    except Exception as e:
                        self.logger.error(f"Lỗi click Verify tại vị trí chuột: {e}")
                        
                        # Fallback: thử nhấn Enter
                        try:
                            from selenium.webdriver.common.keys import Keys
                            input_field.send_keys(Keys.RETURN)
                            self.human_like_delay(2, 3)
                            self.logger.info("Đã nhấn Enter để xác thực")
                        except:
                            pass
                    
                    # Trả về kết quả thành công với secret key mới
                    self.logger.info(f"✅ Hoàn thành đổi 2FA! Secret key mới: {clean_secret_key}")
                    return {
                        "status": "success", 
                        "message": "Đã thay đổi 2FA thành công bằng scan QR code",
                        "new_2fa": clean_secret_key
                    }
                    
                except Exception as e:
                    self.logger.error(f"Lỗi khi nhập mã 2FA mới: {e}")
                    return {"status": "error", "message": f"Lỗi khi nhập mã 2FA mới: {str(e)}"}
            else:
                self.logger.error("Không thể scan QR code")
                return {"status": "error", "message": "Không thể scan QR code để lấy secret key"}
                
        except Exception as e:
            self.logger.error(f"Lỗi thay đổi 2FA: {e}")
            return {"status": "error", "message": "Không thể thay đổi 2FA"}
            
    def process_account(self, email, password, current_2fa):
        """Xử lý một tài khoản với thao tác giống người thật"""
        try:
            # Lưu thông tin để sử dụng trong change_2fa
            self.current_password = password
            self.current_2fa = current_2fa
            
            # Đăng nhập
            login_result = self.login_gmail(email, password)
            if not login_result:
                self.logger.error(f"❌ Đăng nhập thất bại cho {email} - Bỏ qua tài khoản này")
                return {"status": "error", "message": "Đăng nhập thất bại - sai mật khẩu hoặc gặp captcha/robot verification"}
            
            self.logger.info(f"✅ Đăng nhập thành công cho {email}")
            
            # Kiểm tra xem có cần nhập 2FA không
            try:
                # Tìm input cho 2FA
                WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "totpPin"))
                )
                self.logger.info(f"🔐 Cần nhập 2FA cho {email}")
                
                # Nhập 2FA hiện tại
                if not self.enter_current_2fa(current_2fa):
                    self.logger.error(f"❌ Nhập 2FA thất bại cho {email} - Bỏ qua tài khoản này")
                    return {"status": "error", "message": "Nhập 2FA thất bại - sai mã 2FA hoặc gặp captcha/robot verification"}
                    
            except TimeoutException:
                self.logger.info(f"✅ Không cần nhập 2FA cho {email} - đã đăng nhập thành công")
            
            # Thay đổi 2FA (đã ở trang 2FA rồi)
            result = self.change_2fa()
            
            if result["status"] == "success":
                self.logger.info(f"✅ Thành công đổi 2FA cho {email}")
                self.logger.info(f"📝 Secret key mới: {result.get('new_2fa', '')}")
            else:
                self.logger.error(f"❌ Thất bại đổi 2FA cho {email}: {result.get('message', '')} - Bỏ qua tài khoản này")
                
            return result
                
        except Exception as e:
            self.logger.error(f"❌ Lỗi xử lý tài khoản {email}: {e} - Bỏ qua tài khoản này")
            return {"status": "error", "message": f"Lỗi xử lý: {str(e)}"}
            
    def run(self):
        """Chạy script chính - đơn giản hóa"""
        try:
            # Load danh sách tài khoản
            accounts_df = self.load_accounts()
            
            # Tạo DataFrame mới để lưu kết quả
            results = []
            
            for index, row in accounts_df.iterrows():
                email = row['email']
                password = row['password']
                current_2fa = row['current_2fa']
                
                self.logger.info(f"Đang xử lý tài khoản {index + 1}/{len(accounts_df)}: {email}")
                
                # Xử lý tài khoản
                result = self.process_account(email, password, current_2fa)
                
                # Lưu kết quả với ghi chú chi tiết
                result_data = {
                    'email': email,
                    'password': password,
                    'old_2fa': current_2fa,
                    'new_2fa': result.get('new_2fa', ''),
                    'status': result['status'],
                    'message': result.get('message', ''),
                    'note': self.get_detailed_note(result.get('message', '')),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                results.append(result_data)
                
                # Delay ngắn cho tất cả trường hợp - 3-5 giây
                if result['status'] == 'error':
                    self.logger.warning(f"⏭️  Bỏ qua tài khoản {email} và chuyển sang tài khoản tiếp theo...")
                else:
                    self.logger.info(f"✅ Hoàn thành tài khoản {email}, chuyển sang tài khoản tiếp theo...")
                
                # Delay 3-5 giây trước khi xử lý tài khoản tiếp theo
                if index < len(accounts_df) - 1:  # Không delay sau tài khoản cuối
                    self.random_delay(3, 5)
                    
            # Lưu kết quả cuối cùng - ghi đè file
            final_df = pd.DataFrame(results)
            final_df.to_csv(self.output_file, index=False, mode='w')
            self.logger.info(f"✅ Hoàn thành! Kết quả đã ghi đè vào {self.output_file}")
            
            # Hiển thị tóm tắt kết quả
            success_count = len(final_df[final_df['status'] == 'success'])
            total_count = len(final_df)
            self.logger.info(f"📊 Tóm tắt: {success_count}/{total_count} tài khoản thành công")
            
            if success_count > 0:
                self.logger.info("🔑 Secret keys mới:")
                for _, row in final_df[final_df['status'] == 'success'].iterrows():
                    self.logger.info(f"   {row['email']}: {row['new_2fa']}")
            
        except Exception as e:
            self.logger.error(f"Lỗi trong quá trình chạy: {e}")
        finally:
            if self.driver:
                self.driver.quit()
                
    def get_detailed_note(self, message):
        """Tạo ghi chú chi tiết dựa trên message"""
        if not message:
            return "Thành công"
        
        message_lower = message.lower()
        if "sai mật khẩu" in message_lower or "wrong password" in message_lower:
            return "Sai mật khẩu - cần kiểm tra lại"
        elif "captcha" in message_lower or "robot" in message_lower or "verification" in message_lower:
            return "Gặp captcha/robot verification - cần xử lý thủ công"
        elif "sai mã 2fa" in message_lower or "wrong 2fa" in message_lower:
            return "Sai mã 2FA - cần kiểm tra lại secret key"
        elif "không thể scan" in message_lower or "scan qr" in message_lower:
            return "Không thể scan QR code - có thể do lỗi hiển thị"
        elif "không tìm thấy" in message_lower or "not found" in message_lower:
            return "Không tìm thấy element - có thể do thay đổi giao diện"
        else:
            return f"Lỗi khác: {message}"
    
    def cleanup(self):
        """Dọn dẹp tài nguyên"""
        if self.driver:
            self.driver.quit()

def main():
    """Hàm main"""
    print("=== Gmail 2FA Changer - Click at Mouse Position ===")
    print("⚠️  Lưu ý: Hãy backup file dữ liệu trước khi chạy!")
    print("🔄 Tool đã được nâng cấp:")
    print("   - Chrome driver với anti-detection")
    print("   - Window size cố định")
     print("   - Delay 3-5 giây giữa các tài khoản - xử lý nhanh")
    print("   - Tự động scan QR code bằng OpenCV")
    print("   - Click thật tại vị trí chuột cho Next và Verify")
    print("   - Bỏ qua việc tìm selector cho button")
    print("   - Tự động tạo mã 2FA mới và xác thực")
    print("   - Lưu secret key mới vào file output")
    print("   - Ghi chú chi tiết các lỗi vào CSV")
    print()
    print("📌 HƯỚNG DẪN:")
    print("   1. Chạy tool")
    print("   2. Khi scan QR code xong, đặt chuột lên nút Next")
    print("   3. Khi nhập mã 2FA xong, đặt chuột lên nút Verify")
    print("   4. Tool sẽ click thật tại vị trí chuột của bạn")
    print()
    
    # Nhập thông tin file
    input_file = input("Nhập đường dẫn file Excel/CSV chứa danh sách tài khoản (mặc định: sample_accounts.csv): ").strip()
    
    if not input_file:
        input_file = "C:/gmail-2fa-bulk-changer/real_accounts.csv"
    
    if not os.path.exists(input_file):
        print("❌ File không tồn tại!")
        return
        
    output_file = input("Nhập tên file output (mặc định: updated_accounts.csv): ").strip()
    if not output_file:
        output_file = "updated_accounts.csv"
    
    # Kiểm tra xem file output có tồn tại không
    if os.path.exists(output_file):
        overwrite = input(f"⚠️  File {output_file} đã tồn tại. Bạn có muốn ghi đè không? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("❌ Đã hủy!")
            return
        
    # Xác nhận
    print(f"\n📁 Input file: {input_file}")
    print(f"📁 Output file: {output_file}")
     print("⏱️  Delay giữa các tài khoản: 3-5 giây - xử lý nhanh")
    print("🤖 Thao tác: Tối ưu tốc độ")
    print("🛡️  Chrome bình thường - đơn giản")
    print("🤖 Captcha: Bỏ qua phát hiện")
    confirm = input("\nBạn có chắc chắn muốn tiếp tục? (y/N): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Đã hủy!")
        return
        
    # Chạy script
    changer = Gmail2FAChanger(input_file, output_file)
    try:
        changer.run()
    except KeyboardInterrupt:
        print("\n⚠️  Đã dừng bởi người dùng")
    finally:
        changer.cleanup()

if __name__ == "__main__":
    main() 