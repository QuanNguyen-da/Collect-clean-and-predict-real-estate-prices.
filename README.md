# Collecting + Cleaning + Building predict-real-estate-prices model

## Tính cấp thiết của vấn đề 🚨 🚨 🚨

Bất động sản đóng vai trò quan trọng trong nền kinh tế Việt Nam, với ảnh hưởng lớn đến các ngành như công nghiệp, nông nghiệp và dịch vụ. Ngành này không chỉ tạo ra nguồn thu lớn cho ngân sách nhà nước mà còn giải quyết việc làm cho một lượng lao động đáng kể. Tuy nhiên, thị trường bất động sản thường xuyên biến động do các yếu tố như lạm phát, lãi suất, và chính sách phát triển, đặc biệt trong những năm qua do tác động của đại dịch Covid-19. 

Việc định giá bất động sản phụ thuộc vào nhiều yếu tố như thị trường, thị yếu người tiêu dùng, diện tích, vị trí căn hộ, hướng, tầm nhìn và khoảng cách đến các tiện ích xã hội. Những yếu tố này ảnh hưởng trực tiếp đến giá bán nhà ở. Do đó việc nghiên cứu và phân tích các yếu tố ảnh hưởng đến giá bất động sản tại nơi đây là cần thiết để dự báo xu hướng thị trường và hỗ trợ các quyết định đầu tư, phát triển và quản lý bất động sản, từ đó đóng góp vào sự phát triển bền vững của xã hội và môi trường.

