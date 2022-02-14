curl \
        -X POST \
        -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQzOTYxNDcwLCJpYXQiOjE2NDM5NTg0NzAsImp0aSI6ImEwNzA3ZWFiZjEzZTQzNWU4OGRiNWZiNmU0NzI1ZjVmIiwidXNlcl9pZCI6MzkzfQ.2cB2S79-rLj47b-LgIvzp_73s8WyKPWyJcNWPpymJmc" \
        -d '{"title": "Title by shell curl", "body": "Body by shell curl", "status": "published"}' \
        http://127.0.0.1:8000/en/blog/posts-list/
