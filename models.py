import random
from time import sleep

from django.db import models


# Create your models here.

class FlashCard(models.Model):
    pl = models.TextField(null=False, max_length=1000)
    eng = models.TextField(null=False, max_length=1000)

    def display_all(self):
        for card in list(FlashCard.objects.all()):
            print(str(card.id), card.pl, card.eng)

    def add_new_card(self, pl, eng):
        FlashCard.objects.create(pl=pl, eng=eng).save()

    def edit_card(self, card_id, pl=None, eng=None):
        card = FlashCard.objects.get(id=card_id)
        if pl:
            card.pl = pl
        if eng:
            card.eng = eng
        card.save()

    def remove_card(self, card_id):
        FlashCard.objects.get(id=card_id).delete()

    def print_pl(self):
        print(self.pl)

    def print_eng(self):
        print(self.eng)

    def get_front_depends_of_mode(self, mode):
        if mode == 'pl':
            return self.eng
        elif mode == 'eng':
            return self.pl

    def get_reverse_depends_of_mode(self, mode):
        if mode == 'pl':
            return self.pl
        elif mode == 'eng':
            return self.eng


class Ranking(models.Model):
    name = models.TextField(null=False, max_length=3)
    mode = models.TextField(null=False, max_length=3)
    score = models.IntegerField(null=False, default=0)
    lvl = models.TextField(null=False, max_length=6)


class GameMaster:
    error_counter = 0
    score = 0
    lvl_system = {
        'easy': 5,
        'medium': 3,
        'hard': 1,
    }

    def __init__(self, queue, lvl, mode):
        self.queue = queue
        self.lvl = lvl
        self.mode = mode

    def start_game_loop(self):
        while not self.check_if_end_game():
            print('Podaj odpowiedź')
            card: FlashCard = self.queue.pop()
            print(card.get_front_depends_of_mode(self.mode))
            print(self.cover_characters(card.get_reverse_depends_of_mode(self.mode)))
            answer = str(input()).strip()
            if card.get_reverse_depends_of_mode(self.mode) == answer:
                self.score += 1
                print('Dobra odpowiedź')
            else:
                self.error_counter += 1
                print('Zła odpowiedź!')
            print('Prawidłowa odpowiedź to:')
            print(card.get_reverse_depends_of_mode(self.mode))
            print('Wciśnij enter aby kontynuować')
            input()
        self.print_final_result()

    def print_final_result(self):
        print('Koniec Gry!!!')
        print('Podaj swój nick(3 znakowy) abym mógł ciebie umieścić w rankingu')
        name = str(input())
        Ranking.objects.create(name=name, mode=self.mode, score=self.score, lvl=self.lvl)

    def check_if_end_game(self):
        if self.error_counter >= self.lvl_system.get(self.lvl) or len(self.queue) == 0:
            return True
        return False

    def cover_characters(self, word):
        if len(word) < 5:
            return '_' * len(word)
        out = ''
        if self.lvl == 'easy':
            random_letters = random.sample(range(0, len(word)), int(len(word) * 1 / 3))
            for i, x in enumerate(word):
                if i in random_letters:
                    out += x
                else:
                    out += '_'
        if self.lvl == 'medium':
            out = '_' * len(word)
        if self.lvl == 'hard':
            out = ''
        return out


class MenuGame:
    def display_menu(self):
        print('1. Start Gry')
        print('2. Wyniki')
        print('3. Baza danych')
        print('4. Koniec gry')
        print('Proszę wybrać opcje')
        number = int(input())
        if number == 1:
            queue = list(FlashCard.objects.all())
            lvl = {
                1: 'easy',
                2: 'medium',
                3: 'hard'
            }
            mode = {
                1: 'pl',
                2: 'eng'
            }
            print('Wybierz poziom trudności')
            print('1. Easy')
            print('2. Medium')
            print('3. Hard')
            print('Proszę wybrać opcje')
            lvl_number = int(input())
            print('Wybierz w którą stronę zgadujesz')
            print('1. PL->ENG')
            print('2. ENG->PL')
            print('Proszę wybrać opcje')
            mode_number = int(input())
            gm = GameMaster(queue=queue, lvl=lvl.get(lvl_number), mode=mode.get(mode_number))
            return (1, gm)
        if number == 2:
            ranking = list(Ranking.objects.order_by('-score').all())
            print('Ranking: ')
            for r in ranking:
                print(r.name, str(r.score) + 'pkt', r.mode, r.lvl)
            return (2, None)
        if number == 3:
            flash_card = FlashCard()
            while True:
                print('Baza danych: ')
                print('1. Wyświetl')
                print('2. Dodaj')
                print('3. Edytuj')
                print('4. Usuń')
                print('5. Wróć')
                print('Proszę wybrać opcje')
                number = int(input())
                if number == 1:
                    flash_card.display_all()
                if number == 2:
                    print('Wpisz pl')
                    pl = str(input())
                    print('Wpisz eng')
                    eng = str(input())
                    flash_card.add_new_card(pl, eng)
                if number == 3:
                    print('Podaj ID karty')
                    pk = str(input())
                    print('Wpisz pl')
                    pl = str(input())
                    print('Wpisz eng')
                    eng = str(input())
                    flash_card.edit_card(pk, pl, eng)
                if number == 4:
                    print('Podaj ID karty')
                    pk = str(input())
                    flash_card.remove_card(pk)
                if number == 5:
                    return (3, None)
        if number == 4:
            return (4, None)
