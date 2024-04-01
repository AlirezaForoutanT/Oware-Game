import json, copy, time


couleurs = {
    "rouge": '\33[31m',
    "bleu": '\33[34m',
    "vert": '\33[32m',
    "orange": '\033[33m',
    "transparent": '\33[90m'
}


def cprint(couleur: str, text: str):
    couleur = couleurs.get(couleur)
    return f"{couleur}{text}\33[37m"


class Joueur:
    def __init__(self, joueur: int, size: int, score: int = 0):
        self.joueur = joueur
        self.score = score
        self.cases = list(range(self.joueur-1, size, 2))

    def cases_jouables(self):
        return self.cases

    def possible_case(self, case: int):
        return case in self.cases

    def get_copy(self):
        return copy.deepcopy(self)


class Case:
    def __init__(self, numero: int, rouge: int, bleu: int, transparent: int):
        self.no = numero
        self.rouge = rouge
        self.bleu = bleu
        self.transparent = transparent

    def get_couleur(self, couleur: str):
        if couleur in ["rouge", "r"]:
            return self.rouge

        elif couleur in ["bleu", "b"]:
            return self.bleu

        elif couleur in ["tb", "tr"] or "transparent" in couleur:
            return self.transparent

    def is_empty_couleur(self, couleur: str):
        couleur =  self.get_couleur(couleur)
        return False if couleur else True

    def is_empty(self):
        return self.total() == 0

    def total(self):
        return self.rouge + self.bleu + self.transparent

    def empty(self):
        total =  self.total()
        self.rouge = 0
        self.bleu = 0
        self.transparent = 0
        return total

    def get_copy(self):
        return copy.deepcopy(self)


