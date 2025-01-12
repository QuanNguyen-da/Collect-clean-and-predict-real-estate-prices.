{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "5c32057e",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.preprocessing import OrdinalEncoder\n",
    "from xgboost import XGBRegressor\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "196438bf",
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "id": "89e6d04d",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Nhập dữ liệu\n",
    "df = pd.read_excel(r'C:\\Users\\DELL\\Phân tích dữ liệu bằng Python\\Practice_crawl\\predict_web\\truongluong.xlsx')\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 34,
   "id": "3f83dbe1",
   "metadata": {},
   "outputs": [],
   "source": [
    "from unidecode import unidecode\n",
    "\n",
    "# Hàm để xử lý cột province\n",
    "def remove_accents_and_correct(province):\n",
    "    # Loại bỏ khoảng trắng thừa và chuẩn hóa thành chữ thường\n",
    "    province = province.strip()\n",
    "\n",
    "    # Sửa lỗi chính tả nếu có\n",
    "    if province == \"Bình Dươn\":\n",
    "        province = \"Bình Dương\"\n",
    "    elif province == \"Bà Rịa -\":\n",
    "        province = \"Bà Rịa Vũng Tàu\"\n",
    "    elif province == \"Bình Phướ\":\n",
    "        province = \"Bình Phước\"\n",
    "        \n",
    "    # Loại bỏ dấu\n",
    "    return unidecode(province)\n",
    "\n",
    "# Áp dụng hàm vào cột 'province'\n",
    "df['Province'] = df['Province'].apply(remove_accents_and_correct)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 40,
   "id": "e44fa080",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "['TPHCM' 'Ha Noi' 'Binh Duong' 'Lam Dong' 'Da Nang' 'Bac Giang'\n",
      " 'Ba Ria Vung Tau' 'Dong Nai' 'Can Tho' 'Bac Ninh' 'Binh Phuoc'\n",
      " 'Khanh Hoa' 'Tay Ninh']\n"
     ]
    }
   ],
   "source": [
    "# Hàm để xử lý cột province\n",
    "def correct_province_names(province):\n",
    "    # Sửa lỗi chính tả nếu có\n",
    "    if province == \"Ba Ria -\":\n",
    "        province = \"Ba Ria Vung Tau\"\n",
    "    elif province == \"Binh Phuo\":\n",
    "        province = \"Binh Phuoc\"\n",
    "    \n",
    "    return province\n",
    "\n",
    "# Áp dụng hàm vào cột 'province'\n",
    "df['Province'] = df['Province'].apply(correct_province_names)\n",
    "\n",
    "# Kiểm tra kết quả\n",
    "print(df['Province'].unique())\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 41,
   "id": "3769c19b",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "<class 'pandas.core.frame.DataFrame'>\n",
      "RangeIndex: 10785 entries, 0 to 10784\n",
      "Data columns (total 5 columns):\n",
      " #   Column    Non-Null Count  Dtype  \n",
      "---  ------    --------------  -----  \n",
      " 0   Area      10785 non-null  int64  \n",
      " 1   Bathroom  10785 non-null  int64  \n",
      " 2   Bedroom   10785 non-null  int64  \n",
      " 3   Price     10785 non-null  float64\n",
      " 4   Province  10785 non-null  object \n",
      "dtypes: float64(1), int64(3), object(1)\n",
      "memory usage: 421.4+ KB\n"
     ]
    }
   ],
   "source": [
    "df.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 42,
   "id": "cf9944d5",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Tách biến độc lập và phụ thuộc | x: biến độc lập, y: biến phụ thuộc\n",
    "x=df.drop('Price',axis=1)\n",
    "y=df[['Price']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 43,
   "id": "11ddf401",
   "metadata": {},
   "outputs": [],
   "source": [
    "#Chia dữ liệu thành tập huấn luyện và tập test\n",
    "x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.25)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 44,
   "id": "99ba161e",
   "metadata": {},
   "outputs": [],
   "source": [
    "encoder=OrdinalEncoder()\n",
    "encoder.fit(x_train[['Province']])\n",
    "x_train[['Province']]=encoder.transform(x_train[['Province']])\n",
    "x_test[['Province']]=encoder.transform(x_test[['Province']])\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 45,
   "id": "bd66b6ee",
   "metadata": {},
   "outputs": [],
   "source": [
    "model=XGBRegressor()\n",
    "model.fit(x_train,y_train)\n",
    "predict=model.predict(x_test)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 46,
   "id": "c1c58f57",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "R-squared (R²): 0.48396458425823496\n"
     ]
    }
   ],
   "source": [
    "from sklearn.metrics import r2_score\n",
    "\n",
    "r2 = r2_score(y_test, predict)\n",
    "print(\"R-squared (R²):\", r2)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 47,
   "id": "a1762b87",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Area</th>\n",
       "      <th>Bathroom</th>\n",
       "      <th>Bedroom</th>\n",
       "      <th>Price</th>\n",
       "      <th>Province</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>102</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>4.20</td>\n",
       "      <td>TPHCM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>120</td>\n",
       "      <td>14</td>\n",
       "      <td>14</td>\n",
       "      <td>28.50</td>\n",
       "      <td>TPHCM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>21</td>\n",
       "      <td>4</td>\n",
       "      <td>3</td>\n",
       "      <td>3.80</td>\n",
       "      <td>TPHCM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>58</td>\n",
       "      <td>3</td>\n",
       "      <td>2</td>\n",
       "      <td>2.90</td>\n",
       "      <td>TPHCM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>60</td>\n",
       "      <td>5</td>\n",
       "      <td>3</td>\n",
       "      <td>8.90</td>\n",
       "      <td>TPHCM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>10780</th>\n",
       "      <td>50</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>2.55</td>\n",
       "      <td>TPHCM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>10781</th>\n",
       "      <td>250</td>\n",
       "      <td>4</td>\n",
       "      <td>4</td>\n",
       "      <td>24.00</td>\n",
       "      <td>TPHCM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>10782</th>\n",
       "      <td>78</td>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>2.30</td>\n",
       "      <td>TPHCM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>10783</th>\n",
       "      <td>64</td>\n",
       "      <td>5</td>\n",
       "      <td>4</td>\n",
       "      <td>7.30</td>\n",
       "      <td>TPHCM</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>10784</th>\n",
       "      <td>79</td>\n",
       "      <td>6</td>\n",
       "      <td>6</td>\n",
       "      <td>42.00</td>\n",
       "      <td>TPHCM</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>10785 rows × 5 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "       Area  Bathroom  Bedroom  Price Province\n",
       "0       102         0        0   4.20    TPHCM\n",
       "1       120        14       14  28.50    TPHCM\n",
       "2        21         4        3   3.80    TPHCM\n",
       "3        58         3        2   2.90    TPHCM\n",
       "4        60         5        3   8.90    TPHCM\n",
       "...     ...       ...      ...    ...      ...\n",
       "10780    50         0        0   2.55    TPHCM\n",
       "10781   250         4        4  24.00    TPHCM\n",
       "10782    78         0        0   2.30    TPHCM\n",
       "10783    64         5        4   7.30    TPHCM\n",
       "10784    79         6        6  42.00    TPHCM\n",
       "\n",
       "[10785 rows x 5 columns]"
      ]
     },
     "execution_count": 47,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 53,
   "id": "6f3e827a",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "196.64122\n"
     ]
    }
   ],
   "source": [
    "new_sample=[[100,5,5,13]]\n",
    "df_sample=pd.DataFrame(new_sample)\n",
    "df_sample.columns=x.columns\n",
    "pred=model.predict(df_sample)[0]\n",
    "print(pred)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 54,
   "id": "dc782412",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pickle\n",
    "import joblib\n",
    "pickle.dump(model,open('model_HR.pkl','wb'))\n",
    "joblib.dump(model,open('model_HR.sav','wb'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 55,
   "id": "4bc25b93",
   "metadata": {},
   "outputs": [],
   "source": [
    "import json\n",
    "dept={'Province_value':list(x.Province.unique())}\n",
    "with open ('Province_value.json','w') as f:\n",
    "    f.write(json.dumps(dept))"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "base",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
