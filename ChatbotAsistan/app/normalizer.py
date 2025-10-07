import re
import unicodedata

def tr_lower(s: str) -> str:
    # Türkçe küçük harf dönüşümü: İ->i, I->ı
    s = s.replace("İ", "i").replace("I", "ı")
    return s.lower()

def remove_diacritics(s: str) -> str:
    # Unicode NFD sonra işaretleri at
    nfkd = unicodedata.normalize("NFD", s)
    return "".join(ch for ch in nfkd if unicodedata.category(ch) != "Mn")

def tr_normalize(s: str) -> str:
    s = tr_lower(s)
    s = remove_diacritics(s)
    s = re.sub(r"\s+", " ", s).strip()
    return s
