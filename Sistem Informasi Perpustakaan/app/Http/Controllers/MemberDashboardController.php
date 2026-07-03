<?php

namespace App\Http\Controllers;

use App\Models\Fine;
use Illuminate\Http\RedirectResponse;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

class MemberDashboardController extends Controller
{
    public function index(): View|RedirectResponse
    {
        if (Auth::user()->isAdmin()) {
            return redirect()->route('admin.dashboard');
        }

        $member = Auth::user()->member;

        $borrowings = $member
            ? $member->borrowings()->with(['details.book', 'fine'])->latest()->get()
            : collect();

        return view('dashboard', [
            'member' => $member,
            'activeBorrowings' => $borrowings->whereIn('status', ['approved', 'borrowed', 'late'])->count(),
            'pendingRequests' => $borrowings->where('status', 'pending')->count(),
            'returnedBooks' => $borrowings->where('status', 'returned')->count(),
            'totalUnpaidFines' => $member
                ? Fine::whereHas('borrowing', fn ($query) => $query->where('member_id', $member->id))
                    ->where('status', 'unpaid')
                    ->sum('amount')
                : 0,
            'recentBorrowings' => $borrowings->take(5),
        ]);
    }
}
