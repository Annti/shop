🧪 Zadanie rekrutacyjne 1: Logowanie użytkownika z JWT (FastAPI)

🎯 Cel:
Zaimplementuj endpoint logowania (POST /auth/login) z użyciem JWT. System zakłada istnienie mockowanej bazy użytkowników.

📋 Wymagania funkcjonalne:
Endpoint: POST /auth/login

Forma danych wejściowych: application/x-www-form-urlencoded (czyli OAuth2PasswordRequestForm)

username: adres e-mail użytkownika

password: hasło użytkownika

Walidacja danych użytkownika:

sprawdź, czy użytkownik istnieje,

sprawdź, czy hasło jest poprawne (użyj hashowania SHA256).

Jeśli dane poprawne:

zwróć token JWT (access_token) oraz token_type: bearer.

Token JWT powinien zawierać pole "sub" z user_id.

Jeśli dane niepoprawne:

zwróć 401 Unauthorized z komunikatem "Invalid email or password".

🔐 Założenia techniczne:
Użyj biblioteki jwt (pyjwt).

Sekrety JWT mogą być zapisane w zmiennych lub stałych (np. SECRET_KEY).

Nie musisz tworzyć bazy danych – mockowana baza w Pythonie jako słownik wystarczy.


fake_users_db = {
    "user@example.com": {
        "user_id": "abc123",
        "email": "user@example.com",
        "hashed_password": SHA256("password123"),  # użyj hashlib.sha256
        "full_name": "John Doe"
    }
}

✅ Przykład odpowiedzi (200 OK):

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}

❌ Przykład odpowiedzi (401):
{
  "detail": "Invalid email or password"
}
