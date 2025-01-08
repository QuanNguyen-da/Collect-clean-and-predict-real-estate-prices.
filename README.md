# Collecting + Cleaning + Building predict-real-estate-prices model

## Tính cấp thiết của vấn đề

Bất động sản đóng vai trò quan trọng trong nền kinh tế Việt Nam, với ảnh hưởng lớn đến các ngành như công nghiệp, nông nghiệp và dịch vụ. Ngành này không chỉ tạo ra nguồn thu lớn cho ngân sách nhà nước mà còn giải quyết việc làm cho một lượng lao động đáng kể. Tuy nhiên, thị trường bất động sản thường xuyên biến động do các yếu tố như lạm phát, lãi suất, và chính sách phát triển, đặc biệt trong những năm qua do tác động của đại dịch Covid-19. 

Thành phố Đà Nẵng đang phát triển nhanh về kinh tế và dân số, dẫn đến nhu cầu nhà ở ngày càng tăng. Tuy nhiên, quỹ đất của thành phố rất hạn chế. Việc định giá bất động sản phụ thuộc vào nhiều yếu tố như thị trường, thị yếu người tiêu dùng, diện tích, vị trí căn hộ, hướng, tầm nhìn và khoảng cách đến các tiện ích xã hội. Những yếu tố này ảnh hưởng trực tiếp đến giá bán nhà ở. Do đó việc nghiên cứu và phân tích các yếu tố ảnh hưởng đến giá bất động sản tại nơi đây là cần thiết để dự báo xu hướng thị trường và hỗ trợ các quyết định đầu tư, phát triển và quản lý bất động sản, từ đó đóng góp vào sự phát triển bền vững của xã hội và môi trường.

## Thu thập dữ liệu 
### Sử dụng Python để thu thập dữ liệu từ web Bất động sản: Mogi.vn
1. Những thư viện cần thiết:
   ```bash
              import requests
              import pandas as pd
              from bs4 import BeautifulSoup
   ```
2. Những thông tin cần thu thập:
   ```bash
            link = house.find('a', class_="link-overlay")['href']
            title = house.find('h2', class_="prop-title").text.strip()
            addr = house.find('div', class_="prop-addr").text.strip()
            price = house.find('div', class_="price").text.strip()
            attributes = [li.text.strip() for li in house.find('ul', class_='prop-attr').find_all('li')] if house.find('ul', class_='prop-attr') else ["N/A", "N/A"]
            dientich = attributes[0].strip()
            bedroom = attributes[1].strip()
            bathroom = attributes[2].strip()
   ```

3. Kết quả thu thập gồm 10.211 mẫu tại Đà Nẵng được đăng bán từ 2021-nay có dạng như sau:
        <p align="center">
            <img src="https://github.com/user-attachments/assets/b2beff85-9d4a-4b6e-adbe-eef34517750e" alt="image" width="450">
        </p>

      
## Tiền xử lý dữ liệu
### Sử dụng SQL để tiền xử lý dữ liệu


