# 🏀 **Prime Basket Place — Proyek Tengah Semester A10**

> Aplikasi jual beli alat-alat olahraga basket.

---

### 👥 **Anggota Kelompok**

| Nama | NPM |
|------|------|
| Rafsanjani | 2406495400 |
| Iqbal Rafi Nuryana | 2406417462 |
| Farras Syafiq Ulumuddin | 2406495722 |
| Z Arsy Alam Sin | 2406495836 |
| Michael Stephen Daniel Panjaitan | 2406496321 |

---

### 🧩 **Cerita dan Manffat**

**Prime Basket Place** merupakan sebuah aplikasi jual-beli yang dikhususkan untuk alat-alat olahraga basket.  
Disini para pencinta basket bisadatang untuk mempersiapkan dirinya menjadi Pro Player Basketball.  
Aplikasi ini menawarkan tempat untuk beragam alat-alat basket yang bisa dibeli ataupun dijual untuk pengguna ditambah dengan adanya fitur ulasan dan detail yang bisa memudahkan untuk pengguna memilih alat yang kualitas bagus. ☆

---

## 📦 **Daftar Modul**

---

### 🔐 **Account**

🧠 **Deskripsi:**  
Modul Account berfungsi sebagai pusat identitas dan aktivitas pengguna di **Prime Basket Place**.  
Di dalam modul ini, pengguna dapat melakukan berbagai hal seperti mengelola profil pribadi, melihat riwayat transaksi pembelian maupun penjualan alat basket, serta memantau produk yang pernah mereka ulas atau sukai.  

⚙️ **Fitur Utama:**  
- Mengubah **profil dan password**.  
- Memperbarui **informasi profil**.  
- Melihat **status transaksi dan pengiriman** secara *real-time*.  
- Melihat **riwayat transaksi**, **produk yang diulas**, dan **produk yang disukai**.  
- Menghapus **Akun dari sisi pengguna atau admin** 

🔒 **Akses Pengguna:**  
- **User:** Akses penuh terhadap fitur personal.  
- **Guest:** Dialihkan ke halaman login.  
- **Admin:** Akses terbatas hanya untuk pengelolaan data pengguna.  

🧾 **CRUD:**
| Operasi | Deskripsi | Akses |
|----------|------------|--------|
| **Read** | Melihat data profil dan riwayat aktivitas | User, Admin |
| **Update** | Mengubah profil dan password | User |
| **Delete** | Mengubah profil dan password | User |
| **Create** | Menghapus akun pengguna dari sistem | User, Admin |

---

### 🏠 **Homepage**

🧠 **Deskripsi:**  
Aplikasi ini menampilkan halaman utama berisi produk-produk olahraga basket di toko.  
Antarmuka dilengkapi dengan fitur pencarian, pemfilteran, dan pengurutan produk agar pengguna dapat menemukan produk yang diinginkan.  
Terdapat pula fitur *slider* untuk menampilkan produk-produk populer, direkomendasikan, atau sedang diskon.  

⚙️ **Fitur Utama:**  
- 🔎 **Pencarian** produk berdasarkan nama atau penggalan nama.  
- 🧮 **Pemfilteran** produk berdasarkan jenis/kategori.  
- 📊 **Pengurutan** produk berdasarkan harga, popularitas, atau rating.  
- 🎞️ **Slider** menampilkan produk populer/diskon.  

🧾 **CRUD:**
| Operasi | Deskripsi | Akses |
|----------|------------|--------|
| **Read** | Menampilkan data produk di homepage | Guest, User, Admin |
| **Create** | Menambahkan slider promosi atau diskon produk | Admin |
| **Update** | Mengubah produk di dalam slider | Admin |
| **Delete** | Menghapus konten slider dan produk di homepage | Admin |

---

### 🧭 **Dashboard Product**

🧠 **Deskripsi:**  
Modul ini menyediakan fitur **CRUD (Create, Read, Update, Delete)** terhadap data produk yang dijual di **Prime Basket Place**.  
Objek yang diolah adalah **produk perlengkapan basket**.  
Setiap user yang berjualan hanya bisa mengelola produk miliknya sendiri karena data difilter berdasarkan *foreign key* yang merujuk ke *primary key* user.  

⚙️ **Fitur Utama:**  
- Menambah produk baru untuk dijual.  
- Melihat daftar produk milik sendiri.  
- Mengedit detail produk.  
- Menghapus produk yang tidak lagi dijual.  

🔒 **Akses Pengguna:**  
- **User:** CRUD penuh hanya untuk produk milik sendiri.  
- **Admin:** Hanya **Read** dan **Delete** tanpa filter.  
- **Guest:** Tidak dapat mengakses, akan diarahkan ke halaman login.  

🧾 **CRUD:**
| Operasi | Deskripsi | Akses |
|----------|------------|--------|
| **Create** | Menambahkan produk baru | User |
| **Read** | Melihat daftar produk | User, Admin |
| **Update** | Mengubah detail produk | User |
| **Delete** | Menghapus produk | User, Admin |

