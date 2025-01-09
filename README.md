# Collecting + Cleaning + Building predict-real-estate-prices model

## Tính cấp thiết của vấn đề 🚨 🚨 🚨

Bất động sản đóng vai trò quan trọng trong nền kinh tế Việt Nam, với ảnh hưởng lớn đến các ngành như công nghiệp, nông nghiệp và dịch vụ. Ngành này không chỉ tạo ra nguồn thu lớn cho ngân sách nhà nước mà còn giải quyết việc làm cho một lượng lao động đáng kể. Tuy nhiên, thị trường bất động sản thường xuyên biến động do các yếu tố như lạm phát, lãi suất, và chính sách phát triển, đặc biệt trong những năm qua do tác động của đại dịch Covid-19. 

Việc định giá bất động sản phụ thuộc vào nhiều yếu tố như thị trường, thị yếu người tiêu dùng, diện tích, vị trí căn hộ, hướng, tầm nhìn và khoảng cách đến các tiện ích xã hội. Những yếu tố này ảnh hưởng trực tiếp đến giá bán nhà ở. Do đó việc nghiên cứu và phân tích các yếu tố ảnh hưởng đến giá bất động sản tại nơi đây là cần thiết để dự báo xu hướng thị trường và hỗ trợ các quyết định đầu tư, phát triển và quản lý bất động sản, từ đó đóng góp vào sự phát triển bền vững của xã hội và môi trường.

## Tổng quan quy trình thực hiện 🎯🎯🎯
1. [Thu thập dữ liệu](#Thu-thập-dữ-liệu)
2. [Tiền xử lý dữ liệu](#Tiền-xử-lý-dữ-liệu)
3. Xây dựng mô hình dự báo
4. Xây dựng web để người dùng dự đoán giá
   
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

3. Kết quả thu thập gồm 10.799 mẫu được đăng bán từ 2021-nay có dạng như sau:
        <p align="center">
            <img src="https://github.com/user-attachments/assets/b2beff85-9d4a-4b6e-adbe-eef34517750e" alt="image" width="450">
        </p>
        
4. Kiểm tra giá trị bị thiếu
   ```bash
   	df.info()
   ```
    <p align="center">
            <img src="https://github.com/user-attachments/assets/d76baccf-5d59-44c6-b57b-7f4b0fb40348" alt="image" width="350">
        </p>
Dữ liệu không có giá trị bị thiếu

## Tiền xử lý dữ liệu
### Sử dụng SQL để tiền xử lý dữ liệu
#### Một số vấn đề cần xử lý như sau
   1. Kiểm tra các giá trị thiếu 
   2. Loại bỏ các cột không cần thiết
   3. Định dạng lại kiểu dữ liệu cho đồng nhất
   4. Xử lý các giá trị Giá
   5. Xử lý các giá trị Ngày tháng
#### Cụ thể
##### 1. Kiểm tra các giá trị thiếu
       Đã kiểm tra ở trên bằng Python.
       
##### 2. Loại bỏ các cột không cần thiết
```bash
   ALTER TABLE mogi
   DROP COLUMN Link, Title;
```
##### 3. Định dạng lại kiểu dữ liệu cho đồng nhất

###### 3.1 Bởi vì các cột như Số phòng tắm, Số phòng ngủ và Diện tích có các ký tự văn bản lẫn vào nên cần loại bỏ và đồng nhất kiểu dữ liệu là int
```bash
      update mogiok
      set Bathroom = cast(substring(bathroom,1,charindex('WC',BathRoom)-1) as int)

      delete from mogiok
      where bedroom not like N'%PN%'
      update mogiok
      set bedroom =   cast(substring(BedRoom, 1, charindex('PN',BedRoom)-1) as int)
      
      --Cập nhật lại dientich 
      update mogiok
      set Area =cast(substring(Area,1,charindex('m2',Area)-1) as int)
```

###### 3.2 Cột Địa chỉ gồm Quận, Thành phố nên chỉ lấy Quận và Mã hóa thành dạng số để thuận tiện cho việc xây dựng mô hình dự đoán

```bash
   --Lấy ra thành phố từ cột Address
   update mogiok
   set address_final  = SUBSTRING(address, CHARINDEX('Quận', address) + 5, CHARINDEX(',', address) - (CHARINDEX('Quận', address) + 5))

   --Mã hóa
   SELECT DISTINCT address_final
   FROM mogiok;
   
   update  mogiok
   set address_final=N'Hòa Vang'
   where address_final like N'n Hoà Vang'
   
   alter table mogiok
   add  Address_ma_hoa int

   UPDATE mogiok
   SET Address_ma_hoa = CASE 
       WHEN address_final = N'HảiChâu' THEN 1
       WHEN address_final = N'LiênChiểu' THEN 2
       WHEN address_final = N'NgũHànhSơn' THEN 3
       WHEN address_final = N'CẩmLệ' THEN 4
       WHEN address_final = N'SơnTrà' THEN 5
       WHEN address_final = N'ThanhKhê' THEN 6
       WHEN address_final = N'Hòa Vang' THEN 7
       ELSE NULL
   END;
```

##### 4. Xử lý các giá trị Giá
Thực hiện việc tách và cắt để lấy các phần tử Tỷ, Triệu, Nghìn để chuyển về Tiền tệ và cộng chúng lại.
Sử dụng các hàm như:`Charindex`, `Substring` và `Cast`.
Ví dụ cho hàng Tỷ:
```bash
   update mogiok
   set billion =  case
			when price not like N'%tỷ%' and price like N'%triệu%' then 0
			when price like N'%tỷ%'   then cast(substring(price, 1, CHARINDEX(N'tỷ',price) -1) as numeric(15,0))
		  end
```
Tương tự cho các hàng còn lại. 
Sau khi tiền xử lý, dữ liệu có dạng như sau:
  <p align="center">
            <img src="https://github.com/user-attachments/assets/dd32d7a6-12e0-43a9-bc61-cb977a979de8" alt="image" width="450">
   </p>



