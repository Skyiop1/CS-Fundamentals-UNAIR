<!doctype html>
<html lang="id">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>@yield('title', 'Admin') - Sistem Informasi Perpustakaan</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="{{ asset('css/app.css') }}" rel="stylesheet">
</head>
<body>
    <div class="admin-shell">
        <aside class="admin-sidebar">
            <div class="px-3 py-4">
                <div class="d-flex align-items-center gap-2 mb-4">
                    <div class="brand-mark brand-mark-sm">P</div>
                    <div>
                        <div class="fw-bold">Perpustakaan</div>
                        <small class="text-white-50">Panel Admin</small>
                    </div>
                </div>

                <nav class="nav flex-column gap-1">
                    <a class="nav-link {{ request()->routeIs('admin.dashboard') ? 'active' : '' }}" href="{{ route('admin.dashboard') }}">Dashboard</a>
                    <a class="nav-link {{ request()->routeIs('admin.books.*') ? 'active' : '' }}" href="{{ route('admin.books.index') }}">Data Buku</a>
                    <a class="nav-link {{ request()->routeIs('admin.categories.*') ? 'active' : '' }}" href="{{ route('admin.categories.index') }}">Kategori</a>
                    <a class="nav-link {{ request()->routeIs('admin.members.*') ? 'active' : '' }}" href="{{ route('admin.members.index') }}">Data Anggota</a>
                    <a class="nav-link {{ request()->routeIs('admin.borrowings.*') ? 'active' : '' }}" href="{{ route('admin.borrowings.index') }}">Peminjaman</a>
                    <a class="nav-link {{ request()->routeIs('admin.returns.*') ? 'active' : '' }}" href="{{ route('admin.returns.index') }}">Pengembalian</a>
                    <a class="nav-link {{ request()->routeIs('admin.fines.*') ? 'active' : '' }}" href="{{ route('admin.fines.index') }}">Denda</a>
                    <a class="nav-link disabled" href="#">Laporan</a>
                </nav>
            </div>
        </aside>

        <div class="admin-main">
            <nav class="navbar navbar-expand bg-white border-bottom sticky-top">
                <div class="container-fluid">
                    <span class="navbar-brand fw-semibold">@yield('page_title', 'Dashboard')</span>
                    <div class="d-flex align-items-center gap-3">
                        <span class="text-secondary small">{{ auth()->user()->name }}</span>
                        <form action="{{ route('logout') }}" method="POST">
                            @csrf
                            <button class="btn btn-sm btn-outline-secondary" type="submit">Logout</button>
                        </form>
                    </div>
                </div>
            </nav>

            <main class="container-fluid py-4">
                @if (session('success'))
                    <div class="alert alert-success alert-dismissible fade show border-0 shadow-sm" role="alert">
                        {{ session('success') }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                @endif
                @if (session('error'))
                    <div class="alert alert-danger alert-dismissible fade show border-0 shadow-sm" role="alert">
                        {{ session('error') }}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                @endif
                @yield('content')
            </main>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
