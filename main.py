from typing import Dict, List, Tuple
import random

"""
Map: for dimension K=3 we have intuitive court label
NW    N    NE

W     C    E

SW    S    SE

the index of the map with dimension K=3
6     7     8

3     4     5

0     1      2


Hence when not at the outside border,
if one move, the index will change the following way:
the dimension is K ( 3 in the above graph)
move  E +1
move  W -1
move  N +K
move  S -K

Also it means coordinates x and y has a one to one relationship to index
    x + K*y = index
    y = int(index/K)
    x = index%K

"""

#########  Constants and Data #############
# The dimension of the map need to be an odd number so we can have a balanced center court
MAP_DIMENSION = 3
INDEX_BOUND = MAP_DIMENSION * MAP_DIMENSION - 1
CENTER_COURT_INDEX = int(INDEX_BOUND / 2)

court_names = [
    "court SW",
    "court S",
    "court SE",
    "court W",
    "court C",
    "court E",
    "court Nw",
    "court N",
    "court NE",
]

court_descriptions = [
    "court SW: People are all dancing on the court",
    "court S: People are all dancing on the court",
    "court SE: An exhibition match is going on...",
    "court W",
    "The Host is playing Federer's 10 greatest matchs on the screen.",
    "court E",
    "court Nw",
    "court N",
    "court NE",
]

qa_for_federer = {
    "How old are you?": "41",
    "Is your forehand better?": "Yes"
}

qa_for_nadal = {
    "How old are you?": "36",
    "Is your forehand better?": "No"
}


#########  Constants and Data Ends #############


class Court:
    def __init__(self,
                 court_name: str,
                 index: int,
                 court_description: str
                 ):
        self.court_name = court_name
        self.index = index
        self.court_description = court_description

    def display(self):
        print(f"{self.court_name}\n{self.court_description}")

    def is_center_court(self) -> bool:
        return self.index == CENTER_COURT_INDEX


class Player:
    # class variable, upper case indicate it is constant
    POS_CHANGE: Dict[str, int] = {
        'E': 1,
        'W': -1,
        'N': 3,
        'S': -3
    }

    def __init__(self,
                 name: str,
                 courts: List[Court],
                 score: int = 0,
                 # default at center court, MAP_DIMENSION has to be odd number
                 current_index: int = CENTER_COURT_INDEX,
                 ):
        self._name = name
        self._courts = courts
        self._score = score
        self._current_index = current_index

    def _check_boundary(self, delta):
        # todo
        return True

    def move(self, direction: str) -> bool:
        index_delta = Player.POS_CHANGE.get(direction)
        if self._check_boundary(index_delta):
            self._current_index += index_delta
            return True
        else:
            return False

    def current_available_actions(self):
        pass

    def coordinate_x(self):
        return self._current_index % MAP_DIMENSION

    def coordinate_y(self):
        return int(self._current_index / MAP_DIMENSION)

    @property
    def score(self):
        return

    def add_point(self):
        self._score += 1

    def current_court(self) -> Court:
        return self._courts[self._current_index]


# Non-player character(NPC)
class Npc:
    def __init__(self,
                 name: str,
                 index: int,
                 q_a: Dict[str, str] = {}
                 ):
        self._name = name
        self._index = index
        self._q_a: Dict[str, str] = q_a
        self._found = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, value: int):
        if value > INDEX_BOUND or value < 0:
            print(f"Npc.index: index value {value} out of bound!")
        else:
            self._index = value

    def add_q_a(self,
                extra_q_a: Dict[str, str]):
        self._q_a.update(extra_q_a)

    def answer_question(self, question: str) -> str:
        return self._q_a.get(question.strip().lower(),
                             "Sorry I don't know the answer to that question./n")

    def get_radom_qa(self) -> Tuple:
        '''
        randomly get a question answer from this npc
        :return: a tuple of question answer. qa[0] is question aq[1] is the answer
        '''
        qa = random.choice(
            list(self._q_a.items())
        )
        return qa

    def display(self):
        print(f"{self._name} is here!")

    @property
    def found(self):
        return self._found

    @found.setter
    def found(self, value: bool):
        self._found = value

    def reset(self):
        self._index = random.randint(0, INDEX_BOUND)
        self._found = False


class Host:
    def __init__(self,
                 npcs: List[Npc]):
        self._npcs = npcs
        self._task_issued = False
        self._current_npc: Npc = None
        self._current_qa: Tuple = None

    def hint(self):
        if not self._task_issued:
            print("Host: You can 'Ask Task' to earn point.")
        elif not self._current_npc.found:
            print(f"Host: You need to find {self._current_npc.name} first.")
        else:
            print(f"Good job finding {self._current_npc.name}, "
                  f"Please type 'Answer task' if you like to start answering the question")

    def issue_task(self):
        self._current_npc = self._npcs[random.randint(0, len(npcs) - 1)]
        self._current_qa = self._current_npc.get_radom_qa()
        self._task_issued = True
        print(f"Please find {self._current_npc.name} and ask '{self._current_qa[0]}'")

    def check_answer(self, ans: str):
        if ans.strip().lower() == self._current_qa[1]:
            print("Congratulations! You just finished a task")
            self._task_issued = False
            return True
        else:
            print("Wrong answer!")
            return False


def display_court(court: Court, host: Host, list_of_npcs: List[Npc]):
    print("-----------------------------------------------------------------------------")
    court.display()
    for npc in list_of_npcs:
        if npc.index == court.index:
            npc.found = True
            npc.display()
    if court.is_center_court():
        host.hint()
    print("-----------------------------------------------------------------------------\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # how to use the class
    #  load the courts
    # this is a court_description list of 3 * 3

    # initialize courts map
    courts: List[Court] = []
    for idx in range(MAP_DIMENSION * MAP_DIMENSION):
        courts.append(
            Court(court_names[idx],
                  idx, court_descriptions[idx])
        )

    # load the NPCs
    # todo: randamize npc initial location
    npcs: List[Npc] = [
        Npc("Federer", 3, qa_for_federer),
        Npc("Nadal", 3, qa_for_nadal),
    ]

    host = Host(npcs)

    quit_the_game = False

    player_name = input("Welcome to Federer's retirement party, may I have your name please:.\n >>")
    player = Player(player_name, courts)
    display_court(player.current_court(), host, npcs)
    while not quit_the_game:
        action: str = input(">>")
        action = action.strip().upper()
        if action in ["Q", "QUIT"]:
            quit_the_game = True
        elif action in ["N", "S", "E", 'W']:
            player.move(action)
            display_court(player.current_court(), host, npcs)
        elif action == "ASK TASK":
            if player.current_court().is_center_court():
                host.issue_task()
            else:
                print("You can 'ask task' from host at center court")
        elif action == "ANSWER TASK":
            ans = input("Host: what is your answer")
            if host.check_answer(ans):
                player.add_point()
