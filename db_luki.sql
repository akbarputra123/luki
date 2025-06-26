-- 1. Tabel User
CREATE TABLE User_Tabel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL,
    nama_lengkap VARCHAR(100),
    tanggal_lahir DATE
);

-- 2. Tabel Gejala
CREATE TABLE Gejala_Tabel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_gejala VARCHAR(10) NOT NULL UNIQUE,
    nama_gejala VARCHAR(100) NOT NULL,
    deskripsi TEXT,
    kategori VARCHAR(50)
);

-- 3. Tabel Penyakit / Hama
CREATE TABLE Penyakit_Tabel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kode_penyakit VARCHAR(10) NOT NULL UNIQUE,
    nama_penyakit VARCHAR(100) NOT NULL,
    deskripsi TEXT,
    solusi TEXT
);

-- 4. Tabel Aturan (Basis Pengetahuan + CF)
CREATE TABLE Aturan_Tabel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    penyakit_id INT NOT NULL,
    gejala_id INT NOT NULL,
    mb FLOAT NOT NULL,
    md FLOAT NOT NULL,
    FOREIGN KEY (penyakit_id) REFERENCES Penyakit_Tabel(id) ON DELETE CASCADE,
    FOREIGN KEY (gejala_id) REFERENCES Gejala_Tabel(id) ON DELETE CASCADE
);

-- 5. Tabel Hasil Diagnosa
CREATE TABLE HasilDiagnosa_Tabel (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    penyakit_id INT NOT NULL,
    nilai_cf FLOAT NOT NULL,
    tanggal_diagnosa DATETIME DEFAULT CURRENT_TIMESTAMP,
    gejala_terpilih TEXT,
    FOREIGN KEY (user_id) REFERENCES User_Tabel(id) ON DELETE CASCADE,
    FOREIGN KEY (penyakit_id) REFERENCES Penyakit_Tabel(id) ON DELETE CASCADE
);
