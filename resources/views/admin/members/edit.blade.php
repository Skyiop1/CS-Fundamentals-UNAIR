@extends('layouts.admin')

@section('title', 'Edit Anggota')
@section('page_title', 'Edit Data Anggota')

@section('content')
    <div class="row justify-content-center">
        <div class="col-12 col-lg-8">
            <div class="card app-card shadow-sm border-0">
                <div class="card-header bg-white py-3 border-bottom d-flex justify-content-between align-items-center">
                    <h5 class="card-title mb-0 fw-bold text-dark">Form Edit Anggota: {{ $member->member_number }}</h5>
                    <a href="{{ route('admin.members.index') }}" class="btn btn-sm btn-outline-secondary">Kembali</a>
                </div>
                <div class="card-body p-4">
                    <form action="{{ route('admin.members.update', $member) }}" method="POST">
                        @csrf
                        @method('PUT')
                        <div class="row g-3 mb-4">
                            <!-- Nomor Anggota (Readonly) -->
                            <div class="col-12 col-md-6">
                                <label class="form-label small fw-semibold text-secondary">Nomor Anggota</label>
                                <input type="text" class="form-control bg-light" value="{{ $member->member_number }}" readonly>
                            </div>

                            <!-- Status -->
                            <div class="col-12 col-md-6">
                                <label for="status" class="form-label small fw-semibold text-secondary">Status Anggota <span class="text-danger">*</span></label>
                                <select class="form-select @error('status') is-invalid @enderror" id="status" name="status" required>
                                    <option value="active" {{ old('status', $member->status) === 'active' ? 'selected' : '' }}>Aktif</option>
                                    <option value="inactive" {{ old('status', $member->status) === 'inactive' ? 'selected' : '' }}>Inaktif</option>
                                </select>
                                @error('status')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>

                            <!-- Nama Lengkap -->
                            <div class="col-12">
                                <label for="name" class="form-label small fw-semibold text-secondary">Nama Lengkap <span class="text-danger">*</span></label>
                                <input type="text" class="form-control @error('name') is-invalid @enderror" id="name" name="name" value="{{ old('name', $member->name) }}" required>
                                @error('name')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>

                            <!-- Email -->
                            <div class="col-12 col-md-6">
                                <label for="email" class="form-label small fw-semibold text-secondary">Alamat Email <span class="text-danger">*</span></label>
                                <input type="email" class="form-control @error('email') is-invalid @enderror" id="email" name="email" value="{{ old('email', $member->user?->email) }}" required>
                                @error('email')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>

                            <!-- No Telepon -->
                            <div class="col-12 col-md-6">
                                <label for="phone" class="form-label small fw-semibold text-secondary">No. Telepon / WA</label>
                                <input type="text" class="form-control @error('phone') is-invalid @enderror" id="phone" name="phone" value="{{ old('phone', $member->phone) }}">
                                @error('phone')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>

                            <!-- Password Baru -->
                            <div class="col-12 col-md-6">
                                <label for="password" class="form-label small fw-semibold text-secondary">Password Baru (Kosongkan jika tidak ingin diubah)</label>
                                <input type="password" class="form-control @error('password') is-invalid @enderror" id="password" name="password" placeholder="Minimal 8 karakter...">
                                @error('password')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>

                            <!-- Konfirmasi Password Baru -->
                            <div class="col-12 col-md-6">
                                <label for="password_confirmation" class="form-label small fw-semibold text-secondary">Konfirmasi Password Baru</label>
                                <input type="password" class="form-control" id="password_confirmation" name="password_confirmation" placeholder="Ulangi password...">
                            </div>

                            <!-- Alamat -->
                            <div class="col-12">
                                <label for="address" class="form-label small fw-semibold text-secondary">Alamat Lengkap</label>
                                <textarea class="form-control @error('address') is-invalid @enderror" id="address" name="address" rows="3">{{ old('address', $member->address) }}</textarea>
                                @error('address')
                                    <div class="invalid-feedback">{{ $message }}</div>
                                @enderror
                            </div>
                        </div>

                        <div class="d-flex gap-3">
                            <button type="submit" class="btn btn-primary px-4 py-2">
                                Simpan Perubahan
                            </button>
                            <a href="{{ route('admin.members.index') }}" class="btn btn-outline-secondary px-4 py-2">
                                Batal
                            </a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
@endsection
