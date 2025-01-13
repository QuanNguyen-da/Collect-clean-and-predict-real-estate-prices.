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
Đầu tiên, ta chuẩn bị môi trường để thực hiện các tác vụ liên quan đến mô hình dự đoán và đánh giá hiệu suất của nó, bao gồm:

```python
	import pandas as pd
	from sklearn.model_selection import train_test_split
	from sklearn.preprocessing import OrdinalEncoder
	from xgboost import XGBRegressor
	from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
	from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
	from unidecode import unidecode
```
Kiểm tra thông tin của dữ liệu:
![image](https://github.com/user-attachments/assets/40a48e14-ccb8-4c89-842f-9a9bd918d714)

Bộ dữ liệu này có 10785 dòng và không có giá trị null với 5 cột lần lượt là:
- Diện tích (Area)
- Địa chỉ (Address)
- Số phòng ngủ (Bedroom)
- Số phòng tắm (Bathroom)
- Giá nhà (Price).

Đối với cột Address dùng hàm loại bỏ dấu và khoảng trắng để thuận tiện cho việc mã hóa sau này.Và đổi thành Province vì chỉ lấy các giá trị tỉnh thành.

Thực hiện kiểm tra các giá trị ngoại lai bằng Box Plot và thay thế bằng các giá trị hợp lý. Sau đó cần xem xét mối quan hệ giữa các biến bằng biểu đồ phân tán và heatmap. 

Mọi thứ đều được kiểm tra xong và bắt đầu xây dựng mô hình dự đoán. 

  
#### Thực hiện xây dựng mô hình dự đoán 
- Bởi vì đây là bài toán dự đoán giá bất động sản nên kết quả đầu ra sẽ là các giá trị tiền tệ tương ứng với dữ liệu đầu vào, việc sử dụng các mô hình phân lớp Classification là không hợp lý. Chính vì thế nên chọn mô hình XGBRegressor.

+ Hàm train_test_split được sử dụng để phân chia các biến X (4 cột đầu tiên) và Y (cột “price_label”) thành các tập huấn luyện và kiểm tra. Tham số test_size chỉ định tỷ lệ dữ liệu được sử dụng trong bộ thử nghiệm. Trong trường hợp này, 30% dữ liệu sẽ được sử dụng trong bộ kiểm tra. Tham số Random_state được sử dụng để đảm bảo rằng việc phân chia có thể lặp lại được.

``` python
	#Tách biến độc lập và phụ thuộc | x: biến độc lập, y: biến phụ thuộc
	x=df.drop('Price',axis=1)
	y=df[['Price']]
	#Chia dữ liệu thành tập huấn luyện và tập test
	x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25)
```

Mô hình chỉ nhận giá trị số nên đối với cột Province dùng `OrdinalEncoder` để mã hóa.
```python
	encoder=OrdinalEncoder()
	encoder.fit(x_train[['Province']])
	x_train[['Province']]=encoder.transform(x_train[['Province']])
	x_test[['Province']]=encoder.transform(x_test[['Province']])
```
Độ chính xác của mô hình là 70%, có thể chấp nhận được.

Tạo file json chứa danh sách gồm các tỉnh:

```python
	provinces = {'Provinces_value': list(x['Province'].unique())}
	with open('Provinces_value.json', 'w') as f:
	    f.write(json.dumps(provinces))

```
Lưu mô hình thành file .pkl hoặc .sav tạo API và xây dựng web dự đoán. 
```python
	#pickle.dump(model, open('model_HR.pkl', 'wb'))
	joblib.dump(model, open('model_HR.sav', 'wb'))
```




