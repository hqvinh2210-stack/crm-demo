import random
from datetime import datetime, timedelta

from passlib.context import CryptContext
from sqlalchemy import delete

from app.database import Base, SessionLocal, engine
from app.models.channel import Channel
from app.models.conversation import Conversation
from app.models.customer import Customer
from app.models.message import Message
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

STATUSES = [
    "New lead",
    "Contacted",
    "In negotiation",
    "Customer",
    "Dormant",
]

CHANNELS = [
    {"name": "Email", "provider": "email"},
    {"name": "Facebook Messenger", "provider": "messenger"},
    {"name": "Zalo", "provider": "zalo"},
]

NAMES = [
    "Nguyễn Văn An", "Trần Thị Bích", "Lê Minh Cường", "Phạm Thùy Dung", "Hoàng Quang Dũng",
    "Đỗ Thị Hạnh", "Vũ Văn Hùng", "Bùi Thanh Hòa", "Phan Quốc Khánh", "Ngô Mỹ Linh",
    "Lê Thị Mai", "Trương Anh Nam", "Đặng Phương Oanh", "Lê Văn Phúc", "Hà Thị Quỳnh",
    "Lưu Minh Sơn", "Tạ Thị Thu", "Nguyễn Thị Vân", "Lê Tuấn Vinh", "Phạm Anh Duy",
]

DOMAIN = ["example.com", "crm.vn", "market.io", "sales.co", "biz.vn"]

NOTES = [
    "Quan tâm dữ liệu khách hàng, cần demo nhanh.",
    "Đang chờ báo giá gói tích hợp CRM.",
    "Cần hỗ trợ kỹ thuật và training sử dụng.",
    "Yêu cầu API webhook cho nền tảng nội bộ.",
    "Mong muốn tự động hóa chăm sóc khách hàng.",
    "Đang tìm giải pháp quản lý tiếp thị.",
    "Đã từng dùng CRM nhưng muốn chuyển đổi.",
]

PRODUCT_LINES = ["CRM Platform", "B2B Market enterprise", "Enterprise Suite", "Visa analysis"]


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def build_customer(i: int) -> Customer:
    name = random.choice(NAMES)
    if i > len(NAMES):
        name = f"Khách hàng {i:04d}"
    email = f"customer{i}@{random.choice(DOMAIN)}"
    phone = f"09{random.randint(10000000, 99999999)}"
    status = random.choices(STATUSES, weights=[20, 20, 20, 25, 15], k=1)[0]
    notes = random.choice(NOTES)
    return Customer(name=name, email=email, phone=phone, status=status, notes=notes)


def build_message(conversation_id: int, sender_id: int | None, direction: str, content: str, created_at: datetime) -> Message:
    return Message(
        conversation_id=conversation_id,
        sender_id=sender_id,
        direction=direction,
        content=content,
        created_at=created_at,
    )


def seed_demo_data() -> None:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        db.execute(delete(Message))
        db.execute(delete(Conversation))
        db.execute(delete(Customer))
        db.execute(delete(Channel))
        db.execute(delete(User))
        db.commit()

        channels = [Channel(**item) for item in CHANNELS]
        db.add_all(channels)
        db.commit()

        users = [
            User(username="admin", full_name="Quản trị viên CRM", hashed_password=hash_password("admin123")),
            User(username="sales", full_name="Nhân viên Kinh doanh", hashed_password=hash_password("sales123")),
            User(username="support", full_name="Nhân viên Hỗ trợ", hashed_password=hash_password("support123")),
        ]
        db.add_all(users)
        db.commit()

        customers = [build_customer(i + 1) for i in range(1000)]
        db.add_all(customers)
        db.commit()

        conversations = []
        messages = []

        for idx, customer in enumerate(customers, start=1):
            if random.random() < 0.55:
                conversation_count = random.randint(1, 4)
                for j in range(conversation_count):
                    channel = random.choice(channels)
                    assigned_to = random.choice(users).id
                    subject = random.choice([
                        "Yêu cầu báo giá",
                        "Hỗ trợ kỹ thuật",
                        "Tư vấn giải pháp CRM",
                        "Đàm phán hợp đồng",
                        "Tích hợp hệ thống nội bộ",
                    ])
                    conversation = Conversation(
                        customer_id=customer.id,
                        channel_id=channel.id,
                        assigned_to=assigned_to,
                        subject=f"{subject} - {random.choice(['gói cơ bản', 'gói nâng cao', 'tích hợp API', 'workflow tự động'])}",
                    )
                    conversations.append(conversation)
        db.add_all(conversations)
        db.commit()

        for conversation in conversations:
            msg_count = random.randint(1, 5)
            last_time = datetime.utcnow() - timedelta(days=random.randint(0, 18), hours=random.randint(0, 23))
            for k in range(msg_count):
                direction = "inbound" if k % 2 == 0 else "outbound"
                sender_id = None if direction == "inbound" else random.choice(users).id
                content = random.choice([
                    "Xin chào, tôi muốn biết thêm về dịch vụ của bạn.",
                    "Vui lòng cung cấp báo giá và phạm vi hỗ trợ.",
                    "Hệ thống hiện tại của chúng tôi đang gặp vấn đề khi kết nối API.",
                    "Chúng tôi muốn dùng CRM để quản lý khách hàng doanh nghiệp.",
                    "Cần báo cáo chi tiết về hoạt động sales tháng này.",
                    "Yêu cầu cập nhật trạng thái đơn hàng và thông báo tự động.",
                ])
                messages.append(build_message(conversation.id, sender_id, direction, content, last_time))
                last_time += timedelta(hours=random.randint(1, 24))
        db.add_all(messages)
        db.commit()

        print("Da tao du lieu demo mo rong thanh cong.")
        print("- 1000 khach hang, nhieu conversation va tin nhan da san sang.")
        print("- Tai khoan: admin/admin123, sales/sales123, support/support123")
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