class Plateau:
    def __init__(self, size: int = 16):
        self.size = size
        self.cases = [Case(i, 2, 2, 1) for i in range(self.size)]
        self.joueurs = [Joueur(i, size) for i in range(1, 3)]
        self.current_joueur = 1


    def next_joueur(self):
        self.current_joueur = 2 if self.current_joueur == 1 else 1

    def traduire_couleur(self, couleur: str):
        couleur = couleur.lower()

        if couleur in ["r", "rouge"]:
            return "rouge"

        elif couleur in ["b", "bleu"]:
            return "bleu"

        elif couleur in ["tb", "transparent_bleu", "transparent bleu", "t_bleu", "t bleu"]:
            return "transparent_bleu"

        elif couleur in ["tr", "transparent_rouge", "transparent rouge", "t_rouge", "t rouge"]:
            return "transparent_rouge"

        return None

    def is_possible(self, case: Case, couleur: str, joueur: Joueur = None):
        joueur =  self.get_joueur(joueur)
        case =  self.get_case(case)
        couleur =  self.traduire_couleur(couleur)

        if not case or not joueur or not couleur:
            return False

        if not joueur.possible_case(case.no):
            return False

        if case.is_empty_couleur(couleur):
            return False

        return True

    def fini(self):
        j1 =  self.get_joueur(1)
        j2 =  self.get_joueur(2)

        if j1.score >= 41:
            return j1

        elif j2.score >= 41:
            return j2

        elif j1.score == 40 and j2.score == 40:
            return True

        graines =  self.get_graines_total()

        if self.affame(j1) and j1.joueur == self.current_joueur:
            j2.score += graines

            if j1.score > j2.score:
                return j1

            elif j1.score == j2.score:
                return True

            return j2

        elif self.affame(j2) and j2.joueur == self.current_joueur:
            j1.score += graines

            if j1.score > j2.score:
                return j1

            elif j1.score == j2.score:
                return True

            return j2

        if graines < 10:
            if j1.score > j2.score:
                return j1

            elif j1.score == j2.score:
                return True

            return j2

        return False

    def affame(self, joueur: int = None, cases: list = None):
        joueur =  self.get_joueur(joueur)

        if cases is None:
            cases =  self.get_cases()

        vide = 0

        for c in joueur.cases_jouables():
            case = cases[c]

            if case.is_empty():
                vide += 1

        return vide == self.size//2

    def calc_score(self, case: Case, couleur: str, joueur: Joueur = None):
        cases = [self.get_case(i).get_copy() for i in range(self.size)]

        joueur =  self.get_joueur(joueur)
        couleur =  self.traduire_couleur(couleur)

        autre_joueur = 2 if joueur.joueur == 1 else 1

        if isinstance(case, int):
            case = cases[case]

        current = case.no
        i = current + 1

        if "rouge" in couleur:
            while case.get_couleur(couleur) > 0:
                if i >= self.size:
                    i = 0

                if i == current:
                    i += 1

                    if i >= self.size:
                        i = 0

                    continue

                self.move_graine(case, cases[i], couleur)
                i += 1

        elif "bleu" in couleur:
            while case.get_couleur(couleur) > 0:
                if i == self.size:
                    i = 0

                elif i == self.size+1:
                    i = 1

                self.move_graine(case, cases[i], couleur)
                i += 2

            i -= 1

        i -= 1

        if i < 0:
            i = self.size - 1

        elif i >= self.size:
            i = 0

        last_case = cases[i]
        score = 0

        while last_case.total() in [2, 3]:
            score +=  last_case.empty()
            i -= 1

            if i < 0:
                i = self.size - 1

            last_case = cases[i]

        if self.affame(autre_joueur, cases):
            score =  self.get_graines_total()

        return score

    def jouer(self, case: Case, couleur: str, joueur: Joueur = None):
        joueur =  self.get_joueur(joueur)
        case =  self.get_case(case)
        couleur =  self.traduire_couleur(couleur)

        current = case.no
        i = current + 1

        if "rouge" in couleur:
            while case.get_couleur(couleur) > 0:
                if i >= self.size:
                    i = 0

                if i == current:
                    i += 1

                    if i >= self.size:
                        i = 0

                    continue
                self.move_graine(case, i, couleur)
                i += 1

        elif "bleu" in couleur:
            while case.get_couleur(couleur) > 0:
                if i == self.size:
                    i = 0

                elif i == self.size+1:
                    i = 1

                self.move_graine(case, i, couleur)
                i += 2
            i -= 1

        i -= 1

        if i < 0:
            i = self.size - 1

        elif i >= self.size:
            i = 0

        last_case =  self.get_case(i)
        score = 0

        while last_case.total() in [2, 3]:
            score +=  last_case.empty()
            i -= 1

            if i < 0:
                i = self.size - 1

            last_case =  self.get_case(i)

        joueur.score += score
        return score

    def traite_donnees(self, data):
        if isinstance(data, str):
            data = data.lower()

            if len(data) < 2:
                return

            if data[-2] == "t":
                couleur = data[-2:]
                case = data[:-2]
            else:
                couleur = data[-1]
                case = data[:-1]

        elif isinstance(data, dict):
            case = data.get("case")
            couleur = data.get("couleur")

        try:
            case = int(case)-1
        except ValueError:
            return None, None

        if couleur not in ["r", "b", "tr", "tb"] or case > self.size:
            return None, None

        return case, couleur

    def ask_entry(self):
        case = None
        couleur = None
        trans = None

        print(f"C'est au tour du joueur {self.current_joueur}")

        while True:
            while case == None:
                case = input("Entrez la case : ").lower()

                if "r" in case or "b" in case:
                    test =  self.traite_donnees(case)

                    if test is not None:
                        case, couleur = test[0], test[1]
                else:
                    try:
                        case = int(case)-1
                    except ValueError:
                        case = None
                        continue

                j =  self.get_joueur(self.current_joueur)

                if not j.possible_case(case):
                    case = None

            while couleur not in ["r", "b", "tr", "tb"]:
                couleur = input("Entrez la couleur (r/b/tr/tb) : ").lower()

            if not self.is_possible(case, couleur, self.current_joueur):
                case = None
                couleur = None
                continue

            break

        couleur =  self.traduire_couleur(couleur)
        return case, couleur, self.current_joueur

    def show_case(self, case: int):
        case =  self.get_case(case)
        return f" ({cprint('rouge', case.rouge)}, {cprint('bleu', case.bleu)}, {cprint('transparent', case.transparent)}) |"

    def show(self):
        print(f"Joueur 1 : {self.get_joueur(1).score}")
        print(f"Joueur 2 : {self.get_joueur(2).score}", "\n")
        text_j = "| "
        text = "|"
        reverse = False
        for i in range(0, self.size//2):
            text_j += f"  J{(i%2)+1} ({i+1})  |" + " " * (2-len(str(i+1)))
            text += self.show_case(i)

        print(text_j)
        print(text)
        print("")

        text_j = "|"
        text = "|"

        for i in range(self.size-1, (self.size//2)-1, -1):
            text_j += " "*(2-len(str(i+1))) + f"  J{(i%2)+1} ({i+1})  |"
            text += self.show_case(i)

        print(text_j)
        print(text)

    def get_playable_list(self, joueur: int = None):
        choix = []

        joueur =  self.get_joueur(joueur)

        for case in range(joueur.joueur-1, self.size, 2):
            for couleur in ["r", "b", "tr", "tb"]:
                if self.is_possible(case, couleur, joueur):
                    choix.append([case, couleur])

        return choix

    def get_joueur(self, joueur: int = None):
        try:
            joueur.joueur
            return joueur
        except Exception:
            pass

        if joueur is None:
            joueur = self.current_joueur

        try:
            return self.joueurs[joueur-1]
        except Exception:
            return None

    def get_autre_joueur(self, joueur: int = None):
        try:
            joueur = 2 if joueur.joueur == 1 else 1
        except Exception:
            pass

        if joueur is None:
            joueur = 2 if self.current_joueur == 1 else 1

        try:
            return self.joueurs[joueur-1]
        except Exception:
            return None

    def get_case(self, case: int):
        try:
            case.no
            return case
        except Exception:
            pass

        try:
            return self.cases[case]
        except Exception:
            return None

    def get_cases(self):
        if isinstance(self.cases, list):
            return self.cases

        elif isinstance(self.cases, dict):
            liste = [v for v in self.cases.values()]
            liste.sort(key = lambda row: row.no)
            return liste

    def get_graines_total(self):
        total = 0
        for case in self.get_cases():
            total += case.total()

        return total

    def get_cases_pleines(self):
        count = 0
        for case in self.get_cases():
            if case.total():
                count += 1

        return count

    def move_graine(self, case1: Case, case2: Case, couleur: str):
        case1 =  self.get_case(case1)
        case2 =  self.get_case(case2)
        couleur =  self.traduire_couleur(couleur)

        if "transparent" in couleur and not case1.is_empty_couleur("transparent"):
            case1.transparent -= 1
            case2.transparent += 1

        if "bleu" == couleur and not case1.is_empty_couleur("bleu"):
            case1.bleu -= 1
            case2.bleu += 1

        if "rouge" == couleur and not case1.is_empty_couleur("rouge"):
            case1.rouge -= 1
            case2.rouge += 1

    def get_copy(self):
        return copy.deepcopy(self)


def main():
    plateau = Plateau()
    coup = 0

    lock = True
    joue_contre = 1

    algoJ1 = None
    algoJ2 = None

    while True:
        plateau.show()
        print("\n")
        coup += 1

        coul = "vert"
        algo = ""
        f = 0
        profondeur = 0

        if plateau.current_joueur == 1:
            if joue_contre == 1 or lock:
                case, couleur, joueur =  plateau.ask_entry()
                score = 0

        elif plateau.current_joueur == 2:
            if joue_contre == 2 or lock:
                case, couleur, joueur =  plateau.ask_entry()
                score = 0


        print(cprint(coul, f"coup : {coup}  | joueur : {plateau.current_joueur} | profondeur : {profondeur} | case : {case+1}{couleur} | eval : {score} | points : {plateau.calc_score(case, couleur)}"))
        print(cprint(coul, f"cases : {plateau.get_cases_pleines()} | graines : {plateau.get_graines_total()} | algo : {algo} | temps : {f:.2f}"))

        plateau.jouer(case, couleur)
        plateau.next_joueur()
        fini =  plateau.fini()

        if fini:
            plateau.show()

            if fini == True:
                print("Egalite")

            else:
                print(f"Joueur {fini.joueur} a gagné! : {fini.score}")

            input("")
            plateau = Plateau()
            coup = 0

        print("")


if __name__ == "__main__":
    main()
