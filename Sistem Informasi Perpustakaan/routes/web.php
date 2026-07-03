<?php

use App\Http\Controllers\AdminDashboardController;
use App\Http\Controllers\AuthController;
use App\Http\Controllers\MemberDashboardController;
use App\Http\Controllers\BookController;
use App\Http\Controllers\CategoryController;
use App\Http\Controllers\MemberController;
use App\Http\Controllers\CatalogController;
use App\Http\Controllers\BorrowingController;
use App\Http\Controllers\ReturnController;
use App\Http\Controllers\FineController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    if (auth()->check()) {
        return auth()->user()->isAdmin()
            ? redirect()->route('admin.dashboard')
            : redirect()->route('dashboard');
    }

    return redirect()->route('login');
});

Route::middleware('guest')->group(function () {
    Route::get('/login', [AuthController::class, 'showLogin'])->name('login');
    Route::post('/login', [AuthController::class, 'login'])->name('login.store');
    Route::get('/register', [AuthController::class, 'showRegister'])->name('register');
    Route::post('/register', [AuthController::class, 'register'])->name('register.store');
});

Route::post('/logout', [AuthController::class, 'logout'])
    ->middleware('auth')
    ->name('logout');

Route::middleware(['auth', 'admin'])
    ->prefix('admin')
    ->name('admin.')
    ->group(function () {
        Route::get('/dashboard', [AdminDashboardController::class, 'index'])->name('dashboard');
        Route::resource('books', BookController::class);
        Route::resource('categories', CategoryController::class)->except(['create', 'show']);
        Route::resource('members', MemberController::class);

        // Peminjaman Admin
        Route::get('/borrowings', [BorrowingController::class, 'index'])->name('borrowings.index');
        Route::get('/borrowings/{borrowing}', [BorrowingController::class, 'show'])->name('borrowings.show');
        Route::put('/borrowings/{borrowing}/approve', [BorrowingController::class, 'approve'])->name('borrowings.approve');
        Route::put('/borrowings/{borrowing}/reject', [BorrowingController::class, 'reject'])->name('borrowings.reject');

        // Pengembalian Admin
        Route::get('/returns', [ReturnController::class, 'index'])->name('returns.index');
        Route::post('/returns/{borrowing}', [ReturnController::class, 'store'])->name('returns.store');

        // Denda Admin
        Route::get('/fines', [FineController::class, 'index'])->name('fines.index');
        Route::put('/fines/{fine}/mark-paid', [FineController::class, 'markPaid'])->name('fines.markPaid');
    });

Route::middleware('auth')->group(function () {
    Route::get('/dashboard', [MemberDashboardController::class, 'index'])->name('dashboard');

    // Katalog Buku
    Route::get('/catalog', [CatalogController::class, 'index'])->name('catalog.index');
    Route::get('/catalog/{book}', [CatalogController::class, 'show'])->name('catalog.show');

    // Peminjaman Anggota
    Route::post('/borrowings/request/{book}', [BorrowingController::class, 'request'])->name('borrowings.request');
    Route::get('/my-borrowings', [BorrowingController::class, 'mine'])->name('borrowings.mine');
    Route::get('/my-borrowings/{borrowing}', [BorrowingController::class, 'showMine'])->name('borrowings.showMine');
});
