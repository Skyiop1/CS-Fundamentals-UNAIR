<!doctype html>
<html lang="id">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>@yield('title', 'Autentikasi') - Perpusku</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <link href="{{ asset('css/app.css') }}" rel="stylesheet">
</head>
<body class="auth-page">
    <main class="container">
        <div class="row min-vh-100 align-items-center justify-content-center py-5">
            <div class="col-12 col-md-8 col-lg-5">
                <div class="text-center mb-4">
                    <div class="brand-mark mx-auto mb-3">P</div>
                    <h1 class="h3 fw-extrabold mb-1">Perpus<span class="text-primary">ku</span></h1>
                    <p class="text-muted small mb-0">Sistem Peminjaman Buku Perpustakaan Modern</p>
                </div>

                <div class="card app-card shadow-sm">
                    <div class="card-body p-4 p-md-5">
                        @yield('content')
                    </div>
                </div>
            </div>
        </div>
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
