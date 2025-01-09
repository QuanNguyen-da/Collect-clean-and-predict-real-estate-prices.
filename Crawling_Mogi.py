import requests
import pandas as pd
from bs4 import BeautifulSoup

data = []

for page in range(1, 683):
    url = f'https://mogi.vn/mua-nha-dat?cp={page}'
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f'Truy cập trang thứ {page} thành công')
        soup = BeautifulSoup(response.text, 'html.parser')
        houses = soup.find_all('div', class_='prop-info')
        dates = soup.find_all('div', class_='prop-extra')

        for house in houses:
            link = house.find('a', class_="link-overlay")['href']
            title = house.find('h2', class_="prop-title").text.strip()
            addr = house.find('div', class_="prop-addr").text.strip()
            price = house.find('div', class_="price").text.strip()
            attributes = [li.text.strip() for li in house.find('ul', class_='prop-attr').find_all('li')] if house.find('ul', class_='prop-attr') else ["N/A", "N/A"]
            dientich = attributes[0].strip()
            bedroom = attributes[1].strip()
            bathroom = attributes[2].strip()

            # Kiểm tra ngày và gắn nó vào cùng dòng dữ liệu
            day = None  # Nếu không có ngày thì để None
            for date in dates:
                day = date.find('div', class_="prop-created").text.strip() if date else None

            # Thêm tất cả dữ liệu vào trong một dòng
            data.append([link, title, addr, dientich, bedroom, bathroom, price, day])

    else:
        # Mã trạng thái và ý nghĩa nếu không thành công
        status_code_meanings = {
            400: "Bad Request: Yêu cầu không hợp lệ.",
            401: "Unauthorized: Cần xác thực.",
            403: "Forbidden: Truy cập bị từ chối.",
            404: "Not Found: Trang không tìm thấy.",
            500: "Internal Server Error: Lỗi máy chủ.",
            503: "Service Unavailable: Dịch vụ không khả dụng."
        }
        
        # Lấy ý nghĩa của mã trạng thái nếu có
        meaning = status_code_meanings.get(response.status_code, "Mã trạng thái không xác định.")
        
        print(f"Không thể truy cập, mã trạng thái: {response.status_code} - {meaning}")

# Đổi tên cột để bao gồm "day" ở cuối
df = pd.DataFrame(data, columns=['link', 'title', 'addr', 'dientich', 'bedroom', 'bathroom', 'price', 'day'])
df.to_csv('mogiday.csv', index=False)
