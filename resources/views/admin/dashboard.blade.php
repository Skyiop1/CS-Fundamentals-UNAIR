@extends('layouts.admin')

@section('title', 'Dashboard Admin')
@section('page_title', 'Dashboard Admin')

@section('content')
    <div class="row g-3 mb-4">
        <div class="col-12 col-sm-6 col-xl-2">
            <div class="card app-card h-100"><div class="card-body"><div class="text-secondary small">Total Buku</div><div class="display-count">{{ $totalBooks }}</div></div></div>
        </div>
        <div class="col-12 col-sm-6 col-xl-2">
            <div class="card app-card h-100"><div class="card-body"><div class="text-secondary small">Total Anggota</div><div class="display-count">{{ $totalMembers }}</div></div></div>
        </div>
        <div class="col-12 col-sm-6 col-xl-2">
            <div class="card app-card h-100"><div class="card-body"><div class="text-secondary small">Peminjaman Aktif</div><div class="display-count">{{ $activeBorrowings }}</div></div></div>
        </div>
        <div class="col-12 col-sm-6 col-xl-2">
            <div class="card app-card h-100"><div class="card-body"><div class="text-secondary small">Menunggu</div><div class="display-count">{{ $pendingBorrowings }}</div></div></div>
        </div>
        <div class="col-12 col-sm-6 col-xl-2">
            <div class="card app-card h-100"><div class="card-body"><div class="text-secondary small">Terlambat</div><div class="display-count">{{ $lateReturns }}</div></div></div>
        </div>
        <div class="col-12 col-sm-6 col-xl-2">
            <div class="card app-card h-100"><div class="card-body"><div class="text-secondary small">Denda</div><div class="display-count fs-4">Rp {{ number_format($totalFines, 0, ',', '.') }}</div></div></div>
        </div>
    </div>

    <div class="card app-card">
        <div class="card-header bg-white fw-semibold">Transaksi Peminjaman Terbaru</div>
        <div class="table-responsive">
            <table class="table align-middle mb-0">
                <thead>
                    <tr>
                        <th>Anggota</th>
                        <th>Buku</th>
                        <th>Status</th>
                        <th>Tanggal Request</th>
                        <th>Jatuh Tempo</th>
                    </tr>
                </thead>
                <tbody>
                    @forelse ($recentBorrowings as $borrowing)
                        <tr>
                            <td>{{ $borrowing->member->name }}</td>
                            <td>{{ $borrowing->details->first()?->book?->title ?? '-' }}</td>
                            <td><span class="badge badge-status badge-{{ $borrowing->status }}">{{ ucfirst($borrowing->status) }}</span></td>
                            <td>{{ $borrowing->request_date?->format('d/m/Y') }}</td>
                            <td>{{ $borrowing->due_date?->format('d/m/Y') ?? '-' }}</td>
                        </tr>
                    @empty
                        <tr>
                            <td colspan="5" class="text-center text-secondary py-4">Belum ada transaksi peminjaman.</td>
                        </tr>
                    @endforelse
                </tbody>
            </table>
        </div>
    </div>
@endsection
