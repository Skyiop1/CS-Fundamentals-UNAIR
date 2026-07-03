@extends('layouts.member')

@section('title', 'Detail Peminjaman #' . $borrowing->id)

@section('content')
    <div class="row justify-content-center">
        <div class="col-12 col-lg-10">
            <div class="card app-card shadow-sm border-0 mb-4">
                <div class="card-header bg-white py-3 border-bottom d-flex justify-content-between align-items-center">
                    <h5 class="card-title mb-0 fw-bold text-dark">Detail Transaksi Peminjaman #{{ $borrowing->id }}</h5>
                    <a href="{{ route('borrowings.mine') }}" class="btn btn-sm btn-outline-secondary">Kembali</a>
                </div>
                <div class="card-body p-4">
                    <div class="row g-4 mb-4">
                        <!-- Sisi Kiri: Status & Buku -->
                        <div class="col-12 col-md-6">
                            <h6 class="fw-bold text-secondary small uppercase tracking-wider mb-2">Status Transaksi</h6>
                            <div class="mb-4">
                                <span class="badge badge-status badge-{{ $borrowing->status }} fs-6 px-3 py-2">
                                    {{ ucfirst($borrowing->status) }}
                                </span>
                            </div>

                            <h6 class="fw-bold text-secondary small uppercase tracking-wider mb-2">Buku yang Dipinjam</h6>
                            @foreach ($borrowing->details as $detail)
                                <div class="p-3 bg-light rounded border d-flex gap-3 mb-2">
                                    @if ($detail->book->cover_image)
                                        <img src="{{ asset('storage/' . $detail->book->cover_image) }}" alt="Cover" class="rounded" style="width: 48px; height: 68px; object-fit: cover;">
                                    @else
                                        <div class="bg-white border rounded text-secondary d-flex align-items-center justify-content-center" style="width: 48px; height: 68px; font-size: 10px; font-weight: bold;">
                                            NO COV
                                        </div>
                                    @endif
                                    <div>
                                        <div class="fw-bold text-dark">{{ $detail->book->title }}</div>
                                        <div class="text-secondary small">Kode: {{ $detail->book->book_code }}</div>
                                        <div class="text-secondary small">Penulis: {{ $detail->book->author }}</div>
                                    </div>
                                </div>
                            @endforeach
                        </div>

                        <!-- Sisi Kanan: Alur Tanggal -->
                        <div class="col-12 col-md-6">
                            <h6 class="fw-bold text-secondary small uppercase tracking-wider mb-2">Alur Tanggal Peminjaman</h6>
                            <table class="table table-sm table-borderless">
                                <tbody>
                                    <tr>
                                        <td class="text-secondary" style="width: 150px;">Tanggal Pengajuan</td>
                                        <td>: {{ $borrowing->request_date?->format('d F Y') ?? '-' }}</td>
                                    </tr>
                                    <tr>
                                        <td class="text-secondary">Tanggal Disetujui</td>
                                        <td>: {{ $borrowing->approved_at?->format('d F Y H:i') ?? '-' }}</td>
                                    </tr>
                                    <tr>
                                        <td class="text-secondary">Tanggal Pinjam</td>
                                        <td>: {{ $borrowing->borrowed_at?->format('d F Y') ?? '-' }}</td>
                                    </tr>
                                    <tr>
                                        <td class="text-secondary">Jatuh Tempo</td>
                                        <td>: <span class="fw-semibold text-danger">{{ $borrowing->due_date?->format('d F Y') ?? '-' }}</span></td>
                                    </tr>
                                    <tr>
                                        <td class="text-secondary">Tanggal Kembali</td>
                                        <td>: {{ $borrowing->returned_at?->format('d F Y') ?? '-' }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>

                    <!-- Informasi Kondisi Khusus (Ditolak / Terlambat / Denda) -->
                    @if ($borrowing->status === 'rejected')
                        <div class="alert alert-danger border-0 shadow-sm mb-4">
                            <h6 class="fw-bold"><i class="bi bi-x-circle-fill me-1"></i> Alasan Penolakan Admin:</h6>
                            <p class="mb-0 small">{{ $borrowing->rejected_reason ?: 'Tidak dicantumkan alasan.' }}</p>
                        </div>
                    @endif

                    @if ($borrowing->fine)
                        <div class="card bg-light border-0 shadow-sm mb-0">
                            <div class="card-body d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="fw-bold text-dark mb-1">Informasi Denda Keterlambatan</h6>
                                    <p class="text-secondary small mb-0">
                                        Keterlambatan: <strong>{{ $borrowing->fine->late_days }} Hari</strong>
                                        @if ($borrowing->fine->paid_at)
                                            <span class="text-muted">(Dibayar pada: {{ $borrowing->fine->paid_at->format('d/m/Y H:i') }})</span>
                                        @endif
                                    </p>
                                </div>
                                <div class="text-end">
                                    <span class="fs-4 fw-bold text-danger d-block">Rp {{ number_format($borrowing->fine->amount, 0, ',', '.') }}</span>
                                    @if ($borrowing->fine->status === 'paid')
                                        <span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill">Lunas</span>
                                    @else
                                        <span class="badge bg-warning-subtle text-warning border border-warning-subtle rounded-pill text-dark">Belum Dibayar</span>
                                    @endif
                                </div>
                            </div>
                        </div>
                    @elseif ($borrowing->status === 'late')
                        <div class="alert alert-danger border-0 shadow-sm mb-0">
                            <h6 class="fw-bold"><i class="bi bi-exclamation-triangle-fill me-1"></i> Buku Terlambat Dikembalikan:</h6>
                            <p class="mb-0 small">Buku ini telah melewati batas jatuh tempo. Denda akan dihitung secara otomatis sebesar <strong>Rp 1.000 per hari keterlambatan</strong> saat proses pengembalian dikonfirmasi oleh petugas perpustakaan.</p>
                        </div>
                    @endif
                </div>
            </div>
        </div>
    </div>
@endsection
