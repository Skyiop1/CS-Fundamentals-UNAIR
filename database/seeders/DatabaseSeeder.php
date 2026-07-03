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
            'Sastra' => 'Koleksi buku sastra Indonesia dan dunia.',
            'Pengembangan Diri' => 'Buku tentang motivasi, kebiasaan baik, dan pengembangan potensi diri.',
        ];

        foreach ($categories as $name => $description) {
            Category::updateOrCreate(
                ['name' => $name],
                ['description' => $description]
            );
        }

        // Hapus buku yang tidak punya cover lokal
        Book::whereIn('book_code', ['BK-TI-002', 'BK-MJ-001', 'BK-PD-001'])->delete();

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
                'category' => 'Sastra',
                'book_code' => 'BK-ST-002',
                'title' => 'Bumi',
                'author' => 'Tere Liye',
                'publisher' => 'Gramedia Pustaka Utama',
                'publication_year' => 2014,
                'stock' => 5,
                'description' => 'Novel fantasi tentang petualangan Raib, gadis berusia 15 tahun yang memiliki kekuatan misterius. Buku pertama dari serial Bumi karya Tere Liye.',
                'cover_image' => 'images/covers/bumi.jpg',
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
