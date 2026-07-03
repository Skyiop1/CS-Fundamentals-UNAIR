@extends('layouts.admin')

@section('title', 'Kelola Anggota')
@section('page_title', 'Kelola Data Anggota')

@section('content')
    <div class="card app-card shadow-sm border-0 mb-4">
        <div class="card-body">
            <form action="{{ route('admin.members.index') }}" method="GET" class="row g-3">
                <div class="col-12 col-md-5">
                    <div class="input-group">
                        <span class="input-group-text bg-transparent text-secondary border-end-0">
                            <i class="bi bi-search"></i>
                        </span>
                        <input type="text" name="search" class="form-control border-start-0 ps-0" placeholder="Cari nama, nomor anggota, atau telepon..." value="{{ request('search') }}">
                    </div>
                </div>
                <div class="col-12 col-md-3">
                    <select name="status" class="form-select">
                        <option value="">Semua Status</option>
                        <option value="active" {{ request('status') == 'active' ? 'selected' : '' }}>Aktif</option>
                        <option value="inactive" {{ request('status') == 'inactive' ? 'selected' : '' }}>Inaktif</option>
                    </select>
                </div>
                <div class="col-12 col-md-4 d-flex gap-2">
                    <button type="submit" class="btn btn-primary flex-fill">Cari</button>
                    @if (request()->filled('search') || request()->filled('status'))
                        <a href="{{ route('admin.members.index') }}" class="btn btn-outline-secondary">Reset</a>
                    @endif
                    <a href="{{ route('admin.members.create') }}" class="btn btn-success flex-fill">
                        + Tambah Anggota
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
                        <th style="width: 150px;">No. Anggota</th>
                        <th>Nama & Email</th>
                        <th>No. Telepon</th>
                        <th>Alamat</th>
                        <th style="width: 120px;" class="text-center">Status</th>
                        <th style="width: 200px;" class="text-center">Aksi</th>
                    </tr>
                </thead>
                <tbody>
                    @forelse ($members as $member)
                        <tr>
                            <td>
                                <code class="text-dark fw-bold">{{ $member->member_number }}</code>
                            </td>
                            <td>
                                <div class="fw-semibold text-dark">{{ $member->name }}</div>
                                <div class="text-secondary small">{{ $member->user?->email }}</div>
                            </td>
                            <td>
                                <span class="small text-secondary">{{ $member->phone ?: '-' }}</span>
                            </td>
                            <td>
                                <div class="text-truncate small text-secondary" style="max-width: 220px;">
                                    {{ $member->address ?: '-' }}
                                </div>
                            </td>
                            <td class="text-center">
                                @if ($member->status === 'active')
                                    <span class="badge bg-success-subtle text-success rounded-pill px-2.5 border border-success-subtle">Aktif</span>
                                @else
                                    <span class="badge bg-danger-subtle text-danger rounded-pill px-2.5 border border-danger-subtle">Inaktif</span>
                                @endif
                            </td>
                            <td class="text-center">
                                <div class="d-flex justify-content-center gap-2">
                                    <a href="{{ route('admin.members.show', $member) }}" class="btn btn-sm btn-outline-info">
                                        Detail
                                    </a>
                                    <a href="{{ route('admin.members.edit', $member) }}" class="btn btn-sm btn-outline-primary">
                                        Edit
                                    </a>
                                    <form action="{{ route('admin.members.destroy', $member) }}" method="POST" onsubmit="return confirm('Apakah Anda yakin ingin menghapus anggota ini? Data user yang berhubungan juga akan dihapus.');">
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
                            <td colspan="6" class="text-center text-secondary py-5">
                                Belum ada data anggota perpustakaan yang sesuai.
                            </td>
                        </tr>
                    @endforelse
                </tbody>
            </table>
        </div>
        @if ($members->hasPages())
            <div class="card-footer bg-white py-3">
                {{ $members->links('pagination::bootstrap-5') }}
            </div>
        @endif
    </div>
@endsection
