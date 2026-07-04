-- CreateTable
CREATE TABLE "BluRay" (
    "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "tmdbId" INTEGER,
    "title" TEXT NOT NULL,
    "originalTitle" TEXT,
    "year" INTEGER,
    "posterPath" TEXT,
    "backdropPath" TEXT,
    "overview" TEXT,
    "rating" REAL,
    "runtime" INTEGER,
    "genres" TEXT,
    "director" TEXT,
    "format" TEXT NOT NULL DEFAULT 'Blu-ray',
    "notes" TEXT,
    "createdAt" DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" DATETIME NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "BluRay_tmdbId_key" ON "BluRay"("tmdbId");
