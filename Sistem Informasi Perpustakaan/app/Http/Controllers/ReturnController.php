<?php

namespace App\Http\Controllers;

use App\Models\BookReturn;
use App\Models\Borrowing;
use App\Models\Fine;
use Carbon\Carbon;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\DB;
use Illuminate\View\View;

class ReturnController extends Controller
{
    /**
     * ADMIN: Show active borrowings list and return history.
     */
    public function index(): View
    {
        // Active borrowings ready to be returned
        $activeBorrowings = Borrowing::with(['member', 'details.book'])
            ->whereIn('status', ['borrowed', 'late'])
            ->latest()
            ->get();

        // Processed returns list
        $returns = BookReturn::with(['borrowing.member', 'borrowing.details.book', 'processedBy'])
            ->latest()
            ->paginate(10);

        return view('admin.returns.index', compact('activeBorrowings', 'returns'));
    }

    /**
     * ADMIN: Process return for a borrowing transaction.
     */
    public function store(Request $request, Borrowing $borrowing): RedirectResponse
    {
        if (!in_array($borrowing->status, ['borrowed', 'late'])) {
            return back()->with('error', 'Hanya buku yang sedang dipinjam yang dapat dikembalikan.');
        }

        $validated = $request->validate([
            'return_date' => ['required', 'date', 'after_or_equal:' . $borrowing->borrowed_at->format('Y-m-d')],
            'condition_note' => ['nullable', 'string', 'max:1000'],
        ], [
            'return_date.required' => 'Tanggal pengembalian wajib diisi.',
            'return_date.after_or_equal' => 'Tanggal pengembalian tidak boleh sebelum tanggal pinjam.',
        ]);

        $returnDate = Carbon::parse($validated['return_date']);
        $dueDate = $borrowing->due_date;

        // Calculate late days
        $lateDays = 0;
        if ($returnDate->greaterThan($dueDate)) {
            $lateDays = $returnDate->diffInDays($dueDate);
        }
        $fineAmount = $lateDays * 1000;

        try {
            DB::transaction(function () use ($borrowing, $returnDate, $validated, $lateDays, $fineAmount) {
                // 1. Create return record
                BookReturn::create([
                    'borrowing_id' => $borrowing->id,
                    'return_date' => $returnDate,
                    'condition_note' => $validated['condition_note'] ?? null,
                    'processed_by' => Auth::id(),
                ]);

                // 2. Create fine if late
                if ($lateDays > 0) {
                    Fine::create([
                        'borrowing_id' => $borrowing->id,
                        'late_days' => $lateDays,
                        'amount' => $fineAmount,
                        'status' => 'unpaid',
                    ]);
                }

                // 3. Update borrowing record
                $borrowing->update([
                    'status' => 'returned',
                    'returned_at' => $returnDate,
                ]);

                // 4. Increment stock of each borrowed book
                foreach ($borrowing->details as $detail) {
                    $detail->book->increment('stock');
                }
            });

            $successMsg = 'Buku berhasil dikembalikan.';
            if ($lateDays > 0) {
                $successMsg .= ' Terlambat ' . $lateDays . ' hari. Denda otomatis dibuat sebesar Rp ' . number_format($fineAmount, 0, ',', '.') . '.';
            }

            return redirect()->route('admin.returns.index')->with('success', $successMsg);
        } catch (\Exception $e) {
            return back()->with('error', 'Terjadi kesalahan saat memproses pengembalian: ' . $e->getMessage());
        }
    }
}
