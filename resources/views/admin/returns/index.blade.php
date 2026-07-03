@extends('layouts.admin')

@section('title', 'Proses Pengembalian')
@section('page_title', 'Kelola Pengembalian Buku')

@section('content')
    <div class="row g-4 mb-4">
        <!-- Buku Aktif Dipinjam -->
        <div class="col-12">
            <div class="card app-card shadow-sm border-0">
                <div class="card-header bg-white py-3 border-bottom">
                    <h5 class="card-title mb-0 fw-bold text-dark">Buku Sedang Aktif Dipinjam</h5>
                    <p class="text-secondary small mb-0">Klik tombol "Proses Kembali" untuk memproses pengembalian buku dan kalkulasi denda keterlambatan secara otomatis.</p>
                </div>
                <div class="table-responsive">
                    <table class="table align-middle mb-0 table-hover">
                        <thead class="table-light text-secondary">
                            <tr>
                                <th style="width: 80px;" class="text-center">ID</th>
                                <th>Anggota</th>
                                <th>Buku yang Dipinjam</th>
                                <th>Tanggal Pinjam</th>
                                <th>Jatuh Tempo</th>
                                <th style="width: 120px;" class="text-center">Status</th>
                                <th style="width: 150px;" class="text-center">Aksi</th>
                            </tr>
                        </thead>
                        <tbody>
                            @forelse ($activeBorrowings as $borrowing)
                                <tr>
                                    <td class="text-center text-secondary small">#{{ $borrowing->id }}</td>
                                    <td>
                                        <div class="fw-semibold text-dark">{{ $borrowing->member?->name }}</div>
                                        <div class="text-secondary small">{{ $borrowing->member?->member_number }}</div>
                                    </td>
                                    <td>
                                        <div class="fw-bold text-dark text-truncate" style="max-width: 280px;">
                                            {{ $borrowing->details->first()?->book?->title ?? '-' }}
                                        </div>
                                        <div class="text-secondary small">Kode: {{ $borrowing->details->first()?->book?->book_code ?? '-' }}</div>
                                    </td>
                                    <td>
                                        <span class="small text-secondary">{{ $borrowing->borrowed_at?->format('d/m/Y') ?? '-' }}</span>
                                    </td>
                                    <td>
                                        <span class="small text-secondary fw-semibold {{ $borrowing->status === 'late' ? 'text-danger' : '' }}">
                                            {{ $borrowing->due_date?->format('d/m/Y') ?? '-' }}
                                        </span>
                                    </td>
                                    <td class="text-center">
                                        <span class="badge badge-status badge-{{ $borrowing->status }}">{{ ucfirst($borrowing->status) }}</span>
                                    </td>
                                    <td class="text-center">
                                        <button type="button" class="btn btn-sm btn-success btn-process-return" 
                                            data-bs-toggle="modal" 
                                            data-bs-target="#returnModal"
                                            data-action="{{ route('admin.returns.store', $borrowing) }}"
                                            data-member-name="{{ $borrowing->member?->name }}"
                                            data-book-title="{{ $borrowing->details->first()?->book?->title }}"
                                            data-borrowed-at="{{ $borrowing->borrowed_at?->format('Y-m-d') }}"
                                            data-due-date="{{ $borrowing->due_date?->format('Y-m-d') }}">
                                            Proses Kembali
                                        </button>
                                    </td>
                                </tr>
                            @empty
                                <tr>
                                    <td colspan="7" class="text-center text-secondary py-4">Tidak ada buku yang sedang dipinjam saat ini.</td>
                                </tr>
                            @endforelse
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Riwayat Pengembalian -->
        <div class="col-12">
            <div class="card app-card shadow-sm border-0">
                <div class="card-header bg-white py-3 border-bottom">
                    <h5 class="card-title mb-0 fw-bold text-dark">Riwayat Buku Kembali</h5>
                </div>
                <div class="table-responsive">
                    <table class="table align-middle mb-0">
                        <thead class="table-light text-secondary">
                            <tr>
                                <th style="width: 80px;" class="text-center">ID</th>
                                <th>Anggota</th>
                                <th>Buku</th>
                                <th>Tanggal Kembali</th>
                                <th>Kondisi Buku</th>
                                <th>Petugas</th>
                            </tr>
                        </thead>
                        <tbody>
                            @forelse ($returns as $ret)
                                <tr>
                                    <td class="text-center text-secondary small">#{{ $ret->id }}</td>
                                    <td>
                                        <div class="fw-semibold text-dark">{{ $ret->borrowing?->member?->name ?? 'Anggota Terhapus' }}</div>
                                        <div class="text-secondary small">{{ $ret->borrowing?->member?->member_number ?? '-' }}</div>
                                    </td>
                                    <td>
                                        <div class="fw-semibold text-dark">{{ $ret->borrowing?->details->first()?->book?->title ?? '-' }}</div>
                                    </td>
                                    <td>
                                        <span class="small text-secondary">{{ $ret->return_date?->format('d/m/Y') }}</span>
                                    </td>
                                    <td>
                                        <span class="small text-secondary">{{ $ret->condition_note ?: 'Baik' }}</span>
                                    </td>
                                    <td>
                                        <span class="small text-secondary">{{ $ret->processedBy?->name ?: '-' }}</span>
                                    </td>
                                </tr>
                            @empty
                                <tr>
                                    <td colspan="6" class="text-center text-secondary py-4">Belum ada riwayat buku kembali.</td>
                                </tr>
                            @endforelse
                        </tbody>
                    </table>
                </div>
                @if ($returns->hasPages())
                    <div class="card-footer bg-white py-3">
                        {{ $returns->links('pagination::bootstrap-5') }}
                    </div>
                @endif
            </div>
        </div>
    </div>

    <!-- Modal Form Pengembalian -->
    <div class="modal fade" id="returnModal" tabindex="-1" aria-labelledby="returnModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <form id="returnForm" action="" method="POST">
                    @csrf
                    <div class="modal-header">
                        <h5 class="modal-title fw-bold" id="returnModalLabel">Proses Pengembalian Buku</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <!-- Ringkasan data -->
                        <div class="mb-3 p-3 bg-light rounded border small">
                            <div>Nama Anggota: <strong id="modalMemberName"></strong></div>
                            <div>Buku: <strong id="modalBookTitle"></strong></div>
                            <div>Tanggal Pinjam: <strong id="modalBorrowedAt"></strong></div>
                            <div>Batas Jatuh Tempo: <strong id="modalDueDate" class="text-danger"></strong></div>
                        </div>

                        <!-- Tanggal Pengembalian -->
                        <div class="mb-3">
                            <label for="return_date" class="form-label small fw-semibold text-secondary">Tanggal Kembali <span class="text-danger">*</span></label>
                            <input type="date" class="form-control" id="return_date" name="return_date" value="{{ date('Y-m-d') }}" required>
                            <small class="text-muted">Denda keterlambatan Rp 1.000 per hari akan dikalkulasi otomatis jika melebihi jatuh tempo.</small>
                        </div>

                        <!-- Kondisi Buku -->
                        <div class="mb-3">
                            <label for="condition_note" class="form-label small fw-semibold text-secondary">Catatan Kondisi Buku</label>
                            <textarea class="form-control" id="condition_note" name="condition_note" rows="3" placeholder="Contoh: Buku dikembalikan dalam keadaan baik dan bersih."></textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Batal</button>
                        <button type="submit" class="btn btn-success">Proses Pengembalian</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Script to populate modal values -->
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const buttons = document.querySelectorAll('.btn-process-return');
            buttons.forEach(button => {
                button.addEventListener('click', function () {
                    const action = this.getAttribute('data-action');
                    const memberName = this.getAttribute('data-member-name');
                    const bookTitle = this.getAttribute('data-book-title');
                    const borrowedAt = this.getAttribute('data-borrowed-at');
                    const dueDate = this.getAttribute('data-due-date');

                    // Set action form
                    document.getElementById('returnForm').setAttribute('action', action);

                    // Set labels
                    document.getElementById('modalMemberName').textContent = memberName;
                    document.getElementById('modalBookTitle').textContent = bookTitle;
                    
                    // Format dates
                    document.getElementById('modalBorrowedAt').textContent = formatDateStr(borrowedAt);
                    document.getElementById('modalDueDate').textContent = formatDateStr(dueDate);

                    // Set min attribute for return date inputs to prevent returning before borrowed_at
                    document.getElementById('return_date').setAttribute('min', borrowedAt);
                });
            });

            function formatDateStr(dateStr) {
                if (!dateStr) return '-';
                const parts = dateStr.split('-');
                if (parts.length === 3) {
                    return parts[2] + '/' + parts[1] + '/' + parts[0];
                }
                return dateStr;
            }
        });
    </script>
@endsection
