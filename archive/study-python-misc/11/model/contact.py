# C:\Users\leon\PycharmProjects\studyPython\13\model\contact.py
class Contact:
    def __init__(self, id, name, phone, comment):
        self.id = id
        self.name = name.strip()
        self.phone = phone.strip()
        self.comment = comment.strip()

    def to_dict(self):
        """Преобразование контакта в словарь для JSON"""
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "comment": self.comment
        }

    @classmethod
    def from_dict(cls, data):
        """Создание контакта из словаря"""
        return cls(
            id=data["id"],
            name=data["name"],
            phone=data["phone"],
            comment=data["comment"]
        )

    def __str__(self):
        return f"ID: {self.id}, Имя: {self.name}, Телефон: {self.phone}, Комментарий: {self.comment}"