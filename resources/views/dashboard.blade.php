@extends('layouts.member')

@section('title', 'Dashboard Anggota')

@section('content')
    <div class="mb-4">
        <h1 class="h3 fw-bold mb-1">Dashboard Anggota</h1>
        <p class="text-secondary mb-0">
            Selamat datang, {{ auth()->user()->name }}.
            @if ($member)
                Nomor anggota: <strong>{{ $member->member_number }}</strong>
            @endif
        </p>
    </div>

    <div class="row g-3 mb-4">
        <div class="col-12 col-md-3">
            <div class="card app-card h-100"><div class="card-body"><div class="text-secondary small">Peminjaman Aktif</div><div class="display-count">{{ $activeBorrowings }}</div></div></div>
        </div>
        <div class="col-12 col-md-3">
            <div class="card app-card h-100"><div class="card-body"><div class="text-secondary small">Menunggu Persetujuan</div><div class="display-count">{{ $pendingRequests }}</div></div></div>
        </div>
        <div class="col-12 col-md-3">
            <div class="card app-card h-100"><div class="card-body"><div class="text-secondary small">Sudah Dikembalikan</div><div class="display-count">{{ $returnedBooks }}</div></div></div>
        </div>
        <div class="col-12 col-md-3">
            <div class="card app-card h-100"><div class="card-body"><div class="text-secondary small">Denda Belum Dibayar</div><div class="display-count fs-4">Rp {{ number_format($totalUnpaidFines, 0, ',', '.') }}</div></div></div>
        </div>
    </div>

    <div class="card app-card">
        <div class="card-header bg-white fw-semibold">Riwayat Peminjaman Terbaru</div>
        <div class="table-responsive">
            <table class="table align-middle mb-0">
                <thead>
                    <tr>
                        <th>Buku</th>
                        <th>Status</th>
                        <th>Tanggal Request</th>
                        <th>Jatuh Tempo</th>
                        <th>Denda</th>
                    </tr>
                </thead>
                <tbody>
                    @forelse ($recentBorrowings as $borrowing)
                        <tr>
                            <td>{{ $borrowing->details->first()?->book?->title ?? '-' }}</td>
                            <td><span class="badge badge-status badge-{{ $borrowing->status }}">{{ ucfirst($borrowing->status) }}</span></td>
                            <td>{{ $borrowing->request_date?->format('d/m/Y') }}</td>
                            <td>{{ $borrowing->due_date?->format('d/m/Y') ?? '-' }}</td>
                            <td>Rp {{ number_format($borrowing->fine?->amount ?? 0, 0, ',', '.') }}</td>
                        </tr>
                    @empty
                        <tr>
                            <td colspan="5" class="text-center text-secondary py-4">Belum ada riwayat peminjaman.</td>
                        </tr>
                    @endforelse
                </tbody>
            </table>
        </div>
    </div>
@endsection
