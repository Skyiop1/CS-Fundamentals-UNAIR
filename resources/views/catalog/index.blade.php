@extends('layouts.member')

@section('title', 'Katalog Buku')

@section('content')
    <div class="mb-5 text-center text-md-start">
        <h1 class="h2 fw-extrabold mb-1 tracking-tight text-dark">Katalog Buku Perpustakaan</h1>
        <p class="text-secondary mb-0">Temukan dan pinjam koleksi buku akademik, sastra, dan teknologi terbaik.</p>
    </div>

    <!-- Spotlight Search -->
    <div class="card app-card border-0 mb-4 bg-white shadow-sm overflow-hidden" style="border-radius: 20px;">
        <div class="card-body p-2">
            <form action="{{ route('catalog.index') }}" method="GET" class="row g-2 align-items-center">
                @if(request('category_id'))
                    <input type="hidden" name="category_id" value="{{ request('category_id') }}">
                @endif
                <div class="col-12 col-md-9 col-lg-10">
                    <div class="input-group border-0">
                        <span class="input-group-text bg-transparent border-0 text-muted ps-3">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-search" viewBox="0 0 16 16">
                              <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
                            </svg>
                        </span>
                        <input type="text" name="search" class="form-control border-0 ps-2 fs-5 py-2 shadow-none" placeholder="Cari buku berdasarkan judul, penulis, kode..." value="{{ request('search') }}">
                    </div>
                </div>
                <div class="col-12 col-md-3 col-lg-2 d-flex gap-2 pe-md-2">
                    <button type="submit" class="btn btn-primary w-100 rounded-pill py-2.5 shadow-sm">Cari Buku</button>
                </div>
            </form>
        </div>
    </div>

    <!-- Bubble Category Filters -->
    <div class="d-flex flex-wrap gap-2 mb-5 align-items-center justify-content-center justify-content-md-start">
        <span class="text-muted me-2 small fw-bold text-uppercase tracking-wider">Kategori:</span>
        <a href="{{ route('catalog.index', ['search' => request('search')]) }}" class="btn btn-sm rounded-pill px-3 py-1.5 {{ !request('category_id') ? 'btn-primary rounded-pill' : 'btn-light border' }}">
            Semua
        </a>
        @foreach ($categories as $category)
            <a href="{{ route('catalog.index', ['category_id' => $category->id, 'search' => request('search')]) }}" class="btn btn-sm rounded-pill px-3 py-1.5 {{ request('category_id') == $category->id ? 'btn-primary rounded-pill' : 'btn-light border' }}">
                {{ $category->name }}
            </a>
        @endforeach
    </div>

    <!-- Grid Buku -->
    <div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4 mb-5">
        @forelse ($books as $book)
            <div class="col">
                <div class="card app-card border-0 h-100 d-flex flex-column" style="border-radius: 20px; overflow: hidden; background: #fff;">
                    <!-- Preview Cover Container -->
                    <div class="p-4 text-center border-bottom d-flex align-items-center justify-content-center position-relative" style="height: 240px; background: radial-gradient(circle, #f8fafc 0%, #e2e8f0 100%);">
                        <span class="position-absolute top-3 start-3 badge rounded-pill bg-white text-secondary border px-2.5 py-1.5 shadow-sm small">
                            {{ $book->category->name }}
                        </span>
                        <div class="book-cover-wrapper">
                            @if ($book->cover_image)
                                <img src="{{ filter_var($book->cover_image, FILTER_VALIDATE_URL) ? $book->cover_image : asset('storage/' . $book->cover_image) }}" 
                                     alt="Cover {{ $book->title }}" 
                                     class="img-fluid book-3d-shadow" 
                                     style="max-height: 180px; width: 120px; object-fit: cover;">
                            @else
                                <div class="bg-white text-secondary d-flex flex-column align-items-center justify-content-center shadow-sm border book-3d-shadow" style="width: 120px; height: 170px;">
                                    <span class="fw-bold small text-uppercase tracking-wider text-muted text-center px-2">No Cover</span>
                                </div>
                            @endif
                        </div>
                    </div>

                    <!-- Informasi Buku -->
                    <div class="card-body d-flex flex-column flex-fill p-4">
                        <h5 class="fw-bold text-dark mb-1 text-truncate-2" style="height: 48px; line-height: 1.3; font-size: 1.1rem;">
                            {{ $book->title }}
                        </h5>
                        <p class="text-muted small mb-4">oleh <span class="fw-semibold text-dark">{{ $book->author }}</span></p>

                        <div class="mt-auto d-flex justify-content-between align-items-center pt-3 border-top">
                            @if ($book->stock > 0)
                                <span class="badge bg-success-subtle text-success rounded-pill px-3 py-1.5 border border-success-subtle">
                                    Stok: {{ $book->stock }}
                                </span>
                            @else
                                <span class="badge bg-danger-subtle text-danger rounded-pill px-3 py-1.5 border border-danger-subtle">
                                    Stok Habis
                                </span>
                            @endif
                            <a href="{{ route('catalog.show', $book) }}" class="btn btn-sm btn-light border rounded-pill px-3.5 py-2 font-semibold">
                                Detail
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
