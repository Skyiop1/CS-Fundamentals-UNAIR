@extends('layouts.admin')

@section('title', 'Detail Transaksi Peminjaman')
@section('page_title', 'Detail Peminjaman #' . $borrowing->id)

@section('content')
    <div class="row justify-content-center">
        <div class="col-12 col-lg-10">
            <div class="card app-card shadow-sm border-0 mb-4">
                <div class="card-header bg-white py-3 border-bottom d-flex justify-content-between align-items-center">
                    <h5 class="card-title mb-0 fw-bold text-dark">Informasi Transaksi</h5>
                    <a href="{{ route('admin.borrowings.index') }}" class="btn btn-sm btn-outline-secondary">Kembali</a>
                </div>
                <div class="card-body p-4">
                    <div class="row g-4 mb-4">
                        <!-- Sisi Kiri: Status & Anggota -->
                        <div class="col-12 col-md-6">
                            <h6 class="fw-bold text-secondary small uppercase tracking-wider mb-2">Profil Anggota</h6>
                            <div class="p-3 bg-light rounded border mb-4">
                                <div class="fw-bold text-dark fs-6">{{ $borrowing->member?->name ?? 'Anggota Terhapus' }}</div>
                                <div class="text-secondary small">No. Anggota: <strong>{{ $borrowing->member?->member_number ?? '-' }}</strong></div>
                                <div class="text-secondary small">No. Telepon: {{ $borrowing->member?->phone ?: '-' }}</div>
                                <div class="text-secondary small">Alamat: {{ $borrowing->member?->address ?: '-' }}</div>
                            </div>

                            <h6 class="fw-bold text-secondary small uppercase tracking-wider mb-2">Buku yang Diajukan</h6>
                            @foreach ($borrowing->details as $detail)
                                <div class="p-3 bg-light rounded border d-flex gap-3 mb-2">
                                    @if ($detail->book->cover_image)
                                        <img src="{{ asset('storage/' . $detail->book->cover_image) }}" alt="Cover" class="rounded border" style="width: 48px; height: 68px; object-fit: cover;">
                                    @else
                                        <div class="bg-white border rounded text-secondary d-flex align-items-center justify-content-center" style="width: 48px; height: 68px; font-size: 10px; font-weight: bold;">
                                            NO COV
                                        </div>
                                    @endif
                                    <div>
                                        <div class="fw-bold text-dark">{{ $detail->book->title }}</div>
                                        <div class="text-secondary small">Kode: {{ $detail->book->book_code }}</div>
                                        <div class="text-secondary small">Pengarang: {{ $detail->book->author }}</div>
                                    </div>
                                </div>
                            @endforeach
                        </div>

                        <!-- Sisi Kanan: Status & Tanggal -->
                        <div class="col-12 col-md-6">
                            <h6 class="fw-bold text-secondary small uppercase tracking-wider mb-2">Status & Tanggal</h6>
                            <div class="mb-4">
                                <span class="badge badge-status badge-{{ $borrowing->status }} fs-6 px-3 py-2">
                                    {{ ucfirst($borrowing->status) }}
                                </span>
                            </div>

                            <table class="table table-sm table-borderless">
                                <tbody>
                                    <tr>
                                        <td class="text-secondary" style="width: 150px;">Tanggal Request</td>
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

                    <!-- Informasi Kondisi Khusus -->
                    @if ($borrowing->status === 'rejected')
                        <div class="alert alert-danger border-0 shadow-sm mb-4">
                            <h6 class="fw-bold"><i class="bi bi-x-circle-fill me-1"></i> Alasan Penolakan:</h6>
                            <p class="mb-0 small">{{ $borrowing->rejected_reason ?: 'Tidak dicantumkan alasan.' }}</p>
                        </div>
                    @endif

                    @if ($borrowing->fine)
                        <div class="card bg-light border border-danger-subtle shadow-sm mb-4">
                            <div class="card-body d-flex justify-content-between align-items-center">
                                <div>
                                    <h6 class="fw-bold text-dark mb-1">Denda Terlambat Kembali</h6>
                                    <p class="text-secondary small mb-0">
                                        Terlambat: <strong>{{ $borrowing->fine->late_days }} Hari</strong>
                                    </p>
                                </div>
                                <div class="text-end">
                                    <span class="fs-5 fw-bold text-danger d-block">Rp {{ number_format($borrowing->fine->amount, 0, ',', '.') }}</span>
                                    @if ($borrowing->fine->status === 'paid')
                                        <span class="badge bg-success text-white">Lunas</span>
                                    @else
                                        <span class="badge bg-warning text-dark">Belum Lunas</span>
                                    @endif
                                </div>
                            </div>
                        </div>
                    @endif

                    <!-- Tombol Aksi Admin -->
                    @if ($borrowing->status === 'pending')
                        <hr>
                        <div class="d-flex gap-3">
                            <form action="{{ route('admin.borrowings.approve', $borrowing) }}" method="POST" class="flex-fill">
                                @csrf
                                @method('PUT')
                                <button type="submit" class="btn btn-success w-100 py-2.5 fw-bold" onclick="return confirm('Apakah Anda yakin ingin menyetujui peminjaman ini? Stok buku akan berkurang.');">
                                    Setujui Peminjaman (Approve)
                                </button>
                            </form>
                            <button type="button" class="btn btn-danger flex-fill py-2.5 fw-bold" data-bs-toggle="modal" data-bs-target="#rejectModal">
                                Tolak Peminjaman (Reject)
                            </button>
                        </div>
                    @endif
                </div>
            </div>
        </div>
    </div>

    <!-- Modal Reject -->
    @if ($borrowing->status === 'pending')
        <div class="modal fade" id="rejectModal" tabindex="-1" aria-labelledby="rejectModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <form action="{{ route('admin.borrowings.reject', $borrowing) }}" method="POST">
                        @csrf
                        @method('PUT')
                        <div class="modal-header">
                            <h5 class="modal-title fw-bold" id="rejectModalLabel">Tolak Pengajuan Peminjaman</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="mb-3">
                                <label for="rejected_reason" class="form-label small fw-semibold text-secondary">Alasan Penolakan <span class="text-danger">*</span></label>
                                <textarea class="form-control" id="rejected_reason" name="rejected_reason" rows="4" placeholder="Contoh: Pengajuan melebihi kuota pinjam, atau stok habis." required></textarea>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Batal</button>
                            <button type="submit" class="btn btn-danger">Tolak Pengajuan</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    @endif
@endsection