---

### ⭐ **Review Product**

🧠 **Deskripsi:**  
Modul ini memungkinkan pengguna memberikan **ulasan (review)** terhadap produk di **Prime Basket Place**.  
Setiap review dapat berisi **rating bintang (1–5)**, **komentar**, dan **foto produk** (opsional).  
Hanya pengguna terdaftar yang bisa menulis review.  

⚙️ **Fitur Utama:**  
- Memberikan **penilaian** dan **komentar**.  
- Menampilkan **review** pengguna lain pada halaman produk.  
- Upload foto opsional sebagai bukti/ilustrasi produk.  

🔒 **Akses Pengguna:**  
- **User:** Dapat menulis review setelah login.  
- **Guest:** Harus login terlebih dahulu.  
- **Admin:** Tidak dapat membuat review.  

🧾 **CRUD:**
| Operasi | Deskripsi | Akses |
|----------|------------|--------|
| **Create** | Menulis review baru | User |
| **Read** | Melihat semua review produk | Semua |
| **Update** | Mengubah review milik sendiri | User |
| **Delete** | Menghapus review milik sendiri | User |

---

### 🧾 **Detail Product**

🧠 **Deskripsi:**  
Modul ini memuat informasi detail mengenai suatu produk basket.  
Terdapat fitur **masukkan keranjang** dan **love button** untuk menandai produk favorit.  
Selain itu, template dari **Review App** ditampilkan di bagian bawah halaman detail produk.  

⚙️ **Fitur Utama:**  
- Menampilkan detail lengkap produk.  
- Tombol **Add to Cart** dan **Love/Favorite**.  
- Menampilkan review dari pengguna.  

🧾 **CRUD:**
| Operasi | Deskripsi | Akses |
|----------|------------|--------|
| **Read** | Menampilkan detail produk | Semua |
| **Create** | Membuat detail baru dari produk | User |
| **Update** | Memperbarui detail produk | User |
| **Delete** | Menghapus detail produk | User |

---

### ❤️ **Favourite**

🧠 **Deskripsi:**  
Modul Favourite memungkinkan pengguna untuk menandai produk basket yang mereka sukai agar mudah ditemukan dan diakses kembali di kemudian hari.
Fitur ini membantu pengguna menyimpan daftar produk favorit. Seperti sepatu, bola, atau jersey,
yang mungkin ingin mereka beli nanti tanpa perlu mencarinya ulang.

⚙️ **Fitur Utama:**  
- Menandai atau menghapus tanda favorit pada produk.
- Melihat daftar produk yang telah ditandai sebagai favorit.
- Mengakses langsung halaman detail produk dari daftar favorit.
- Admin dapat menghapus favorit pengguna yang dianggap tidak relevan atau melanggar kebijakan platform.

🔒 **Akses Pengguna:**  
- **User:** CRUD penuh terhadap daftar favorit dan catatan pribadinya sendiri.  
- **Admin:** Dapat melihat dan menghapus daftar favorit pengguna untuk keperluan moderasi.
- **Guest:** Tidak dapat menandai produk, akan diarahkan ke halaman login.

🧾 **CRUD:**
| Operasi | Deskripsi | Akses |
|----------|------------|--------|
| **Read** | Melihat daftar produk favorit | User, Admin |
| **Create** | Menandai produk sebagai favorit | User |
| **Update** | Mengubah catatan pribadi (notes) pada produk favorit | User |
| **Delete** | Menghapus produk dari daftar favorit | User, Admin |

---

## 👥 **Role Pengguna Aplikasi**

| Role | Deskripsi |
|------|------------|
| 🕶️ **Guest** | Pengguna yang mengakses web **Prime Basket Place** tanpa autentikasi. |
| 🧍‍♂️ **User** | Pengguna yang dapat **menjual** dan **membeli** barang di **Prime Basket Place**. |
| 🧑‍💼 **Admin** | Pengguna yang dapat melakukan **manipulasi (delete)** terhadap *barang* yang tidak valid. |    

---

## Link Sumber Dataset

| Brand | Link |
|--------|------|
| 🏆 **Nike** | [https://www.nike.com/id/w/basketball-clothing](https://www.nike.com/id/w/basketball-clothing) |
| ⭐ **Adidas** | [https://www.adidas.co.id/en/Sports/basketball/clothing.html](https://www.adidas.co.id/en/Sports/basketball/clothing.html) |
| 💪 **Decathlon** | [https://www.decathlon.co.id/en-ID/c/team-sports/basketball/basketball-clothings.html](https://www.decathlon.co.id/en-ID/c/team-sports/basketball/basketball-clothings.html) |

---

## Link PWS
https://pbp.cs.ui.ac.id/rafsanjani41/primebasketplace

---

## Link Figma
https://www.figma.com/site/qtWBlM8sUzHF4jFFDC0jvx/PBP---Prime-Basket-Place?node-id=0-1&t=1CQRrw6bq1zIiLDh-1&view=settings
