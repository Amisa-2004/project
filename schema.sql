-- Create table pyqs.db to store the filenames in a sorted manner
CREATE TABLE pyqs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT NOT NULL,
    semester INTEGER NOT NULL CHECK (semester BETWEEN 1 AND 8),
    subject TEXT NOT NULL,
    exam TEXT NOT NULL CHECK(exam IN ('endsem', 'midsem')),
    year INTEGER NOT NULL CHECK(year >= 2000 AND year <= 2100),
    filename TEXT NOT NULL,
    verified INTEGER DEFAULT 0 CHECK(verified IN (0, 1))
);
