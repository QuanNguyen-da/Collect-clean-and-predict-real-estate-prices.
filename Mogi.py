import requests
import pandas as pd
data=[]
from bs4 import BeautifulSoup


for page in range(1,101):
    url=f'https://mogi.vn/da-nang/mua-nha-dat?cp={page}'
    response = requests.get(url)
    if response.status_code==200:
        print(f'Truy cập trang thứ {page} thành công')
        soup = BeautifulSoup(response.text, 'html.parser')
        houses = soup.find_all('div', class_='prop-info')

        for house in houses:
            link = house.find('a',class_="link-overlay")['href']
            title=house.find('h2',class_="prop-title").text.strip()
            addr=house.find('div', class_="prop-addr").text.strip()
            price=house.find('div',class_="price").text.strip()
            attributes = [li.text.strip() for li in house.find('ul', class_='prop-attr').find_all('li')] if house.find('ul', class_='prop-attr') else ["N/A", "N/A"]
            dientich = attributes[0].strip()
            bedroom = attributes[1].strip()
            bathroom = attributes[2].strip()
            data.append([link, title, addr, dientich, bedroom, bathroom, price])

        

        print("Dữ liệu đã lưu vào file CSV!")

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
df = pd.DataFrame(data, columns=['link', 'title', 'addr', 'dientich', 'bedroom', 'bathroom', 'price'])
df.to_csv('mogi_houses.csv', index=False)

print("Dữ liệu đã lưu vào file CSV!")
    
