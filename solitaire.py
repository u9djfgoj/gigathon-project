import random
import os
from enum import Enum

class Color(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    SPADES = "♠"
    CLUBS = "♣"

class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color
        self.visible = False
    
    def __str__(self):
        if not self.visible:
            return "[X]"
        return f"{self.value}{self.color.value}"
    
    def is_red(self):
        return self.color in [Color.HEARTS, Color.DIAMONDS]
    
    def is_black(self):
        return not self.is_red()
    
    def can_stack_on(self, other):
        if other is None:
            return self.value == "K"
        return (self.is_red() != other.is_red()) and self.is_next_value(other.value)
    
    def is_next_value(self, other_value):
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        current_index = values.index(self.value)
        other_index = values.index(other_value)
        return current_index + 1 == other_index
    
    def can_move_to_foundation(self, foundation_card):
        if foundation_card is None:
            return self.value == "A"
        return self.color == foundation_card.color and self.is_next_value(foundation_card.value)

class Deck:
    def __init__(self):
        self.cards = []
        self.create_deck()
        self.shuffle()
    
    def create_deck(self):
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        colors = [Color.HEARTS, Color.DIAMONDS, Color.SPADES, Color.CLUBS]
        
        for color in colors:
            for value in values:
                self.cards.append(Card(value, color))
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None

class Game:
    def __init__(self):
        self.deck = Deck()
        self.columns = [[] for _ in range(7)]
        self.foundations = {color: [] for color in Color}
        self.waste = []
        self.setup_game()
    
    def setup_game(self):
        # Setup columns
        for i in range(7):
            for j in range(i + 1):
                card = self.deck.deal()
                if j == i:  # Last card in column is visible
                    card.visible = True
                self.columns[i].append(card)
        
        # Remaining cards go to stock
        self.stock = self.deck.cards.copy()
        self.deck.cards.clear()
    
    def draw_from_stock(self):
        if len(self.stock) > 0:
            card = self.stock.pop()
            card.visible = True
            self.waste.append(card)
        else:
            # Move all waste back to stock
            self.stock = self.waste[::-1]
            self.waste = []
            for card in self.stock:
                card.visible = False
    
    def move_card(self, from_col, card_index, to_col):
        if from_col == "waste" and to_col in range(7):
            if len(self.waste) == 0:
                return False
            
            card = self.waste[-1]
            target_col = self.columns[to_col]
            
            if len(target_col) == 0 and card.value != "K":
                return False
            
            if len(target_col) > 0:
                top_card = target_col[-1]
                if not card.can_stack_on(top_card):
                    return False
            
            self.waste.pop()
            card.visible = True
            target_col.append(card)
            return True
        
        elif from_col in range(7) and to_col in range(7):
            source_col = self.columns[from_col]
            
            if card_index >= len(source_col) or not source_col[card_index].visible:
                return False
            
            cards_to_move = source_col[card_index:]
            target_col = self.columns[to_col]
            
            if len(target_col) == 0:
                if cards_to_move[0].value != "K":
                    return False
            else:
                top_card = target_col[-1]
                if not cards_to_move[0].can_stack_on(top_card):
                    return False
            
            self.columns[from_col] = source_col[:card_index]
            self.columns[to_col].extend(cards_to_move)
            
            # Reveal the next card if available
            if len(self.columns[from_col]) > 0:
                self.columns[from_col][-1].visible = True
            
            return True
        
        return False
    
    def move_to_foundation(self, from_col, card_index):
        if from_col == "waste":
            if len(self.waste) == 0:
                return False
            
            card = self.waste[-1]
            foundation = self.foundations[card.color]
            
            if len(foundation) == 0:
                if card.value != "A":
                    return False
            else:
                top_card = foundation[-1]
                if not card.can_move_to_foundation(top_card):
                    return False
            
            self.waste.pop()
            foundation.append(card)
            return True
        
        elif from_col in range(7):
            source_col = self.columns[from_col]
            
            if card_index >= len(source_col):
                return False
            
            card = source_col[card_index]
            foundation = self.foundations[card.color]
            
            if len(foundation) == 0:
                if card.value != "A":
                    return False
            else:
                top_card = foundation[-1]
                if not card.can_move_to_foundation(top_card):
                    return False
            
            source_col.pop(card_index)
            foundation.append(card)
            
            # Reveal the next card if available
            if len(source_col) > 0:
                source_col[-1].visible = True
            
            return True
        
        return False
    
    def is_won(self):
        for foundation in self.foundations.values():
            if len(foundation) != 13:
                return False
        return True
    
    def display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== PASJANS ===")
        
        # Display foundations
        print("\nFundacje:")
        for color, foundation in self.foundations.items():
            if len(foundation) > 0:
                print(f"{foundation[-1]}", end=" ")
            else:
                print(f"[{color.value}]", end=" ")
        print("\n")
        
        # Display waste and stock
        print("Stock:", f"[{len(self.stock)}]", end="  ")
        print("Waste:", end=" ")
        if len(self.waste) > 0:
            print(self.waste[-1], end=" ")
        print("\n")
        
        # Display columns
        max_col_length = max(len(col) for col in self.columns)
        print("Kolumny:")
        print("  0     1     2     3     4     5     6")
        print("----------------------------------------")
        
        for i in range(max_col_length):
            for col in self.columns:
                if i < len(col):
                    print(f"{col[i]}", end="  ")
                else:
                    print("     ", end=" ")
            print()
        
        print("\n")

def main():
    game = Game()
    
    while True:
        game.display()
        
        if game.is_won():
            print("Gratulacje! Wygrałeś pasjansa!")
            break
        
        print("Dostępne komendy:")
        print("  d - dobierz kartę ze stocku")
        print("  m [from] [card_index] [to] - przenieś kartę między kolumnami")
        print("  f [from] [card_index] - przenieś kartę do fundacji")
        print("  q - wyjście z gry")
        print("  n - nowa gra")
        
        command = input("\nWprowadź komendę: ").strip().lower().split()
        
        if not command:
            continue
        
        if command[0] == "d":
            game.draw_from_stock()
        
        elif command[0] == "m" and len(command) == 4:
            try:
                from_col = command[1]
                card_index = int(command[2])
                to_col = int(command[3])
                
                if from_col == "waste":
                    success = game.move_card("waste", 0, to_col)
                else:
                    from_col = int(from_col)
                    success = game.move_card(from_col, card_index, to_col)
                
                if not success:
                    print("Nieprawidłowy ruch!")
                    input("Naciśnij Enter, aby kontynuować...")
            except (ValueError, IndexError):
                print("Nieprawidłowa komenda!")
                input("Naciśnij Enter, aby kontynuować...")
        
        elif command[0] == "f" and len(command) == 3:
            try:
                from_col = command[1]
                card_index = int(command[2])
                
                if from_col == "waste":
                    success = game.move_to_foundation("waste", 0)
                else:
                    from_col = int(from_col)
                    success = game.move_to_foundation(from_col, card_index)
                
                if not success:
                    print("Nie można przenieść karty do fundacji!")
                    input("Naciśnij Enter, aby kontynuować...")
            except (ValueError, IndexError):
                print("Nieprawidłowa komenda!")
                input("Naciśnij Enter, aby kontynuować...")
        
        elif command[0] == "q":
            print("Dziękujemy za grę!")
            break
        
        elif command[0] == "n":
            game = Game()
        
        else:
            print("Nieznana komenda!")
            input("Naciśnij Enter, aby kontynuować...")

if __name__ == "__main__":
    main()
