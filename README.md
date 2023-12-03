# 💻 Readify

![deploy workflow](https://github.com/KelompokD02PBP/proyekts/actions/workflows/pbp-deploy.yml/badge.svg)
![testing workflow](https://github.com/KelompokD02PBP/proyekts/actions/workflows/testing.yml/badge.svg)
<br>
Website: [http://readify-d02-tk.pbp.cs.ui.ac.id](http://readify-d02-tk.pbp.cs.ui.ac.id)

## 🏫 Proyek Tengah Semester dari kelompok D02 PBP
Nama-nama anggota kelompok
1. Venedict Chen - 2206024436
2. Sefriano Edsel Jieftara Djie - 2206818966
3. Kenichi Komala - 2206081452
4. Shabhi Aliyya Siyauqi Dzakia - 2206083741
5. Sabina Maritza Moenzil - 2206027583

## Cerita aplikasi yang diajukan serta manfaatnya

Website yang ingin kami buat berfungsi sebagai sarana untuk review buku.
Jadi dengan website ini user bisa memberi rating mereka terhadap suatu buku dan juga memberikan komentar terhadap buku yang mereka review. Harapannya aplikasi ini dapat berguna untuk pembaca bisa mencari review dari buku yang ingin mereka baca.

## Daftar modul yang akan diimplementasikan

Kami menggunakan django untuk framework websitenya dan menggunakan HTML,CSS, BootStrap, serta Javascript untuk client side programming. Untuk memproses dataset bukunya kita menggunakan pandas.
Kita akan mengimplementasikan 
## Page
### Page login dan register
- Page yang akan muncul saat user masuk ke website pertama kali. Pada page ini user akan diminta untuk memasukan data dan akan diautentikasi datanya.
### Page katalog/main
- Pada page ini akan ditampilkan semua buku yang bisa direview. Page ini akan menampilkan 50 buku pertama pada daftar katalog. Lalu, ada tombol next page dan prevpage untuk melihat 50 buku lain.
### Page tiap buku
- Pada page ini user bisa membuat komentar terhadap buku dan menambahkan buku ke daftar favoritnya.

---

## Fitur
### Fitur search
- Dengan fitur ini user bisa melakukan search pada main page untuk mendapatkan buku yang sudah terfilter
### Fitur favorit untuk tiap user
- Setiap user dapat menambahkan buku yang disukai ke
### Fitur sort
- Dengan fitur ini, user bisa mengurutkan buku yang keluar dalam urutan lexikograf dan tahun publish
### Fitur filter favorit
- Fitur ini akan memberikan kesempatan bagi pengguna untuk dapat melakukan filter buku yang ditandai dengan favorit oleh pengguna.
### Fitur komentar pada tiap buku
- Dengan fitur ini, user bisa membuat komentar pada page buku ke - n

## Sumber dataset katalog buku
Kami mengambil data set  `books.csv` dari
https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset/?select=Books.csv

## Role dari pengguna pada website 
Pada website kami, role pengguna diberikan sebagai reviewer dan pengomentar terhadap buku.
