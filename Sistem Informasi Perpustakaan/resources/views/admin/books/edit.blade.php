@extends('layouts.admin')

@section('title', 'Edit Buku')
@section('page_title', 'Edit Buku')

@section('content')
    <div class="row justify-content-center">
        <div class="col-12 col-lg-10">
            <div class="card app-card shadow-sm border-0">
                <div class="card-header bg-white py-3 border-bottom d-flex justify-content-between align-items-center">
                    <h5 class="card-title mb-0 fw-bold text-dark">Form Edit Buku</h5>
                    <a href="{{ route('admin.books.index') }}" class="btn btn-sm btn-outline-secondary">Kembali</a>
                </div>
                <div class="card-body p-4">
                    <form action="{{ route('admin.books.update', $book) }}" method="POST" enctype="multipart/form-data">
                        @csrf
                        @method('PUT')
                        <div class="row g-3 mb-4">
                            <!-- Kode Buku -->
                            <div class="col-12 col-md-6">
                                <label for="book_code" class="form-label small fw-semibold text-secondary">Kode Buku <span class="text-danger">*</span></label>
                                <input type="text" class="form-control @error('book_code') is-invalid @enderror" id="book_code" name="book_code" value="{{ old('book_code', $book->book_code) }}" required>
                                @error('book_code')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>

                            <!-- Kategori -->
                            <div class="col-12 col-md-6">
                                <label for="category_id" class="form-label small fw-semibold text-secondary">Kategori <span class="text-danger">*</span></label>
                                <select class="form-select @error('category_id') is-invalid @enderror" id="category_id" name="category_id" required>
                                    @foreach ($categories as $category)
                                        <option value="{{ $category->id }}" {{ old('category_id', $book->category_id) == $category->id ? 'selected' : '' }}>
                                            {{ $category->name }}
                                        </option>
                                    @endforeach
                                </select>
                                @error('category_id')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>

                            <!-- Judul Buku -->
                            <div class="col-12">
                                <label for="title" class="form-label small fw-semibold text-secondary">Judul Buku <span class="text-danger">*</span></label>
                                <input type="text" class="form-control @error('title') is-invalid @enderror" id="title" name="title" value="{{ old('title', $book->title) }}" required>
                                @error('title')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>

                            <!-- Pengarang -->
                            <div class="col-12 col-md-6">
                                <label for="author" class="form-label small fw-semibold text-secondary">Nama Pengarang <span class="text-danger">*</span></label>
                                <input type="text" class="form-control @error('author') is-invalid @enderror" id="author" name="author" value="{{ old('author', $book->author) }}" required>
                                @error('author')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>

                            <!-- Penerbit -->
                            <div class="col-12 col-md-6">
                                <label for="publisher" class="form-label small fw-semibold text-secondary">Penerbit</label>
                                <input type="text" class="form-control @error('publisher') is-invalid @enderror" id="publisher" name="publisher" value="{{ old('publisher', $book->publisher) }}">
                                @error('publisher')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>

                            <!-- Tahun Terbit -->
                            <div class="col-12 col-md-6">
                                <label for="publication_year" class="form-label small fw-semibold text-secondary">Tahun Terbit</label>
                                <input type="number" class="form-control @error('publication_year') is-invalid @enderror" id="publication_year" name="publication_year" value="{{ old('publication_year', $book->publication_year) }}">
                                @error('publication_year')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>

                            <!-- Stok -->
                            <div class="col-12 col-md-6">
                                <label for="stock" class="form-label small fw-semibold text-secondary">Jumlah Stok <span class="text-danger">*</span></label>
                                <input type="number" class="form-control @error('stock') is-invalid @enderror" id="stock" name="stock" value="{{ old('stock', $book->stock) }}" min="0" required>
                                @error('stock')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>

                            <!-- Gambar Cover -->
                            <div class="col-12">
                                <label for="cover_image" class="form-label small fw-semibold text-secondary">Gambar Cover (Biarkan kosong jika tidak diubah)</label>
                                <div class="d-flex align-items-start gap-3 mb-2">
                                    @if ($book->cover_image)
                                        <div>
                                            <div class="small text-secondary mb-1">Cover Saat Ini:</div>
                                            <img src="{{ asset('storage/' . $book->cover_image) }}" alt="Cover {{ $book->title }}" class="rounded border shadow-sm" style="width: 80px; height: 110px; object-fit: cover;">
                                        </div>
                                    @endif
                                    <div class="flex-fill">
                                        <input type="file" class="form-control @error('cover_image') is-invalid @enderror" id="cover_image" name="cover_image" accept="image/*">
                                        <small class="text-muted">Maksimal 2MB. Format: jpeg, png, jpg, webp.</small>
                                        @error('cover_image')
                                            <div class="invalid-feedback d-block">{{ $message }}</div>
                                        @enderror
                                    </div>
                                </div>
                            </div>

                            <!-- Deskripsi -->
                            <div class="col-12">
                                <label for="description" class="form-label small fw-semibold text-secondary">Sinopsis / Deskripsi Buku</label>
                                <textarea class="form-control @error('description') is-invalid @enderror" id="description" name="description" rows="5">{{ old('description', $book->description) }}</textarea>
                                @error('description')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                        </div>

                        <div class="d-flex gap-3">
                            <button type="submit" class="btn btn-primary px-4 py-2">
                                Simpan Perubahan
                            </button>
                            <a href="{{ route('admin.books.index') }}" class="btn btn-outline-secondary px-4 py-2">
                                Batal
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
@endsection
