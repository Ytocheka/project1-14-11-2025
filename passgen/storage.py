import json
import os
from typing import Dict, List, Optional
from .utils import hash_password, verify_password


class PasswordStorage:
    def __init__(self, storage_file: str = "passwords.json"):
        self.storage_file = storage_file
        self.data = self._load_data()

    def _load_data(self) -> Dict:
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, Exception):
                return {"passwords": {}}
        return {"passwords": {}}

    def _save_data(self) -> None:
        with open(self.storage_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def store_password(self, service: str, username: str, password: str,
                       master_password: str) -> bool:


        # Проверяем мастер-пароль
        if "master_hash" not in self.data:
            # Первое использование - сохраняем мастер-пароль
            self.data["master_hash"] = hash_password(master_password)
        else:
            if not verify_password(master_password, self.data["master_hash"]):
                return False

        # Хэшируем пароль перед сохранением
        password_hash = hash_password(password)

        if "passwords" not in self.data:
            self.data["passwords"] = {}

        self.data["passwords"][service] = {
            "username": username,
            "password_hash": password_hash,
            "service": service
        }

        self._save_data()
        return True

    def retrieve_password_info(self, service: str, master_password: str) -> Optional[Dict]:
        if not verify_password(master_password, self.data.get("master_hash", "")):
            return None

        return self.data.get("passwords", {}).get(service)

    def list_services(self, master_password: str) -> List[str]:
        if not verify_password(master_password, self.data.get("master_hash", "")):
            return []

        return list(self.data.get("passwords", {}).keys())

    def search_passwords(self, query: str, master_password: str) -> List[Dict]:
        if not verify_password(master_password, self.data.get("master_hash", "")):
            return []

        results = []
        for service, info in self.data.get("passwords", {}).items():
            if query.lower() in service.lower():
                results.append({
                    "service": service,
                    "username": info["username"]
                })

        return results
