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
                'title' => 'Dasar-Dasar Sistem Informasi',
                'author' => 'Tata Sutabri',
                'publisher' => 'Andi Publisher',
                'publication_year' => 2020,
                'stock' => 5,
                'description' => 'Membahas konsep dasar sistem informasi dan penerapannya dalam organisasi.',
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
                    'cover_image' => null,
                ]
            );
        }
    }
}
