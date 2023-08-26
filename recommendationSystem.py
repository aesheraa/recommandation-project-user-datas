

# merhaba bu projeyi vscode da .ipynb uzantılı dosyada notebook kullanarak kodlayıp çalıştırdım githuba atmak için kodları .py uznatılı dosyaya taşıyıp öyle atıyorum :))))
# siz de çalıştırırken notebook kullanın 


import numpy as np 
import pandas as pd 

column_names = ['user_id' , 'item_id' , 'rating' , 'timestamp']
df= pd.read_csv ( 'users.data ' , sep='/t' , names=column_names)

df.head()

#kaç kayıt varmış görelim
len(df)


#şimdi diger dosyamızı yükleyelim
movie_titles= pd.read_csv('movie_id_titles.csv')
movie_titles.head()


#kaç kayıt varmış görelim 
len(movie_titles)

df=pd.merge(df, movie_titles , on='item_id')
df.head()


# Recommandation Systemimi kuruyorum
# öncelikle exceldeki pivot tablo benzeri bir yapı kuruyorum
# bu yapıya göre her kullanıcı bir satır olacak şekilde yani datframe'imin index'i user_id olacak
# sutunlarda film isimleri ( yani title sutunu ) olacak 
# tablo içinde de rating değerleri olacak şekilde bir dataframe oluşturuyorum 


moviemat= df.pivot_table(index='user_id' , columns='title ' , values='rating')
moviemat.head()

type(moviemat)


# amacım  Star Wars filmine benzer film önerileri yapmak 
# Star Wars  (1977) filminin user rating değerlerine bakıyorum 
starwars_user_ratings = moviemat['Star Wars (1977)' ]
starwars_user_ratings.head()



#corrwith metodu kullanarak Star Wars filmi ile korelasyonları hesaplatıyorum :
similar_to_starwars= moviemat.corrwith(starwars_user_ratings)
similar_to_starwars
type(similar_to_starwars)



# bazı kayıtlarda boşluklar olduğu için hata veriyor similar_to_starwars bir seri, biz bunu corr_starwars isimli bir dataframe'e dönüştürelim  ve NaN kayıtlarını temizleyip bakalım
corr_starwars= pd.DataFrame(similar_to_starwars , columns=[ 'Correlation'])
corr_starwars.dropna(inplace=True)
corr_starwars.head()



# elde ettiğimiz datframe'i sıralayalım ve tavsiyelerine bakalım 
corr_starwars.sort_values('Correlation' , ascending= False).head(10)



# alakasız sonuçlar verdi çünkü çok az oy almış filmleri bile işleme dahil etti, bunu engellemek için 100 den az oy alan fillmleri eliyorum 
# ratings isimli bir dataframe oluturuyorum ve her filmin kaç oy aldığını ( oy sayılarını ) tutuyorum 




df.head()


# timestamp sutununa ihtiyacım yok onu siliyorum 
df.drop(['timestamp'] , axis=1 )



# her filmin ortalama (mean value) rating değerini buluyorum
ratings =pd.DataFrame(df.groupby('title')['rating'].mean())



# büyükten küçüğe sıralayıp bakıyorum 
ratings.sort_values('rating' , ascending=False).head()



# bu ortalamalar hesaplanırken kaç oy aldığına bakmadık o yüzden hiç bilinmeyen filmler önerdi
# şimdi her filmin aldığı oy sayısını bulalım 
ratings[ 'rating_oy_sayisi']=pd.DataFrame(pd.groupby('title')['rating'].count())
ratings.head()



# şimdi en çok oy alan filmleri büyüktrn küçüğe sıralayalım 
ratings.sort_values('rating_oy_sayisi' , ascending=False).head()



#  asıl amacıma dönüyorum ve corr_starwars datframe'ime  rating_oy_sayisi sutununu ekliyorum ( join ile )
corr_starwars.sort_values('Correlation', ascending=False).head(10)
corr_starwars= corr_starwars.join(ratings['rating_oy_sayisi']) 
corr_starwars.head()




# sonuca bakalım 
corr_starwars[corr_satarwars['rating_oy_sayisi ']>100.sort_values('Correlation' , ascending=False)].head()

