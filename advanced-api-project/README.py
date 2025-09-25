# API endpoints
# GET /api/books/                 -> list books (public)
# GET /api/books/<int:pk>/        -> retrieve a book (public)
# POST /api/books/create/         -> create book (authenticated)
# PATCH/PUT /api/books/<pk>/update/ -> update book (authenticated)
# DELETE /api/books/<pk>/delete/  -> delete book (authenticated)

# Permissions:
# Read endpoints: public (AllowAny)
# Create/Update/Delete: authenticated only (IsAuthenticated)