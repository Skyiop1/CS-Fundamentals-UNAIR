<?php

namespace App\Http\Controllers;

use App\Models\Book;
use App\Models\Category;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\View\View;

class CatalogController extends Controller
{
    public function index(Request $request): View
    {
        $query = Book::with('category');

        // Search by Title, Author, or Book Code
        if ($request->filled('search')) {
            $search = $request->input('search');
            $query->where(function ($q) use ($search) {
                $q->where('title', 'like', "%{$search}%")
                  ->orWhere('author', 'like', "%{$search}%")
                  ->orWhere('book_code', 'like', "%{$search}%");
            });
        }

        // Filter by Category
        if ($request->filled('category_id')) {
            $query->where('category_id', $request->input('category_id'));
        }

        // Only show books with stock > -1 (or any books, but let's show all books with their stock status)
        $books = $query->latest()->paginate(9)->withQueryString();
        $categories = Category::orderBy('name')->get();

        return view('catalog.index', compact('books', 'categories'));
    }

    public function show(Book $book): View
    {
        $member = Auth::user()->member;
        $hasActiveBorrowing = false;

        if ($member) {
            $hasActiveBorrowing = $member->borrowings()
                ->whereHas('details', function ($q) use ($book) {
                    $q->where('book_id', $book->id);
                })
                ->whereIn('status', ['pending', 'approved', 'borrowed', 'late'])
                ->exists();
        }

        return view('catalog.show', compact('book', 'hasActiveBorrowing'));
    }
}
