@extends('layouts.member')

@section('title', 'Peminjaman Saya')

@section('content')
    <div class="mb-4 d-flex justify-content-between align-items-center flex-wrap gap-3">
        <div>
            <h1 class="h3 fw-bold mb-1">Daftar Peminjaman Saya</h1>
            <p class="text-secondary mb-0">Pantau status pengajuan peminjaman buku dan denda keterlambatan Anda di sini.</p>
        </div>
    </div>

    <!-- Filter Status -->
    <div class="card app-card shadow-sm border-0 mb-4">
        <div class="card-body p-3">
            <form action="{{ route('borrowings.mine') }}" method="GET" class="row g-3">
                <div class="col-12 col-md-8">
                    <div class="d-flex flex-wrap gap-2">
                        <a href="{{ route('borrowings.mine') }}" class="btn btn-sm {{ !request('status') ? 'btn-secondary' : 'btn-outline-secondary' }}">
                            Semua
                        </a>
                        <a href="{{ route('borrowings.mine', ['status' => 'pending']) }}" class="btn btn-sm {{ request('status') === 'pending' ? 'btn-warning text-dark' : 'btn-outline-secondary' }}">
                            Menunggu (Pending)
                        </a>
                        <a href="{{ route('borrowings.mine', ['status' => 'borrowed']) }}" class="btn btn-sm {{ request('status') === 'borrowed' ? 'btn-primary' : 'btn-outline-secondary' }}">
                            Dipinjam (Active)
                        </a>
                        <a href="{{ route('borrowings.mine', ['status' => 'returned']) }}" class="btn btn-sm {{ request('status') === 'returned' ? 'btn-success' : 'btn-outline-secondary' }}">
                            Dikembalikan
                        </a>
                        <a href="{{ route('borrowings.mine', ['status' => 'rejected']) }}" class="btn btn-sm {{ request('status') === 'rejected' ? 'btn-danger' : 'btn-outline-secondary' }}">
                            Ditolak
                        </a>
                        <a href="{{ route('borrowings.mine', ['status' => 'late']) }}" class="btn btn-sm {{ request('status') === 'late' ? 'btn-danger' : 'btn-outline-secondary' }}">
                            Terlambat
                        </a>
                    </div>
                </div>
                <div class="col-12 col-md-4 text-md-end">
                    <!-- Dropdown fallback for mobile screens if they prefer -->
                    <select name="status" class="form-select form-select-sm d-md-none" onchange="this.form.submit()">
                        <option value="">Pilih Status</option>
                        <option value="pending" {{ request('status') == 'pending' ? 'selected' : '' }}>Pending</option>
                        <option value="approved" {{ request('status') == 'approved' ? 'selected' : '' }}>Approved</option>
                        <option value="borrowed" {{ request('status') == 'borrowed' ? 'selected' : '' }}>Borrowed</option>
                        <option value="returned" {{ request('status') == 'returned' ? 'selected' : '' }}>Returned</option>
                        <option value="rejected" {{ request('status') == 'rejected' ? 'selected' : '' }}>Rejected</option>
                        <option value="late" {{ request('status') == 'late' ? 'selected' : '' }}>Late</option>
                    </select>
                </div>
            </form>
        </div>
    </div>

    <!-- Tabel Riwayat Peminjaman -->
    <div class="card app-card shadow-sm border-0">
        <div class="table-responsive">
            <table class="table align-middle mb-0 table-hover">
                <thead class="table-light text-secondary">
                    <tr>
                        <th style="width: 80px;" class="text-center">ID</th>
                        <th>Buku</th>
                        <th>Tanggal Pengajuan</th>
                        <th>Jatuh Tempo</th>
                        <th>Denda</th>
                        <th style="width: 120px;" class="text-center">Status</th>
                        <th style="width: 120px;" class="text-center">Aksi</th>
                    </tr>
                </thead>
                <tbody>
                    @forelse ($borrowings as $borrowing)
                        <tr>
                            <td class="text-center small text-secondary">#{{ $borrowing->id }}</td>
                            <td>
                                <div class="fw-bold text-dark">{{ $borrowing->details->first()?->book?->title ?? 'Buku Tidak Diketahui' }}</div>
                                <div class="text-secondary small">Kode: {{ $borrowing->details->first()?->book?->book_code ?? '-' }}</div>
                            </td>
                            <td>
                                <span class="small text-secondary">{{ $borrowing->request_date?->format('d/m/Y') ?? '-' }}</span>
                            </td>
                            <td>
                                <span class="small text-secondary">{{ $borrowing->due_date?->format('d/m/Y') ?? '-' }}</span>
                            </td>
                            <td>
                                @if ($borrowing->fine)
                                    <span class="small fw-semibold text-danger">Rp {{ number_format($borrowing->fine->amount, 0, ',', '.') }}</span>
                                    @if ($borrowing->fine->status === 'paid')
                                        <span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill ms-1 fw-normal" style="font-size: 10px;">Lunas</span>
                                    @else
                                        <span class="badge bg-warning-subtle text-warning border border-warning-subtle rounded-pill ms-1 fw-normal text-dark" style="font-size: 10px;">Belum Lunas</span>
                                    @endif
                                @else
                                    <span class="small text-secondary">-</span>
                                @endif
                            </td>
                            <td class="text-center">
                                <span class="badge badge-status badge-{{ $borrowing->status }}">{{ ucfirst($borrowing->status) }}</span>
                            </td>
                            <td class="text-center">
                                <a href="{{ route('borrowings.showMine', $borrowing) }}" class="btn btn-sm btn-outline-info">
                                    Detail
                                </a>
                            </td>
                        </tr>
                    @empty
                        <tr>
                            <td colspan="7" class="text-center text-secondary py-5">
                                Belum ada transaksi peminjaman buku yang sesuai.
                            </td>
                        </tr>
                    @endforelse
                </tbody>
            </table>
        </div>
        @if ($borrowings instanceof \Illuminate\Pagination\LengthAwarePaginator && $borrowings->hasPages())
            <div class="card-footer bg-white py-3">
                {{ $borrowings->links('pagination::bootstrap-5') }}
            </div>
        @endif
    </div>
@endsection
