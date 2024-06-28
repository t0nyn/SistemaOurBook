def update_book_status(self):
    if self.return_date is None:
        self.book_copy.status = "BORROWED"
    else:
        self.book_copy.status = "AVAILABLE"
