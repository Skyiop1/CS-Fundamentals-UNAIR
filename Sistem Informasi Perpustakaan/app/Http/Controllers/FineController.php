<?php

namespace App\Http\Controllers;

use App\Models\Fine;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\View\View;

class FineController extends Controller
{
    /**
     * ADMIN: View list of all fines in the library.
     */
    public function index(Request $request): View
    {
        $query = Fine::with(['borrowing.member', 'borrowing.details.book']);

        if ($request->filled('status')) {
            $query->where('status', $request->input('status'));
        }

        if ($request->filled('search')) {
            $search = $request->input('search');
            $query->whereHas('borrowing.member', function ($q) use ($search) {
                $q->where('name', 'like', "%{$search}%")
                  ->orWhere('member_number', 'like', "%{$search}%");
            });
        }

        $fines = $query->latest()->paginate(15)->withQueryString();

        return view('admin.fines.index', compact('fines'));
    }

    /**
     * ADMIN: Mark fine as paid.
     */
    public function markPaid(Fine $fine): RedirectResponse
    {
        if ($fine->status === 'paid') {
            return back()->with('error', 'Denda ini sudah lunas.');
        }

        $fine->update([
            'status' => 'paid',
            'paid_at' => now(),
        ]);

        return back()->with('success', 'Denda berhasil ditandai lunas.');
    }
}
