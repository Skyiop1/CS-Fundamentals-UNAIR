@extends('layouts.member')

@section('title', 'Katalog Buku')

@section('content')
    <div class="mb-4">
        <h1 class="h3 fw-bold mb-1">Katalog Buku Perpustakaan</h1>
        <p class="text-secondary mb-0">Temukan koleksi buku akademik, sastra, dan teknologi yang tersedia untuk dipinjam.</p>
    </div>

    <!-- Filter & Pencarian -->
    <div class="card app-card shadow-sm border-0 mb-4">
        <div class="card-body p-3">
            <form action="{{ route('catalog.index') }}" method="GET" class="row g-3">
                <div class="col-12 col-md-6">
                    <div class="input-group">
                        <span class="input-group-text bg-transparent text-secondary border-end-0">
                            <i class="bi bi-search"></i>
                        </span>
                        <input type="text" name="search" class="form-control border-start-0 ps-0" placeholder="Cari judul buku, nama pengarang, kode..." value="{{ request('search') }}">
                    </div>
                </div>
                <div class="col-12 col-md-3">
                    <select name="category_id" class="form-select">
                        <option value="">Semua Kategori</option>
                        @foreach ($categories as $category)
                            <option value="{{ $category->id }}" {{ request('category_id') == $category->id ? 'selected' : '' }}>
                                {{ $category->name }}
                            </option>
                        @endforeach
                    </select>
                </div>
                <div class="col-12 col-md-3 d-flex gap-2">
                    <button type="submit" class="btn btn-primary flex-fill">Cari</button>
                    @if (request()->filled('search') || request()->filled('category_id'))
                        <a href="{{ route('catalog.index') }}" class="btn btn-outline-secondary">Reset</a>
                    @endif
                </div>
            </form>
        </div>
    </div>

    <!-- Grid Buku -->
    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-4">
        @forelse ($books as $book)
            <div class="col">
                <div class="card app-card shadow-sm border-0 h-100 d-flex flex-column">
                    <!-- Preview Cover -->
                    <div class="bg-light text-center py-4 border-bottom position-relative" style="height: 200px; display: flex; align-items: center; justify-content: center;">
                        @if ($book->cover_image)
                            <img src="{{ asset('storage/' . $book->cover_image) }}" alt="Cover {{ $book->title }}" class="img-fluid shadow-sm" style="max-height: 180px; object-fit: cover;">
                        @else
                            <div class="text-secondary d-flex flex-column align-items-center justify-content-center">
                                <span class="fw-bold small text-uppercase tracking-wider">No Cover</span>
                            </div>
                        @endif
                        <span class="position-absolute top-2 end-2 badge bg-white text-dark border small shadow-sm">
                            {{ $book->category->name }}
                        </span>
                    </div>

                    <!-- Informasi Buku -->
                    <div class="card-body d-flex flex-column flex-fill p-3">
                        <h6 class="card-title fw-bold text-dark mb-1 text-truncate-2" style="height: 40px; line-height: 1.3;">
                            {{ $book->title }}
                        </h6>
                        <p class="text-secondary small mb-3">oleh <span class="fw-semibold">{{ $book->author }}</span></p>

                        <div class="mt-auto d-flex justify-content-between align-items-center">
                            @if ($book->stock > 0)
                                <span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill">
                                    Stok: {{ $book->stock }} eks
                                </span>
                            @else
                                <span class="badge bg-danger-subtle text-danger border border-danger-subtle rounded-pill">
                                    Stok Habis
                                </span>
                            @endif
                            <a href="{{ route('catalog.show', $book) }}" class="btn btn-sm btn-outline-primary px-3">
                                Lihat Detail
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        @empty
            <div class="col-12 text-center py-5">
                <div class="text-secondary">
                    <h5>Buku tidak ditemukan</h5>
                    <p class="small">Coba cari dengan kata kunci lain atau pilih kategori yang berbeda.</p>
                </div>
            </div>
        @endforelse
    </div>

    <!-- Pagination -->
    @if ($books->hasPages())
        <div class="d-flex justify-content-center">
            {{ $books->links('pagination::bootstrap-5') }}
        </div>
    @endif
@endsection
