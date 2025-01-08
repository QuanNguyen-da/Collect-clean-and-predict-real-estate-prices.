select * from Mogiok

--Thêm cột tiền tỷ
alter table Mogiok
add billion numeric(15,0)

--Thêm cột tiền triệu
alter table Mogiok
add million numeric(15,0)

--Thêm cột đơn vị nghìn
alter table Mogiok
add thousand numeric(15,0)

---Thêm cột price sau khi xử lý
alter table mogiok
add Price_Final numeric(15,0)

select * from mogiok where price like N'%nghìn%'
--cập nhật giá trị cho cột đơn vị nghìn
UPDATE mogiok
SET thousand = CAST(SUBSTRING(price, CHARINDEX(N'triệu', price) + 6, 3) AS NUMERIC(15, 3))
WHERE price LIKE N'%nghìn%';
UPDATE mogiok
SET thousand = 0
WHERE price not LIKE N'%nghìn%';

EXEC sp_columns mogiok;



-- Cập nhật giá trị cho cột tiền tỷ
update mogiok
set billion =  case when price not like N'%tỷ%' and price like N'%triệu%' then 0
					when price like N'%tỷ%'   then cast(substring(price, 1, CHARINDEX(N'tỷ',price) -1) as numeric(15,0))

				end

delete from mogiok
where substring(price,charindex(N'tỷ',price)+3,3) like N'%7 t%'

--Cập nhật giá trị cho cột tiền triệu
update mogiok
set million =  case when price not like N'%triệu%' 					then 0
when price like N'%triệu%' and price like N'%tỷ%' 
					then cast(substring(price,charindex(N'tỷ',price)+3,3) as numeric(15,0))
					when price  like N'%triệu%' and price not like N'%tỷ%'  
					then cast(substring(price,1,charindex(N'triệu',price)-1) as numeric(15,0))
end

select * from mogiok
UPDATE mogiok
SET billion = billion * 1000000000;


UPDATE mogiok
SET million = million * 1000000;

UPDATE mogiok
SET thousand = thousand * 1000;

--Quy đổi giá trị triệu thành tỷ 
update mogi 
set Price_Final=billion+million+thousand

select * from mogiok

 
--Cập nhật giá trị cho cột Price_Final
update mogiok
set price_final = (billion+million+thousand)

select bedroom, len(bedroom) from mogiok

--Cập nhật giá trị cho cột số phòng ngủ
update mogiok
set bedroom =   cast(substring(BedRoom, 1, charindex('PN',BedRoom)-1) as int)

select bedroom from mogiok where bedroom not like N'%PN%'

delete from mogiok
where bedroom not like N'%PN%'



--Cập nhật giá trị cho cột số phòng WC
update mogiok
set Bathroom = cast(substring(bathroom,1,charindex('WC',BathRoom)-1) as int)

--Cập nhật lại dientich 
update mogiok
set Area =cast(substring(Area,1,charindex('m2',Area)-1) as int)

--Thêm cột Address_final
alter table mogiok
add address_final nvarchar(100)

select * from mogiok
--Lấy ra thành phố từ cột Address
update mogiok
set address_final  = SUBSTRING(address, CHARINDEX('Quận', address) + 5, CHARINDEX(',', address) - (CHARINDEX('Quận', address) + 5))


SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'mogiok' AND COLUMN_NAME = 'Date';

select date from mogiok
WHERE year(date) =2025;

UPDATE mogiok
SET date = 
     SUBSTRING([Date], 7, 4) + '-' + SUBSTRING([Date], 4, 2) + '-' + SUBSTRING([Date], 1, 2)
WHERE ISDATE([Date]) = 0;





select * from mogiok

SELECT DISTINCT address_final
FROM mogiok;

update  mogiok
set address_final=N'Hòa Vang'
where address_final like N'n Hoà Vang'

alter table mogiok
add  Address_ma_hoa int

UPDATE mogiok
SET address_final = REPLACE(address_final, ' ', '')
WHERE address_final LIKE '% %';

UPDATE mogiok
SET address_final = REPLACE(REPLACE(REPLACE(address_final, 'HòaVang', 'Hòa Vang'), 'HảiChâu', 'Hải Châu'), 'LiênChiểu', 'Liên Chiểu')
-- Tiếp tục với các từ khác nếu có
WHERE address_final IN ('HòaVang', 'HảiChâu', 'LiênChiểu', 'NgũHànhSơn', 'CẩmLệ', 'SơnTrà', 'ThanhKhê');

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

select * from mogiok