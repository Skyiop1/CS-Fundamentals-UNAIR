@extends('layouts.auth')

@section('title', 'Registrasi Anggota')

@section('content')
    <h2 class="h5 fw-bold mb-1">Registrasi Anggota</h2>
    <p class="text-secondary mb-4">Akun baru otomatis dibuat sebagai anggota perpustakaan.</p>

    @if ($errors->any())
        <div class="alert alert-danger">
            <ul class="mb-0 ps-3">
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <form action="{{ route('register.store') }}" method="POST">
        @csrf
        <div class="mb-3">
            <label class="form-label" for="name">Nama Lengkap</label>
            <input class="form-control" id="name" type="text" name="name" value="{{ old('name') }}" required>
        </div>
        <div class="mb-3">
            <label class="form-label" for="email">Email</label>
            <input class="form-control" id="email" type="email" name="email" value="{{ old('email') }}" required>
        </div>
        <div class="mb-3">
            <label class="form-label" for="phone">Nomor Telepon</label>
            <input class="form-control" id="phone" type="text" name="phone" value="{{ old('phone') }}">
        </div>
        <div class="mb-3">
            <label class="form-label" for="address">Alamat</label>
            <textarea class="form-control" id="address" name="address" rows="3">{{ old('address') }}</textarea>
        </div>
        <div class="mb-3">
            <label class="form-label" for="password">Password</label>
            <input class="form-control" id="password" type="password" name="password" required>
        </div>
        <div class="mb-4">
            <label class="form-label" for="password_confirmation">Konfirmasi Password</label>
            <input class="form-control" id="password_confirmation" type="password" name="password_confirmation" required>
        </div>
        <button class="btn btn-primary w-100" type="submit">Daftar</button>
    </form>

    <p class="mb-0 mt-4">Sudah punya akun? <a href="{{ route('login') }}">Login</a></p>
@endsection
