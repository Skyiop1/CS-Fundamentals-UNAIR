@extends('layouts.admin')

@section('title', 'Kelola Denda')
@section('page_title', 'Kelola Denda Anggota')

@section('content')
    <!-- Filter & Pencarian -->
    <div class="card app-card shadow-sm border-0 mb-4">
        <div class="card-body">
            <form action="{{ route('admin.fines.index') }}" method="GET" class="row g-3">
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
                        <option value="unpaid" {{ request('status') === 'unpaid' ? 'selected' : '' }}>Belum Lunas (Unpaid)</option>
                        <option value="paid" {{ request('status') === 'paid' ? 'selected' : '' }}>Lunas (Paid)</option>
                    </select>
                </div>
                <div class="col-12 col-md-4 d-flex gap-2">
                    <button type="submit" class="btn btn-primary flex-fill">Cari</button>
                    @if (request()->filled('search') || request()->filled('status'))
                        <a href="{{ route('admin.fines.index') }}" class="btn btn-outline-secondary">Reset</a>
                    @endif
                </div>
            </form>
        </div>
    </div>

    <!-- Tabel Data Denda -->
    <div class="card app-card shadow-sm border-0">
        <div class="table-responsive">
            <table class="table align-middle mb-0 table-hover">
                <thead class="table-light text-secondary">
                    <tr>
                        <th style="width: 80px;" class="text-center">ID</th>
                        <th>Anggota</th>
                        <th>Buku</th>
                        <th class="text-center">Keterlambatan</th>
                        <th>Jumlah Denda</th>
                        <th style="width: 120px;" class="text-center">Status</th>
                        <th>Tanggal Bayar</th>
                        <th style="width: 150px;" class="text-center">Aksi</th>
                    </tr>
                </thead>
                <tbody>
                    @forelse ($fines as $fine)
                        <tr>
                            <td class="text-center text-secondary small">#{{ $fine->id }}</td>
                            <td>
                                <div class="fw-semibold text-dark">{{ $fine->borrowing?->member?->name ?? 'Anggota Terhapus' }}</div>
                                <div class="text-secondary small">{{ $fine->borrowing?->member?->member_number ?? '-' }}</div>
                            </td>
                            <td>
                                <div class="fw-semibold text-dark text-truncate" style="max-width: 250px;">
                                    {{ $fine->borrowing?->details->first()?->book?->title ?? '-' }}
                                </div>
                                <div class="text-secondary small">Kode: {{ $fine->borrowing?->details->first()?->book?->book_code ?? '-' }}</div>
                            </td>
                            <td class="text-center">
                                <span class="badge bg-danger-subtle text-danger">{{ $fine->late_days }} hari</span>
                            </td>
                            <td>
                                <span class="fw-bold text-danger">{{ $fine->formattedAmount() }}</span>
                            </td>
                            <td class="text-center">
                                @if ($fine->status === 'paid')
                                    <span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-2.5">Lunas</span>
                                @else
                                    <span class="badge bg-warning-subtle text-warning border border-warning-subtle rounded-pill text-dark px-2.5">Belum Lunas</span>
                                @endif
                            </td>
                            <td>
                                <span class="small text-secondary">{{ $fine->paid_at?->format('d/m/Y H:i') ?? '-' }}</span>
                            </td>
                            <td class="text-center">
                                @if ($fine->status === 'unpaid')
                                    <form action="{{ route('admin.fines.markPaid', $fine) }}" method="POST" onsubmit="return confirm('Apakah Anda yakin denda ini sudah dibayar lunas?');">
                                        @csrf
                                        @method('PUT')
                                        <button type="submit" class="btn btn-sm btn-success">
                                            Tandai Lunas
                                        </button>
                                    </form>
                                @else
                                    <span class="text-secondary small fw-semibold"><i class="bi bi-check-circle-fill text-success me-1"></i>Selesai</span>
                                @endif
                            </td>
                        </tr>
                    @empty
                        <tr>
                            <td colspan="8" class="text-center text-secondary py-5">
                                Belum ada data denda keterlambatan.
                            </td>
                        </tr>
                    @endforelse
                </tbody>
            </table>
        </div>
        @if ($fines->hasPages())
            <div class="card-footer bg-white py-3">
                {{ $fines->links('pagination::bootstrap-5') }}
            </div>
        @endif
    </div>
@endsection
