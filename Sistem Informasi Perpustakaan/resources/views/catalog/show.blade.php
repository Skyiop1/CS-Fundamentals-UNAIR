@extends('layouts.member')

@section('title', 'Detail Buku - ' . $book->title)

@section('content')
    <div class="row justify-content-center">
        <div class="col-12 col-lg-10">
            <div class="card app-card shadow-sm border-0">
                <div class="card-header bg-white py-3 border-bottom d-flex justify-content-between align-items-center">
                    <h5 class="card-title mb-0 fw-bold text-dark">Informasi Detail Buku</h5>
                    <a href="{{ route('catalog.index') }}" class="btn btn-sm btn-outline-secondary">Kembali ke Katalog</a>
                </div>
                <div class="card-body p-4">
                    <div class="row g-4">
                        <!-- Sisi Kiri: Cover Buku -->
                        <div class="col-12 col-md-4 text-center">
                            @if ($book->cover_image)
                                <img src="{{ asset('storage/' . $book->cover_image) }}" alt="Cover {{ $book->title }}" class="img-fluid rounded border shadow-sm mx-auto" style="max-height: 380px; object-fit: cover;">
                            @else
                                <div class="bg-light rounded text-secondary d-flex flex-column align-items-center justify-content-center mx-auto shadow-sm border" style="width: 220px; height: 300px;">
                                    <span class="fw-bold">TIDAK ADA COVER</span>
                                </div>
                            @endif
                        </div>

                        <!-- Sisi Kanan: Spesifikasi Buku -->
                        <div class="col-12 col-md-8">
                            <h3 class="fw-bold text-dark mb-1">{{ $book->title }}</h3>
                            <p class="text-secondary mb-3">oleh <span class="fw-semibold text-dark">{{ $book->author }}</span></p>

                            <hr>

                            <table class="table table-borderless align-middle my-3">
                                <tbody>
                                    <tr>
                                        <th style="width: 150px;" class="text-secondary fw-semibold py-1.5">Kategori</th>
                                        <td class="py-1.5"><span class="badge bg-light text-dark border">{{ $book->category->name }}</span></td>
                                    </tr>
                                    <tr>
                                        <th class="text-secondary fw-semibold py-1.5">Kode Buku</th>
                                        <td class="py-1.5"><code>{{ $book->book_code }}</code></td>
                                    </tr>
                                    <tr>
                                        <th class="text-secondary fw-semibold py-1.5">Penerbit</th>
                                        <td class="py-1.5">{{ $book->publisher ?: '-' }}</td>
                                    </tr>
                                    <tr>
                                        <th class="text-secondary fw-semibold py-1.5">Tahun Terbit</th>
                                        <td class="py-1.5">{{ $book->publication_year ?: '-' }}</td>
                                    </tr>
                                    <tr>
                                        <th class="text-secondary fw-semibold py-1.5">Stok Perpustakaan</th>
                                        <td class="py-1.5">
                                            @if ($book->stock > 0)
                                                <span class="badge bg-success-subtle text-success rounded-pill px-2.5">{{ $book->stock }} eksemplar</span>
                                            @else
                                                <span class="badge bg-danger-subtle text-danger rounded-pill px-2.5">Stok Habis</span>
                                            @endif
                                        </td>
                                    </tr>
                                </tbody>
                            </table>

                            <hr>

                            <div class="my-4">
                                <h6 class="fw-bold text-dark mb-2">Sinopsis / Ringkasan Buku:</h6>
                                <p class="text-secondary" style="line-height: 1.6; text-align: justify;">
                                    {!! nl2br(e($book->description ?: 'Tidak ada sinopsis atau deskripsi untuk buku ini.')) !!}
                                </p>
                            </div>

                            <hr>

                            <!-- Sektor Pemesanan / Peminjaman -->
                            <div class="mt-4">
                                @if ($hasActiveBorrowing)
                                    <div class="alert alert-warning border-0 shadow-sm d-flex align-items-center gap-2 mb-0" role="alert">
                                        <div>
                                            Anda sedang <strong>mengajukan atau aktif meminjam</strong> buku ini saat ini. Silakan periksa di menu <a href="{{ route('borrowings.mine') }}" class="alert-link">Peminjaman Saya</a>.
                                        </div>
                                    </div>
                                @elseif ($book->stock <= 0)
                                    <button class="btn btn-secondary w-100 py-2.5 fw-bold" disabled>
                                        Stok Tidak Tersedia (Habis)
                                    </button>
                                @else
                                    <form action="{{ route('borrowings.request', $book) }}" method="POST">
                                        @csrf
                                        <button type="submit" class="btn btn-primary w-100 py-2.5 fw-bold" onclick="return confirm('Apakah Anda yakin ingin mengajukan peminjaman untuk buku ini?');">
                                            Ajukan Peminjaman Buku
                                        </button>
                                    </form>
                                @endif
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
@endsection
