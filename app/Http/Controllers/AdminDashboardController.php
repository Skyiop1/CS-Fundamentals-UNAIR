<?php

namespace App\Http\Controllers;

use App\Models\Book;
use App\Models\Borrowing;
use App\Models\Fine;
use App\Models\Member;
use Illuminate\View\View;

class AdminDashboardController extends Controller
{
    public function index(): View
    {
        return view('admin.dashboard', [
            'totalBooks' => Book::count(),
            'totalMembers' => Member::where('status', 'active')->count(),
            'activeBorrowings' => Borrowing::whereIn('status', ['approved', 'borrowed', 'late'])->count(),
            'pendingBorrowings' => Borrowing::where('status', 'pending')->count(),
            'lateReturns' => Borrowing::where('status', 'late')->count(),
            'totalFines' => Fine::where('status', 'unpaid')->sum('amount'),
            'recentBorrowings' => Borrowing::with(['member', 'details.book'])
                ->latest()
                ->limit(5)
                ->get(),
        ]);
    }
}
