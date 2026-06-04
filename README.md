# CRM Demo - Multi-Channel Customer Relationship Management

## Overview
**CRM Demo** là hệ thống quản lý khách hàng đa kênh được xây dựng bằng FastAPI nhằm hỗ trợ doanh nghiệp quản lý khách hàng, cuộc hội thoại và tương tác từ nhiều nền tảng khác nhau như Facebook, Instagram, Email và Zalo.

Hệ thống cung cấp giao diện Dashboard trực quan, quản lý khách hàng, quản lý cuộc trò chuyện theo thời gian thực và tích hợp AI hỗ trợ phản hồi khách hàng.

## Live Demo
Hệ thống hiện đã được triển khai trực tuyến, bạn có thể truy cập và trải nghiệm trực tiếp các tính năng tại:
https://crm-demo-14wn.onrender.com/

> *Lưu ý: Vì dự án được deploy trên hạ tầng Render (gói Free), nếu bạn truy cập lần đầu sau một thời gian không có lượt tương tác, hệ thống sẽ mất khoảng 30s - 1 phút để khởi động lại dịch vụ (Cold Start).*

## Features

### Dashboard Analytics
* Tổng số khách hàng
* Tổng số cuộc hội thoại
* Thống kê khách hàng theo trạng thái
* Thống kê cuộc trò chuyện theo kênh
* Top khách hàng tương tác nhiều nhất
* Cuộc trò chuyện gần đây

### Customer Management
* Danh sách khách hàng
* Quản lý thông tin khách hàng
* Phân loại trạng thái khách hàng:
  * `New Lead`
  * `Contacted`
  * `In Negotiation`
  * `Customer`
  * `Dormant`

### Conversation Management
* Quản lý hội thoại đa kênh
* Theo dõi lịch sử trao đổi
* Gửi và nhận tin nhắn
* Hỗ trợ WebSocket realtime

### AI Integration
* Hỗ trợ AI Agent
* Tự động đề xuất phản hồi thông minh dựa trên ngữ cảnh cuộc hội thoại
* Hỗ trợ chăm sóc khách hàng tự động

### Multi-channel Support
* Facebook Messenger
* Instagram
* Email
* Zalo

## Technology Stack

### Backend
* FastAPI
* SQLAlchemy
* Pydantic
* WebSocket
* OpenAI API

### Database
* SQLite (Demo)
* PostgreSQL (Production)

### Authentication
* JWT Authentication
* Passlib

### Deployment
* Docker
* Render
* GitHub Actions

## Project Structure
```text
backend/
│
├── app/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── static/
│   ├── database.py
│   ├── config.py
│   ├── websocket.py
│   └── main.py
│
├── frontend/
│   └── index.html
│
├── seed_demo_data.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── crm.db
