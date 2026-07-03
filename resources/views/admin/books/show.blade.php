@extends('layouts.admin')

@section('title', 'Detail Buku')
@section('page_title', 'Detail Informasi Buku')

@section('content')
    <div class="row justify-content-center">
        <div class="col-12 col-lg-10">
            <div class="card app-card shadow-sm border-0">
                <div class="card-header bg-white py-3 border-bottom d-flex justify-content-between align-items-center">
                    <h5 class="card-title mb-0 fw-bold text-dark">Detail Buku: {{ $book->book_code }}</h5>
                    <div class="d-flex gap-2">
                        <a href="{{ route('admin.books.edit', $book) }}" class="btn btn-sm btn-primary">Edit Buku</a>
                        <a href="{{ route('admin.books.index') }}" class="btn btn-sm btn-outline-secondary">Kembali</a>
                    </div>
                </div>
                <div class="card-body p-4">
                    <div class="row g-4">
                        <!-- Sisi Kiri: Gambar Cover -->
                        <div class="col-12 col-md-4 text-center">
                            @if ($book->cover_image)
                                <img src="{{ asset('storage/' . $book->cover_image) }}" alt="Cover {{ $book->title }}" class="img-fluid rounded border shadow-sm" style="max-height: 380px; object-fit: cover;">
                            @else
                                <div class="bg-light rounded text-secondary d-flex flex-column align-items-center justify-content-center mx-auto shadow-sm border" style="width: 220px; height: 300px;">
                                    <i class="bi bi-book fs-1 mb-2"></i>
                                    <span class="fw-bold">TIDAK ADA COVER</span>
                                </div>
                            @endif
                        </div>

                        <!-- Sisi Kanan: Detail Informasi -->
                        <div class="col-12 col-md-8">
                            <h3 class="fw-bold text-dark mb-1">{{ $book->title }}</h3>
                            <p class="text-secondary mb-3">oleh <span class="fw-semibold text-dark">{{ $book->author }}</span></p>

                            <hr>

                            <table class="table table-borderless align-middle my-3">
                                <tbody>
                                    <tr>
                                        <th style="width: 150px;" class="text-secondary fw-semibold py-2">Kategori</th>
                                        <td class="py-2"><span class="badge bg-light text-dark border">{{ $book->category->name }}</span></td>
                                    </tr>
                                    <tr>
                                        <th class="text-secondary fw-semibold py-2">Kode Buku</th>
                                        <td class="py-2"><code>{{ $book->book_code }}</code></td>
                                    </tr>
                                    <tr>
                                        <th class="text-secondary fw-semibold py-2">Penerbit</th>
                                        <td class="py-2">{{ $book->publisher ?: '-' }}</td>
                                    </tr>
                                    <tr>
                                        <th class="text-secondary fw-semibold py-2">Tahun Terbit</th>
                                        <td class="py-2">{{ $book->publication_year ?: '-' }}</td>
                                    </tr>
                                    <tr>
                                        <th class="text-secondary fw-semibold py-2">Stok Tersedia</th>
                                        <td class="py-2">
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

                            <div class="mt-4">
                                <h6 class="fw-bold text-dark mb-2">Sinopsis / Deskripsi:</h6>
                                <p class="text-secondary" style="line-height: 1.6; text-align: justify;">
                                    {!! nl2br(e($book->description ?: 'Tidak ada deskripsi untuk buku ini.')) !!}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
@endsection
