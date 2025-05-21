# Pasjans

## Wymagania
- Python 3.6 lub nowszy

## Instalacja
1. Pobierz plik `solitaire.py`
2. Upewnij się, że masz zainstalowanego Pythona
3. Uruchom grę komendą: `python solitaire.py`, albo klickiem.

## Komendy
- `d` - dobierz kartę ze stocku
- `m [from] [card_index] [to]` - przenieś kartę między kolumnami
  - `from` - źródłowa kolumna (0-6) lub "waste"
  - `card_index` - indeks karty w kolumnie (licząc od 0)
  - `to` - docelowa kolumna (0-6)
- `f [from] [card_index]` - przenieś kartę do fundacji
  - `from` - źródłowa kolumna (0-6) lub "waste"
  - `card_index` - indeks karty w kolumnie (licząc od 0)
- `q` - wyjście z gry
- `n` - nowa gra

## Architektura projektu

### Klasy

1. **Color (Enum)**
   - Reprezentuje kolory kart (kier, karo, pik, trefl)

2. **Card**
   - Reprezentuje pojedynczą kartę
   - Atrybuty:
     - `value` - wartość karty (A, 2-10, J, Q, K)
     - `color` - kolor karty
     - `visible` - czy karta jest widoczna
   - Metody:
     - `is_red()`, `is_black()` - sprawdza kolor karty
     - `can_stack_on()` - sprawdza czy kartę można położyć na inną
     - `can_move_to_foundation()` - sprawdza czy kartę można przenieść do fundacji

3. **Deck**
   - Reprezentuje talię kart
   - Metody:
     - `create_deck()` - tworzy standardową talię 52 kart
     - `shuffle()` - tasuje karty
     - `deal()` - rozdaje kartę z talii

4. **Game**
   - Główna klasa gry
   - Atrybuty:
     - `deck` - talia kart
     - `columns` - 7 kolumn gry
     - `foundations` - 4 stosy fundacyjne
     - `waste` - stos kart odrzuconych
     - `stock` - stos kart do dobrania
   - Metody:
     - `setup_game()` - przygotowuje początkowy układ gry
     - `draw_from_stock()` - dobiera kartę ze stocku
     - `move_card()` - przenosi kartę między kolumnami
     - `move_to_foundation()` - przenosi kartę do fundacji
     - `is_won()` - sprawdza czy gra została wygrana
     - `display()` - wyświetla aktualny stan gry

### Funkcja main()
- Inicjalizuje grę
- Obsługuje pętlę główną gry
- Interpretuje komendy gracza

## Zasady gry
1. Cel: Uporządkować wszystkie karty w fundacjach według koloru od Asa do Króla
2. Karty w kolumnach muszą być ułożone naprzemiennie kolorami w kolejności malejącej
3. Tylko ostatnia karta w każdej kolumnie jest widoczna
4. Król może być przeniesiony na puste miejsce kolumny
5. Karty można przenosić do fundacji tylko w kolejności od Asa do Króla
