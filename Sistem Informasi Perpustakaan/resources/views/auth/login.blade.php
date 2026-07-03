@extends('layouts.auth')

@section('title', 'Login')

@section('content')
    <h2 class="h5 fw-bold mb-1">Login</h2>
    <p class="text-secondary mb-4">Masuk menggunakan akun admin atau anggota.</p>

    @if ($errors->any())
        <div class="alert alert-danger">
            {{ $errors->first() }}
        </div>
    @endif

    <form action="{{ route('login.store') }}" method="POST">
        @csrf
        <div class="mb-3">
            <label class="form-label" for="email">Email</label>
            <input class="form-control" id="email" type="email" name="email" value="{{ old('email') }}" required autofocus>
        </div>
        <div class="mb-3">
            <label class="form-label" for="password">Password</label>
            <input class="form-control" id="password" type="password" name="password" required>
        </div>
        <div class="d-flex justify-content-between align-items-center mb-4">
            <div class="form-check">
                <input class="form-check-input" id="remember" type="checkbox" name="remember">
                <label class="form-check-label" for="remember">Ingat saya</label>
            </div>
        </div>
        <button class="btn btn-primary w-100" type="submit">Login</button>
    </form>

    <div class="border-top mt-4 pt-4">
        <p class="small text-secondary mb-2">Akun demo:</p>
        <div class="small text-secondary">
            Admin: <strong>admin@perpus.test</strong> / <strong>password</strong><br>
            Anggota: <strong>anggota@perpus.test</strong> / <strong>password</strong>
        </div>
        <p class="mb-0 mt-3">Belum punya akun? <a href="{{ route('register') }}">Daftar sebagai anggota</a></p>
    </div>
@endsection