## Tổng quan quy trình thực hiện 🎯🎯🎯
1. [Thu thập dữ liệu](#Thu-thập-dữ-liệu)
2. [Tiền xử lý dữ liệu](#Tiền-xử-lý-dữ-liệu)
3. [Xây dựng mô hình dự đoán](#Xây-dựng-mô-hình-dự-đoán)
4. Xây dựng web để người dùng dự đoán giá
   
## 1. Thu thập dữ liệu 
### Sử dụng Python để thu thập dữ liệu từ web Bất động sản: Mogi.vn

1.1. Những thư viện cần thiết:
   ```sql
              import requests
              import pandas as pd
              from bs4 import BeautifulSoup
   ```
1.2. Những thông tin cần thu thập:
   ```sql
            link = house.find('a', class_="link-overlay")['href']
            title = house.find('h2', class_="prop-title").text.strip()
            addr = house.find('div', class_="prop-addr").text.strip()
            price = house.find('div', class_="price").text.strip()
            attributes = [li.text.strip() for li in house.find('ul', class_='prop-attr').find_all('li')] if house.find('ul', class_='prop-attr') else ["N/A", "N/A"]
            dientich = attributes[0].strip()
            bedroom = attributes[1].strip()
            bathroom = attributes[2].strip()
   ```

1.3. Kết quả thu thập gồm 10.799 mẫu được đăng bán từ 2021-nay có dạng như sau:
        <p align="center">
            <img src="https://github.com/user-attachments/assets/42824589-1ea6-4e04-bf20-f50b9c6d3c19" alt="image" width="450">
        </p>

1.4. Kiểm tra giá trị bị thiếu
    	<p align="center">
            <img src="https://github.com/user-attachments/assets/d76baccf-5d59-44c6-b57b-7f4b0fb40348" alt="image" width="350">
        </p>
	
Dữ liệu không có giá trị bị thiếu

## 2.  Tiền xử lý dữ liệu
### Sử dụng SQL để tiền xử lý dữ liệu
#### Một số vấn đề cần xử lý như sau
   2.1. Kiểm tra các giá trị thiếu 
   
   2.2. Loại bỏ các cột không cần thiết
   
   2.3. Định dạng lại kiểu dữ liệu cho đồng nhất
   
   2.4. Xử lý các giá trị Giá
   
   2.5. Xử lý các giá trị Ngày tháng
   
#### Cụ thể
##### 2.1. Kiểm tra các giá trị thiếu
       Đã kiểm tra ở trên bằng Python.
       
##### 2.2. Loại bỏ các cột không cần thiết
```sql
   ALTER TABLE mogi
   DROP COLUMN Link, Title;
```
##### 2.3. Định dạng lại kiểu dữ liệu cho đồng nhất

###### 2.3.1 Bởi vì các cột như Số phòng tắm, Số phòng ngủ và Diện tích có các ký tự văn bản lẫn vào nên cần loại bỏ và đồng nhất kiểu dữ liệu là int

```sql
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

###### 2.3.2 Cột Địa chỉ gồm Quận, Thành phố nên chỉ lấy Quận và Mã hóa thành dạng số để thuận tiện cho việc xây dựng mô hình dự đoán

```sql
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

##### 2.4. Xử lý các giá trị Giá
Thực hiện việc tách và cắt để lấy các phần tử Tỷ, Triệu, Nghìn để chuyển về Tiền tệ và cộng chúng lại.

Sử dụng các hàm như:`Charindex`, `Substring` và `Cast`.

Ví dụ cho hàng Tỷ:
```sql
   update mogiok
   set billion =  case
			when price not like N'%tỷ%' and price like N'%triệu%' then 0
			when price like N'%tỷ%'   then cast(substring(price, 1, CHARINDEX(N'tỷ',price) -1) as numeric(15,0))
		  end
```
Tương tự cho các hàng còn lại. Có thể tham khảo cụ thể hơn ở file Pre-processing.sql


## 3. Xây dựng mô hình dự đoán
Đầu tiên, ta chuẩn bị môi trường để thực hiện các tác vụ liên quan đến mô hình cây quyết định và đánh giá hiệu suất của nó trong bài toán phân loại, bao gồm:

+ Thư viện pandas
+ Thư viện Matplotlib.pyplot, seaborn để vẽ biểu đồ và đồ thị.
+ Import module model_selection từ thư viện scikit-learn. Module này thường được sử dụng để chia dữ liệu thành các tập huấn luyện và tập kiểm tra.
+ Import hàm classification_report từ module metrics trong scikit-learn. Hàm này cung cấp báo cáo chi tiết về hiệu suất của mô hình phân loại.
+ Import hàm accuracy_score từ module metrics trong scikit-learn. Hàm này tính toán độ chính xác của mô hình.

```python
	import pandas as pd
	import numpy as np
	import matplotlib.pyplot as plt
	import seaborn as sns
	from sklearn import linear_model
```
Bộ dữ liệu này có 10796 dòng với 5 cột lần lượt là:
- Diện tích (Area)
- Địa chỉ (Address)
- Số phòng ngủ (Bedroom)
- Số phòng tắm (Bathroom)
- Giá nhà (Price).

Mã hoá 13 tỉnh/thành phố ở cột “Address” về dạng số (từ 0 đến 12), ta được bảng mới như sau:

```bash
	df['Address']=df['Address'].astype('category')
	df['Address']=df['Address'].cat.codes
```
Tiếp theo xem xét mối quan hệ tương quan, tác động lẫn nhau giữa các biến. 

Sau đó gán mức giá của các ngôi nhà ở cột “Price” cho 3 nhãn “Low”, “Medium” và “High” lần lượt là các mức giá thấp, trung bình, cao và tạo thêm cột mới “price_label” với quy định:
+ Ngôi nhà có mức giá thấp (Low) sẽ có giá dưới 10 tỷ đồng.
+ Ngôi nhà có mức giá trung bình (Medium) có giá từ 10-50 tỷ đồng.
+ Ngôi nhà có mức giá cao (High) có giá trên 50 tỷ đồng.

Số giá trị ở mỗi phân lớp như sau:
+ Có 6192 ngôi nhà có mức giá thấp.
+ Có 3585 ngôi nhà có mức giá trung bình.
+ Có 1019 ngôi nhà có mức giá cao.
  
#### Thực hiện xây dựng mô hình dự đoán 
- Bởi vì đây là bài toán dự đoán giá bất động sản nên kết quả đầu ra sẽ là các giá trị tiền tệ tương ứng với dữ liệu đầu vào, việc sử dụng các mô hình phân lớp Classification là không hợp lý. Chính vì thế nên chọn mô hình XGBRegressor.

+ Hàm train_test_split được sử dụng để phân chia các biến X (4 cột đầu tiên) và Y (cột “price_label”) thành các tập huấn luyện và kiểm tra. Tham số test_size chỉ định tỷ lệ dữ liệu được sử dụng trong bộ thử nghiệm. Trong trường hợp này, 30% dữ liệu sẽ được sử dụng trong bộ kiểm tra. Tham số Random_state được sử dụng để đảm bảo rằng việc phân chia có thể lặp lại được.
 ```bash
	from sklearn.model_selection import train_test_split
	
	array = data.values
	X = array[:, 0:4]
	Y = array[:, 4]
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)
```
Lớp DecisionTreeClassifier được nhập từ mô-đun sklearn.tree. Lớp này thực hiện phân loại cây quyết định:
```bash
	from sklearn import tree
	
	decision_tree = tree.DecisionTreeClassifier(criterion='gini')
	decision_tree.fit(X_train, Y_train)
```
Để kiểm tra độ chính xác, ta in ra dòng kiểm tra độ chính xác của bộ phân loại cây quyết định trên dữ liệu huấn luyện. Phương thức Decision_tree.score() được sử dụng để tính toán độ chính xác. Công cụ xác định định dạng .2f được sử dụng để định dạng giá trị chính xác đến hai chữ số thập phân.

Kết quả thu được cho thấy, độ chính xác cho mô hình này dựa trên tập huấn luyện là rất cao (93%) và tập kiểm tra cũng không hề thấp (84%).




