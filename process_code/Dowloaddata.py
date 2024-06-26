import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Hàm để tải file từ URL
def download_file(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        print(f"Đã tải về: {save_path}")
    else:
        print(f"Lỗi khi tải file từ: {url}")

# Hàm để lấy tất cả link trong trang web
def get_all_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')
    return [urljoin(url, link.get('href')) for link in links]

# URL của trang web chứa các file .mat
base_url = 'http://piweb.ooirsn.uw.edu/covis/processed/latest/2020/'

# Đệ quy để duyệt qua tất cả thư mục và tải file .mat
def find_and_download_mat_files(url, base_save_path):
    links = get_all_links(url)
    for link in links:
        if link.endswith('/'):
            # Nếu link là thư mục, tiếp tục đệ quy và tạo thư mục tương ứng
            folder_name = link.rstrip('/').rsplit('/', 1)[-1]
            save_folder = os.path.join(base_save_path, folder_name)
            os.makedirs(save_folder, exist_ok=True)
            find_and_download_mat_files(link, save_folder)
        elif link.endswith('.mat'):
            # Nếu link là file .mat, tải về và lưu vào thư mục hiện tại
            file_name = os.path.basename(link)
            save_path = os.path.join(base_save_path, file_name)
            download_file(link, save_path)

# Đường dẫn thư mục lưu trữ file .mat trên máy
save_path = './downloaded_files'
os.makedirs(save_path, exist_ok=True)

# Bắt đầu quá trình tải file
find_and_download_mat_files(base_url, save_path)
