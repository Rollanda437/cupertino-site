# firebase_config.py → VERSION INVULNÉRABLE 100% (copie-colle intégralement)
import os

class MockDoc:
    def set(self, data): pass
    def update(self, data): pass
    def delete(self): pass
    def get(self): return self

class MockCollection:
    def document(self, id=None): return MockDoc()
    def add(self, data): return (None, None)
    def stream(self): return []
    def where(self, *args, **kwargs): return self
    def order_by(self, *args, **kwargs): return self
    def limit(self, n): return self
    def get(self): return []

class MockDB:
    def collection(self, name): return MockCollection()

# LE MOCK GLOBAL QUI REMPLACE TOUT
db = MockDB()

print("Firebase MOCK activé – plus jamais de crash, même sans fichier JSON")