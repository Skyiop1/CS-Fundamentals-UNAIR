@extends('layouts.admin')

@section('title', 'Detail Anggota')
@section('page_title', 'Detail Informasi Anggota')

@section('content')
    <div class="row g-4">
        <!-- Kolom Kiri: Informasi Profil -->
        <div class="col-12 col-lg-4">
            <div class="card app-card shadow-sm border-0">
                <div class="card-header bg-white py-3 border-bottom d-flex justify-content-between align-items-center">
                    <h5 class="card-title mb-0 fw-bold text-dark">Profil Anggota</h5>
                    <a href="{{ route('admin.members.edit', $member) }}" class="btn btn-sm btn-primary">Edit</a>
                </div>
                <div class="card-body p-4 text-center">
                    <div class="bg-light rounded-circle d-flex align-items-center justify-content-center mx-auto mb-3 shadow-sm" style="width: 80px; height: 80px; border: 1px solid var(--app-border);">
                        <span class="fs-2 fw-bold text-secondary">{{ strtoupper(substr($member->name, 0, 2)) }}</span>
                    </div>
                    <h5 class="fw-bold text-dark mb-1">{{ $member->name }}</h5>
                    <span class="badge bg-secondary mb-3">{{ $member->member_number }}</span>

                    <hr>

                    <div class="text-start mt-3">
                        <div class="mb-3">
                            <label class="text-secondary small fw-semibold d-block mb-1">Email</label>
                            <span class="text-dark">{{ $member->user?->email ?: '-' }}</span>
                        </div>
                        <div class="mb-3">
                            <label class="text-secondary small fw-semibold d-block mb-1">No. Telepon / WA</label>
                            <span class="text-dark">{{ $member->phone ?: '-' }}</span>
                        </div>
                        <div class="mb-3">
                            <label class="text-secondary small fw-semibold d-block mb-1">Alamat</label>
                            <span class="text-dark" style="font-size: 14px;">{{ $member->address ?: '-' }}</span>
                        </div>
                        <div class="mb-3">
                            <label class="text-secondary small fw-semibold d-block mb-1">Status Keanggotaan</label>
                            @if ($member->status === 'active')
                                <span class="badge bg-success-subtle text-success border border-success-subtle rounded-pill px-2.5">Aktif</span>
                            @else
                                <span class="badge bg-danger-subtle text-danger border border-danger-subtle rounded-pill px-2.5">Inaktif</span>
                            @endif
                        </div>
                        <div>
                            <label class="text-secondary small fw-semibold d-block mb-1">Terdaftar Sejak</label>
                            <span class="text-dark small">{{ $member->created_at?->format('d/m/Y H:i') ?: '-' }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Kolom Kanan: Riwayat Peminjaman Buku -->
        <div class="col-12 col-lg-8">
            <div class="card app-card shadow-sm border-0">
                <div class="card-header bg-white py-3 border-bottom d-flex justify-content-between align-items-center">
                    <h5 class="card-title mb-0 fw-bold text-dark">Riwayat Peminjaman Buku</h5>
                    <a href="{{ route('admin.members.index') }}" class="btn btn-sm btn-outline-secondary">Kembali ke Daftar</a>
                </div>
                <div class="table-responsive">
                    <table class="table align-middle mb-0">
                        <thead class="table-light text-secondary">
                            <tr>
                                <th style="width: 80px;" class="text-center">ID</th>
                                <th>Buku yang Dipinjam</th>
                                <th>Tanggal Pinjam</th>
                                <th>Jatuh Tempo</th>
                                <th>Tanggal Kembali</th>
                                <th class="text-center">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            @forelse ($borrowings as $borrowing)
                                <tr>
                                    <td class="text-center small text-secondary">#{{ $borrowing->id }}</td>
                                    <td>
                                        <div class="fw-semibold text-dark">
                                            {{ $borrowing->details->first()?->book?->title ?? '-' }}
                                        </div>
                                        @if ($borrowing->details->count() > 1)
                                            <span class="badge bg-light text-secondary border small">+ {{ $borrowing->details->count() - 1 }} buku lainnya</span>
                                        @endif
                                    </td>
                                    <td>
                                        <span class="small text-secondary">{{ $borrowing->borrowed_at?->format('d/m/Y') ?: ($borrowing->request_date?->format('d/m/Y') ?: '-') }}</span>
                                    </td>
                                    <td>
                                        <span class="small text-secondary">{{ $borrowing->due_date?->format('d/m/Y') ?: '-' }}</span>
                                    </td>
                                    <td>
                                        <span class="small text-secondary">{{ $borrowing->returned_at?->format('d/m/Y') ?: '-' }}</span>
                                    </td>
                                    <td class="text-center">
                                        <span class="badge badge-status badge-{{ $borrowing->status }}">{{ ucfirst($borrowing->status) }}</span>
                                    </td>
                                </tr>
                            @empty
                                <tr>
                                    <td colspan="6" class="text-center text-secondary py-5">
                                        Belum ada riwayat peminjaman untuk anggota ini.
                                    </td>
                                </tr>
                            @endforelse
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
@endsection
