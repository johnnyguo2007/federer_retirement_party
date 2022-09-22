from typing import Dict, List, Tuple
import random

"""
I'd like to use this game to celebrate Federer's retirement.

Player can move around this K * K map.
Player can "ask task" at center court and once completed the task the player will earn a point.
To complete the task you need to find the Non-player Character(npc) first.
After each around of task, the npc location is randomly reassigned. 

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
    "Center Court",
    "court E",
    "court Nw",
    "court N",
    "court NE",
]

court_descriptions = [
    "People are all dancing on the court",
    "People are all singing on the court",
    "An exhibition match is going on...",
    "People are enjoying the sunset view here",
    "The Host is playing Federer's 10 greatest matches on the screen.",
    "Ths place has a nice lake view",
    "a Lot of players are chatting here",
    "You can buy souvenir here...",
    "A beautiful court with green grass",
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
        self._index = index
        self.court_description = court_description

    @property
    def index(self):
        return self._index

    def display(self):
        print(f"{self.court_name}\n{self.court_description}")

    def coordinate_x(self):
        return self._index % MAP_DIMENSION

    def coordinate_y(self):
        return int(self._index / MAP_DIMENSION)

    def is_center_court(self) -> bool:
        return self._index == CENTER_COURT_INDEX

    def available_actions(self) -> List[str]:
        action_list = []
        if self.coordinate_x() > 0:
            action_list.append("W")
        if self.coordinate_x() < MAP_DIMENSION - 1:
            action_list.append("E")
        if self.coordinate_y() > 0:
            action_list.append("S")
        if self.coordinate_y() < MAP_DIMENSION - 1:
            action_list.append("N")
        return action_list


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

    @property
    def name(self):
        return self._name

    def move(self, direction: str) -> bool:
        if direction in self.current_court().available_actions():
            index_delta = Player.POS_CHANGE.get(direction)
            self._current_index += index_delta
            return True
        else:
            return False

    def current_available_actions(self):
        pass

    @property
    def score(self):
        return self._score

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
        self._q_a = {k.lower(): v for k, v in q_a.items()}
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

    def answer_question(self, question: str) -> bool:
        q = question.strip().lower()
        if q in self._q_a.keys():
            print(self._q_a.get(q))
            return True
        else:
            print("Sorry I don't know the answer to that question.")
            return False

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
        if self._found:
            print(f"{self._name} is smiling: You can type 'ask question' if you want to ask me any question.")

    @property
    def found(self):
        return self._found

    @found.setter
    def found(self, value: bool):
        self._found = value

    def reset(self):
        self._index = random.randint(0, INDEX_BOUND)
        # make sure npc does not show up in center court
        if self._index == CENTER_COURT_INDEX:
            self._index -= 1
        self._found = False

    def availabe_actions(self) -> List[str]:
        aa = []
        if self._found:
            aa.append("ask question")
            return aa


class Host:
    def __init__(self,
                 npcs: List[Npc]):
        self._npcs = npcs
        self._task_issued = False
        self._current_npc: Npc = None
        self._current_qa: Tuple = None

    @property
    def current_npc(self):
        return self._current_npc

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
        print(f"Please find {self._current_npc.name} and ask '{self._current_qa[0]}' "
              f"Please copy the question within the quotation mark")

    @property
    def task_issued(self) -> bool:
        return self._task_issued

    def check_answer(self, ans: str):
        if ans.strip().lower() == self._current_qa[1].lower():
            print("Congratulations! You just finished a task")
            self._task_issued = False
            self._current_npc.reset()
            return True
        else:
            print("Wrong answer!")
            return False

    def availabe_actions(self) -> List[str]:
        aa = []
        if self._task_issued:
            if self.current_npc is not None and self.current_npc.found:
                aa.append("Answer Task")
        else:
            aa.append("Ask Task")
        return aa


def display_court(court: Court, host: Host, list_of_npcs: List[Npc]):
    print("-----------------------------------------------------------------------------")
    court.display()
    if court.is_center_court():
        host.hint()
    else:
        for npc in list_of_npcs:
            if npc.index == court.index:
                if host.task_issued:
                    if host.current_npc.name == npc.name:
                        npc.found = True
                npc.display()


def show_available_action(court: Court, host: Host, list_of_npcs: List[Npc]):
    """
    Unlike display_court, show_available_action will never npc state
    :param court:
    :param host:
    :param list_of_npcs:
    :return:
    """
    available_actions: List[str] = []
    available_actions.extend(court.available_actions())
    if court.is_center_court():
        available_actions.extend(host.availabe_actions())
    else:
        for npc in list_of_npcs:
            if npc.index == court.index:
                if host.current_npc is not None:
                    if host.current_npc.name == npc.name:
                        if npc.availabe_actions() is not None:
                            available_actions.extend(npc.availabe_actions())
    print("-----------------------------------------------------------------------------")
    print(f"Available actions are:", end=' ')
    print(*available_actions, sep=", ")
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
        show_available_action(player.current_court(), host, npcs)
        action: str = input(f"You have {player.score} points>>")
        action = action.strip().upper()
        if action in ["Q", "QUIT"]:
            quit_the_game = True
            print(f"You have earned {player.score} points! Bye {player.name}")
            break
        elif action in ["N", "S", "E", 'W']:
            if not player.move(action):
                print(f"You can no longer move {action}")
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
        elif action == "ASK QUESTION":
            if player.current_court()._index == host.current_npc.index:
                question = input(f"{host.current_npc.name}: what is the question?\n>>")
                if host.current_npc.answer_question(question):
                    print("Please bring back the answer to host at center court")
                else:
                    print("Please make sure you copied the question correctly")

            else:
                print(f"You need to be at the same court as {host.current_npc.name} to ask question")

