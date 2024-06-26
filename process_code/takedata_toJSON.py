import scipy.io
import json
import numpy as np

def save_mat_to_json(input_file_path, output_file_path):
    try:
        # Đọc file .mat ban đầu
        mat_contents = scipy.io.loadmat(input_file_path, struct_as_record=False, squeeze_me=True)

        # Truy cập biến con 'x', 'y', 'v' từ file .mat
        x_data = mat_contents['covis'].grid[4].x.tolist()
        y_data = mat_contents['covis'].grid[4].y.tolist()
        v_data = mat_contents['covis'].grid[4].v.tolist()

        # Lưu dữ liệu các biến 'x', 'y', 'v' vào file .json mới
        with open(output_file_path, 'w') as json_file:
            json_file.write(json.dumps({'x': x_data}) + '\n')
            json_file.write(json.dumps({'y': y_data}) + '\n')
            json_file.write(json.dumps({'v': v_data}) + '\n')

        print(f'Dữ liệu từ biến con x, y, v đã được lưu vào file {output_file_path}')
        return True
    except Exception as e:
        print(f'Lỗi khi xử lý file .mat: {str(e)}')
        return False

# Ví dụ sử dụng hàm trong một file khác
if __name__ == "__main__":
    input_file = 'D:\\DATA\\08-01\\COVIS-20230801T003002-diffuse1.mat'  # Thay thế bằng đường dẫn thực tế tới file .mat ban đầu
    output_file = 'D:\\DATA\\DATA2\\final2.json'  # Thay thế bằng đường dẫn và tên file .json mới

    save_mat_to_json(input_file, output_file)
