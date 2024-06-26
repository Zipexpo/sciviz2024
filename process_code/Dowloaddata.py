import requests
import os
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Địa chỉ URL của thư mục chứa các file và thư mục con
base_url = "http://piweb.ooirsn.uw.edu/covis/processed/latest/2023/08/"

# Tạo một thư mục để lưu các file tải về (nếu thư mục chưa tồn tại)
save_dir = 'D:/DATA'
os.makedirs(save_dir, exist_ok=True)

# Gửi yêu cầu GET đến URL và lấy nội dung HTML
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')

# Lặp qua các thẻ <a> trong nội dung HTML để lấy các đường dẫn đến các thư mục con
for link in soup.find_all('a'):
    href = link.get('href')
    
    # Kiểm tra nếu đường dẫn là đến thư mục con và không phải là thư mục cha
    if href and href.endswith('/') and not href.startswith('../'):
        subdir_url = urljoin(base_url, href)
        
        # Gửi yêu cầu GET đến thư mục con và lấy nội dung HTML
        subdir_response = requests.get(subdir_url)
        subdir_soup = BeautifulSoup(subdir_response.content, 'html.parser')
        
        # Lặp qua các thẻ <a> trong nội dung HTML của thư mục con để lấy các đường dẫn đến các thư mục con tiếp theo
        for subdir_link in subdir_soup.find_all('a'):
            subdir_href = subdir_link.get('href')
            
            # Kiểm tra nếu đường dẫn là đến thư mục con tiếp theo và không phải là thư mục cha
            if subdir_href and subdir_href.endswith('/') and not subdir_href.startswith('../'):
                subsubdir_url = urljoin(subdir_url, subdir_href)
                
                # Gửi yêu cầu GET đến thư mục con tiếp theo và lấy nội dung HTML
                subsubdir_response = requests.get(subsubdir_url)
                subsubdir_soup = BeautifulSoup(subsubdir_response.content, 'html.parser')
                
                # Lặp qua các thẻ <a> trong nội dung HTML của thư mục con tiếp theo để lấy các đường dẫn đến các file .mat
                for file_link in subsubdir_soup.find_all('a'):
                    file_href = file_link.get('href')
                    
                    # Kiểm tra nếu đường dẫn là tới file .mat
                    if file_href and file_href.endswith('.mat'):
                        file_url = urljoin(subsubdir_url, file_href)
                        
                        # Tên file là phần cuối cùng của đường dẫn sau dấu '/'
                        filename = os.path.join(save_dir, file_href.split('/')[-1])
                        
                        # Tải file về và lưu vào thư mục đã chỉ định
                        print(f"Downloading {filename}...")
                        try:
                            file_response = requests.get(file_url)
                            with open(filename, 'wb') as f:
                                f.write(file_response.content)
                            print(f"Downloaded {filename}")
                        except Exception as e:
                            print(f"Failed to download {filename}: {str(e)}")
