@extends('layouts.admin')

@section('title', 'Daftar Peminjaman')
@section('page_title', 'Daftar Transaksi Peminjaman')

@section('content')
    <!-- Filter & Pencarian -->
    <div class="card app-card shadow-sm border-0 mb-4">
        <div class="card-body">
            <form action="{{ route('admin.borrowings.index') }}" method="GET" class="row g-3">
                <div class="col-12 col-md-5">
                    <div class="input-group">
                        <span class="input-group-text bg-transparent text-secondary border-end-0">
                            <i class="bi bi-search"></i>
                        </span>
                        <input type="text" name="search" class="form-control border-start-0 ps-0" placeholder="Cari nama atau nomor anggota..." value="{{ request('search') }}">
                    </div>
                </div>
                <div class="col-12 col-md-3">
                    <select name="status" class="form-select">
                        <option value="">Semua Status</option>
                        <option value="pending" {{ request('status') === 'pending' ? 'selected' : '' }}>Pending (Menunggu)</option>
                        <option value="approved" {{ request('status') === 'approved' ? 'selected' : '' }}>Approved (Disetujui)</option>
                        <option value="borrowed" {{ request('status') === 'borrowed' ? 'selected' : '' }}>Borrowed (Dipinjam)</option>
                        <option value="returned" {{ request('status') === 'returned' ? 'selected' : '' }}>Returned (Kembali)</option>
                        <option value="rejected" {{ request('status') === 'rejected' ? 'selected' : '' }}>Rejected (Ditolak)</option>
                        <option value="late" {{ request('status') === 'late' ? 'selected' : '' }}>Late (Terlambat)</option>
                    </select>
                </div>
                <div class="col-12 col-md-4 d-flex gap-2">
                    <button type="submit" class="btn btn-primary flex-fill">Cari</button>
                    @if (request()->filled('search') || request()->filled('status'))
                        <a href="{{ route('admin.borrowings.index') }}" class="btn btn-outline-secondary">Reset</a>
                    @endif
                </div>
            </form>
        </div>
    </div>

    <!-- Tabel Data Peminjaman -->
    <div class="card app-card shadow-sm border-0">
        <div class="table-responsive">
            <table class="table align-middle mb-0 table-hover">
                <thead class="table-light text-secondary">
                    <tr>
                        <th style="width: 80px;" class="text-center">ID</th>
                        <th>Anggota</th>
                        <th>Buku</th>
                        <th>Tanggal Request</th>
                        <th>Jatuh Tempo</th>
                        <th style="width: 120px;" class="text-center">Status</th>
                        <th style="width: 120px;" class="text-center">Aksi</th>
                    </tr>
                </thead>
                <tbody>
                    @forelse ($borrowings as $borrowing)
                        <tr>
                            <td class="text-center text-secondary small">#{{ $borrowing->id }}</td>
                            <td>
                                <div class="fw-semibold text-dark">{{ $borrowing->member?->name ?? 'Anggota Terhapus' }}</div>
                                <div class="text-secondary small">{{ $borrowing->member?->member_number ?? '-' }}</div>
                            </td>
                            <td>
                                <div class="fw-bold text-dark text-truncate" style="max-width: 250px;">
                                    {{ $borrowing->details->first()?->book?->title ?? '-' }}
                                </div>
                                <div class="text-secondary small">Kode: {{ $borrowing->details->first()?->book?->book_code ?? '-' }}</div>
                            </td>
                            <td>
                                <span class="small text-secondary">{{ $borrowing->request_date?->format('d/m/Y') ?? '-' }}</span>
                            </td>
                            <td>
                                <span class="small text-secondary">{{ $borrowing->due_date?->format('d/m/Y') ?? '-' }}</span>
                            </td>
                            <td class="text-center">
                                <span class="badge badge-status badge-{{ $borrowing->status }}">{{ ucfirst($borrowing->status) }}</span>
                            </td>
                            <td class="text-center">
                                <a href="{{ route('admin.borrowings.show', $borrowing) }}" class="btn btn-sm btn-outline-info">
                                    Detail
                                </a>
                            </td>
                        </tr>
                    @empty
                        <tr>
                            <td colspan="7" class="text-center text-secondary py-5">
                                Belum ada data transaksi peminjaman.
                            </td>
                        </tr>
                    @endforelse
                </tbody>
            </table>
        </div>
        @if ($borrowings->hasPages())
            <div class="card-footer bg-white py-3">
                {{ $borrowings->links('pagination::bootstrap-5') }}
            </div>
        @endif
    </div>
@endsection
