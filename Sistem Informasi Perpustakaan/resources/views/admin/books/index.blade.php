@extends('layouts.admin')

@section('title', 'Kelola Buku')
@section('page_title', 'Kelola Data Buku')

@section('content')
    <div class="card app-card shadow-sm border-0 mb-4">
        <div class="card-body">
            <form action="{{ route('admin.books.index') }}" method="GET" class="row g-3">
                <div class="col-12 col-md-5">
                    <div class="input-group">
                        <span class="input-group-text bg-transparent text-secondary border-end-0">
                            <i class="bi bi-search"></i>
                        </span>
                        <input type="text" name="search" class="form-control border-start-0 ps-0" placeholder="Cari judul, pengarang, atau kode buku..." value="{{ request('search') }}">
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
                <div class="col-12 col-md-4 d-flex gap-2">
                    <button type="submit" class="btn btn-primary flex-fill">Cari</button>
                    @if (request()->filled('search') || request()->filled('category_id'))
                        <a href="{{ route('admin.books.index') }}" class="btn btn-outline-secondary">Reset</a>
                    @endif
                    <a href="{{ route('admin.books.create') }}" class="btn btn-success flex-fill">
                        + Tambah Buku
                    </a>
                </div>
            </form>
        </div>
    </div>

    <div class="card app-card shadow-sm border-0">
        <div class="table-responsive">
            <table class="table align-middle mb-0 table-hover">
                <thead class="table-light text-secondary">
                    <tr>
                        <th style="width: 80px;" class="text-center">Cover</th>
                        <th style="width: 120px;">Kode Buku</th>
                        <th>Judul & Pengarang</th>
                        <th>Kategori</th>
                        <th>Penerbit / Tahun</th>
                        <th style="width: 100px;" class="text-center">Stok</th>
                        <th style="width: 200px;" class="text-center">Aksi</th>
                    </tr>
                </thead>
                <tbody>
                    @forelse ($books as $book)
                        <tr>
                            <td class="text-center">
                                @if ($book->cover_image)
                                    <img src="{{ asset('storage/' . $book->cover_image) }}" alt="Cover {{ $book->title }}" class="rounded shadow-sm" style="width: 48px; height: 64px; object-fit: cover;">
                                @else
                                    <div class="bg-light rounded text-secondary d-flex align-items-center justify-content-center mx-auto shadow-sm" style="width: 48px; height: 64px; font-size: 10px; font-weight: bold; border: 1px solid var(--app-border);">
                                        NO COV
                                    </div>
                                @endif
                            </td>
                            <td>
                                <code class="text-dark fw-semibold">{{ $book->book_code }}</code>
                            </td>
                            <td>
                                <div class="fw-bold text-dark">{{ $book->title }}</div>
                                <div class="text-secondary small">oleh {{ $book->author }}</div>
                            </td>
                            <td>
                                <span class="badge bg-light text-dark border">{{ $book->category->name }}</span>
                            </td>
                            <td>
                                <div class="small">{{ $book->publisher ?: '-' }}</div>
                                <div class="text-secondary small">{{ $book->publication_year ?: '-' }}</div>
                            </td>
                            <td class="text-center">
                                @if ($book->stock > 0)
                                    <span class="badge bg-success-subtle text-success rounded-pill px-2.5">{{ $book->stock }} eks</span>
                                @else
                                    <span class="badge bg-danger-subtle text-danger rounded-pill px-2.5">Habis</span>
                                @endif
                            </td>
                            <td class="text-center">
                                <div class="d-flex justify-content-center gap-2">
                                    <a href="{{ route('admin.books.show', $book) }}" class="btn btn-sm btn-outline-info">
                                        Detail
                                    </a>
                                    <a href="{{ route('admin.books.edit', $book) }}" class="btn btn-sm btn-outline-primary">
                                        Edit
                                    </a>
                                    <form action="{{ route('admin.books.destroy', $book) }}" method="POST" onsubmit="return confirm('Apakah Anda yakin ingin menghapus buku ini?');">
                                        @csrf
                                        @method('DELETE')
                                        <button type="submit" class="btn btn-sm btn-outline-danger">
                                            Hapus
                                        </button>
                                    </form>
                                </div>
                            </td>
                        </tr>
                    @empty
                        <tr>
                            <td colspan="7" class="text-center text-secondary py-5">
                                Belum ada data buku yang sesuai.
                            </td>
                        </tr>
                    @endforelse
                </tbody>
            </table>
        </div>
        @if ($books->hasPages())
            <div class="card-footer bg-white py-3">
                {{ $books->links('pagination::bootstrap-5') }}
            </div>
        @endif
    </div>
@endsection
