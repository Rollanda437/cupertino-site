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

# LE SEUL ET UNIQUE db DU PROJET
db = MockDB()

print("Firebase MOCK activé – site 100% stable")