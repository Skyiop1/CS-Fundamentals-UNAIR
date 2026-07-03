<?php

namespace Database\Seeders;

use App\Models\Book;
use App\Models\Category;
use App\Models\Member;
use App\Models\Role;
use App\Models\User;
use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $adminRole = Role::updateOrCreate(
            ['name' => 'admin'],
            ['description' => 'Petugas perpustakaan yang mengelola data dan transaksi.']
        );

        $anggotaRole = Role::updateOrCreate(
            ['name' => 'anggota'],
            ['description' => 'Anggota perpustakaan yang dapat meminjam buku.']
        );

        User::updateOrCreate(
            ['email' => 'admin@perpus.test'],
            [
                'role_id' => $adminRole->id,
                'name' => 'Admin Perpustakaan',
                'password' => Hash::make('password'),
                'phone' => '081200000001',
                'address' => 'Ruang Perpustakaan',
                'status' => 'active',
            ]
        );

        $anggotaUser = User::updateOrCreate(
            ['email' => 'anggota@perpus.test'],
            [
                'role_id' => $anggotaRole->id,
                'name' => 'Anggota Demo',
                'password' => Hash::make('password'),
                'phone' => '081200000002',
                'address' => 'Jl. Pendidikan No. 10',
                'status' => 'active',
            ]
        );

        Member::updateOrCreate(
            ['user_id' => $anggotaUser->id],
            [
                'member_number' => 'AGT-2026-0001',
                'name' => $anggotaUser->name,
                'phone' => $anggotaUser->phone,
                'address' => $anggotaUser->address,
                'status' => 'active',
            ]
        );

        $categories = [
            'Teknologi Informasi' => 'Buku tentang komputer, pemrograman, dan sistem informasi.',
            'Manajemen' => 'Buku tentang organisasi, administrasi, dan pengelolaan.',
            'Pendidikan' => 'Buku tentang metode pembelajaran dan pengembangan akademik.',
            'Sastra' => 'Koleksi buku sastra Indonesia dan dunia.',
            'Pengembangan Diri' => 'Buku tentang motivasi, kebiasaan baik, dan pengembangan potensi diri.',
        ];

        foreach ($categories as $name => $description) {
            Category::updateOrCreate(
                ['name' => $name],
                ['description' => $description]
            );
        }

        $books = [
            [
                'category' => 'Teknologi Informasi',
                'book_code' => 'BK-TI-001',
                'title' => 'Pengantar Sistem Informasi',
                'author' => 'George M. Marakas, James A. O\'Brien',
                'publisher' => 'Penerbit Salemba Empat',
                'publication_year' => 2017,
                'stock' => 5,
                'description' => 'Buku Pengantar Sistem Informasi (Introduction to Information Systems) Edisi 16 Buku 1.',
                'cover_image' => 'images/covers/pengantar_sistem_informasi.jpg',
            ],
            [
                'category' => 'Teknologi Informasi',
                'book_code' => 'BK-TI-002',
                'title' => 'Pemrograman Web dengan Laravel',
                'author' => 'Budi Raharjo',
                'publisher' => 'Informatika',
                'publication_year' => 2022,
                'stock' => 4,
                'description' => 'Panduan membangun aplikasi web menggunakan framework Laravel.',
                'cover_image' => 'https://images.tokopedia.net/img/cache/700/VqbcmM/2022/9/27/b16e885b-e4a8-4bb3-a0e2-89596c342d76.jpg',
            ],
            [
                'category' => 'Manajemen',
                'book_code' => 'BK-MJ-001',
                'title' => 'Pengantar Manajemen',
                'author' => 'Malayu S.P. Hasibuan',
                'publisher' => 'Bumi Aksara',
                'publication_year' => 2019,
                'stock' => 6,
                'description' => 'Buku pengantar tentang fungsi dan proses manajemen.',
                'cover_image' => 'https://images.tokopedia.net/img/cache/700/VqbcmM/2021/3/9/b1236183-b541-45a1-ae40-2bdf613d0779.jpg',
            ],
            [
                'category' => 'Pendidikan',
                'book_code' => 'BK-PD-001',
                'title' => 'Strategi Pembelajaran',
                'author' => 'Wina Sanjaya',
                'publisher' => 'Kencana',
                'publication_year' => 2021,
                'stock' => 3,
                'description' => 'Referensi strategi pembelajaran untuk lingkungan akademik.',
                'cover_image' => 'https://images.tokopedia.net/img/cache/700/VqbcmM/2020/8/16/d2cb401e-de8c-4f7f-a9cb-bb3522a49f57.jpg',
            ],
            [
                'category' => 'Sastra',
                'book_code' => 'BK-ST-001',
                'title' => 'Laskar Pelangi',
                'author' => 'Andrea Hirata',
                'publisher' => 'Bentang Pustaka',
                'publication_year' => 2005,
                'stock' => 7,
                'description' => 'Novel Indonesia tentang perjuangan pendidikan dan persahabatan.',
                'cover_image' => 'images/covers/laskar_pelangi.jpg',
            ],
            [
                'category' => 'Pengembangan Diri',
                'book_code' => 'BK-SD-001',
                'title' => 'Atomic Habits',
                'author' => 'James Clear',
                'publisher' => 'Gramedia Pustaka Utama',
                'publication_year' => 2019,
                'stock' => 8,
                'description' => 'Perubahan kecil yang memberikan hasil luar biasa. Cara mudah dan terbukti untuk membentuk kebiasaan baik dan menghilangkan kebiasaan buruk.',
                'cover_image' => 'images/covers/atomic_habits.jpg',
            ],
        ];

        foreach ($books as $book) {
            $category = Category::where('name', $book['category'])->first();

            Book::updateOrCreate(
                ['book_code' => $book['book_code']],
                [
                    'category_id' => $category->id,
                    'title' => $book['title'],
                    'author' => $book['author'],
                    'publisher' => $book['publisher'],
                    'publication_year' => $book['publication_year'],
                    'stock' => $book['stock'],
                    'description' => $book['description'],
                    'cover_image' => $book['cover_image'],
                ]
            );
        }
    }
}
