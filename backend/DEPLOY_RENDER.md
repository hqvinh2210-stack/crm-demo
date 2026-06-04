Deploy hướng dẫn nhanh — Render (Docker)

Mục tiêu: đóng gói `backend` FastAPI vào Docker và deploy trên Render để có HTTPS public demo.

1) Chuẩn bị local (optional)
- Kiểm tra Dockerfile tại `backend/Dockerfile`. (Đã có sẵn.)
- Tạo file `.dockerignore` (đã tạo).

2) Build & run local (kiểm tra trước khi push)
- Build image (từ repo root):

```bash
# Build using backend directory as context
docker build -t crm-demo:local backend
# Run container
docker run --rm -p 8000:8000 crm-demo:local
```

- Mở http://localhost:8000 để kiểm tra.

3) Push lên GitHub
- Tạo repository mới trên GitHub và push toàn bộ project.

```bash
git init
git add .
git commit -m "Add CRM demo"
git branch -M main
# add origin then push
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```

4) Tạo Web Service trên Render
- Đăng nhập Render (https://render.com) và chọn "New" → "Web Service".
- Kết nối GitHub và chọn repo vừa push.
- Chọn "Docker" as the environment and set the build context to `backend` if your `Dockerfile` is inside `backend` (Render UI allows specifying Dockerfile path). Ensure port `8000` is used.
- Add environment variables:
  - `DATABASE_URL` — nếu bạn muốn dùng Postgres, tạo "Databases" → PostgreSQL trên Render và copy URL; nếu muốn SQLite demo, bạn có thể keep default but note: container filesystem is ephemeral.
- Click "Create Web Service". Render sẽ build image and provide public HTTPS URL.

5) Notes & Recommendations
- For a stable demo, use a managed PostgreSQL on Render and set `DATABASE_URL` env var.
- If you need persistent uploaded files, use object storage (S3) or a managed volume.
- Make sure to remove any sensitive credentials from the repository before pushing.

6) Optional: Add automatic deploy via GitHub Actions
- Render auto-deploys on push by default. No extra CI required unless you want running tests.

—
Nếu bạn muốn, tôi sẽ:
- A: Tạo `README.md` ở repo root với hướng dẫn ngắn (tôi có thể tạo file và cam kết vào repo). 
- B: Tạo mẫu `render.yaml` (Infrastructure as Code) cho Render (nếu bạn muốn quản lý config mã hóa).
- C: Tạo hướng dẫn đầy đủ để cấu hình Postgres trên Render và populate seed data.

Chọn A, B hoặc C hoặc yêu cầu tôi thực hiện toàn bộ deployment tự động (tôi sẽ chuẩn bị các file cần thiết và hướng dẫn tiếp theo).