<?php

namespace App\Http\Controllers;

use App\Models\Book;
use App\Models\Borrowing;
use App\Models\BorrowingDetail;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class BorrowingController extends Controller
{
    /**
     * MEMBER: Submit a borrowing request.
     */
    public function request(Book $book): RedirectResponse
    {
        $member = Auth::user()->member;

        if (!$member) {
            return back()->with('error', 'Hanya anggota terdaftar yang dapat meminjam buku.');
        }

        if ($member->status !== 'active') {
            return back()->with('error', 'Status keanggotaan Anda tidak aktif. Silakan hubungi admin.');
        }

        // 1. Check book stock
        if ($book->stock <= 0) {
            return back()->with('error', 'Stok buku tidak tersedia saat ini.');
        }

        // 2. Check if member already has an active borrowing request for this book
        // Active statuses: pending, approved, borrowed, late
        $hasActive = $member->borrowings()
            ->whereHas('details', function ($q) use ($book) {
                $q->where('book_id', $book->id);
            })
            ->whereIn('status', ['pending', 'approved', 'borrowed', 'late'])
            ->exists();

        if ($hasActive) {
            return back()->with('error', 'Anda masih memiliki permintaan atau peminjaman aktif untuk buku ini.');
        }

        // 3. Create borrowing & detail records in a transaction
        DB::transaction(function () use ($member, $book) {
            $borrowing = Borrowing::create([
                'member_id' => $member->id,
                'status' => 'pending',
                'request_date' => now(),
            ]);

            BorrowingDetail::create([
                'borrowing_id' => $borrowing->id,
                'book_id' => $book->id,
                'quantity' => 1,
            ]);
        });

        return redirect()->route('borrowings.mine')->with('success', 'Permintaan peminjaman buku berhasil diajukan. Silakan tunggu persetujuan admin.');
    }

    /**
     * MEMBER: View list of my borrowings.
     */
    public function mine(Request $request): View
    {
        $member = Auth::user()->member;

        if (!$member) {
            return view('borrowings.mine', [
                'borrowings' => collect(),
            ])->with('error', 'Profil anggota tidak ditemukan.');
        }

        $query = $member->borrowings()->with(['details.book', 'fine']);

        if ($request->filled('status')) {
            $query->where('status', $request->input('status'));
        }

        $borrowings = $query->latest()->paginate(10)->withQueryString();

        return view('borrowings.mine', compact('borrowings'));
    }

    /**
     * MEMBER: View specific borrowing details.
     */
    public function showMine(Borrowing $borrowing): View
    {
        $member = Auth::user()->member;

        if (!$member || $borrowing->member_id !== $member->id) {
            abort(403, 'Anda tidak memiliki hak akses untuk melihat transaksi peminjaman ini.');
        }

        $borrowing->load(['details.book', 'fine', 'bookReturn']);

        return view('borrowings.show', compact('borrowing'));
    }

    /**
     * ADMIN: View all borrowings.
     */
    public function index(Request $request): View
    {
        $query = Borrowing::with(['member', 'details.book']);

        if ($request->filled('status')) {
            $query->where('status', $request->input('status'));
        }

        if ($request->filled('search')) {
            $search = $request->input('search');
            $query->whereHas('member', function ($q) use ($search) {
                $q->where('name', 'like', "%{$search}%")
                  ->orWhere('member_number', 'like', "%{$search}%");
            });
        }

        $borrowings = $query->latest()->paginate(15)->withQueryString();

        return view('admin.borrowings.index', compact('borrowings'));
    }

    /**
     * ADMIN: View specific borrowing details.
     */
    public function show(Borrowing $borrowing): View
    {
        $borrowing->load(['member', 'details.book', 'fine', 'bookReturn']);
        return view('admin.borrowings.show', compact('borrowing'));
    }

    /**
     * ADMIN: Approve a borrowing request.
     */
    public function approve(Borrowing $borrowing): RedirectResponse
    {
        if ($borrowing->status !== 'pending') {
            return back()->with('error', 'Hanya permintaan berstatus pending yang dapat disetujui.');
        }

        try {
            DB::transaction(function () use ($borrowing) {
                // Decrement stock for books with write lock
                foreach ($borrowing->details as $detail) {
                    $book = $detail->book()->lockForUpdate()->first();
                    if ($book->stock <= 0) {
                        throw new \Exception("Stok untuk buku '{$book->title}' sudah habis.");
                    }
                    $book->decrement('stock');
                }

                // Update status and dates
                $borrowing->update([
                    'status' => 'borrowed',
                    'approved_at' => now(),
                    'borrowed_at' => now(),
                    'due_date' => now()->addDays(7), // 7 days loan duration
                ]);
            });

            return back()->with('success', 'Permintaan peminjaman berhasil disetujui.');
        } catch (\Exception $e) {
            return back()->with('error', $e->getMessage());
        }
    }

    /**
     * ADMIN: Reject a borrowing request.
     */
    public function reject(Request $request, Borrowing $borrowing): RedirectResponse
    {
        if ($borrowing->status !== 'pending') {
            return back()->with('error', 'Hanya permintaan berstatus pending yang dapat ditolak.');
        }

        $validated = $request->validate([
            'rejected_reason' => ['required', 'string', 'max:255'],
        ], [
            'rejected_reason.required' => 'Alasan penolakan wajib diisi.',
        ]);

        $borrowing->update([
            'status' => 'rejected',
            'rejected_reason' => $validated['rejected_reason'],
        ]);

        return back()->with('success', 'Permintaan peminjaman berhasil ditolak.');
    }
}
