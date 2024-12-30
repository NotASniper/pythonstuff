from typing import Dict, List, Tuple

class Player:
    def __init__(self, name: str, timeZone: str, availability: Dict[str, List[Tuple[int, int]]]):
        """
        availability format:
        {
            "Mon": [(18, 22)],
            "Tue": [(20, 24)]
        }
        24hour format
        """
        self.name = name
        self.timeZone = timeZone
        self.availability = availability

    def __repr__(self):
        return f"Player({self.name}, TZ={self.timeZone})"


class MatchMaker:
    def __init__(self):
        self.players: List[Player] = []
        self.days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def addPlayer(self, player: Player):
        self.players.append(player)

    def findDayOverlaps(self, day: str) -> List[Tuple[int, int, List[Player]]]:
        """
        Returns a list of (start, end, [players]) showing intervals
        where players overlap on a given day.
        """
        intervalsWithPlayer = []
        for p in self.players:
            if day in p.availability:
                for interval in p.availability[day]:
                    intervalsWithPlayer.append((interval[0], interval[1], p))

        intervalsWithPlayer.sort(key=lambda x: x[0])

        dayOverlaps = []
        for startHour in range(0, 24):
            endHour = startHour + 1
            playersAvailable = []
            for (startI, endI, player) in intervalsWithPlayer:
                if startI <= startHour and endI >= endHour:
                    playersAvailable.append(player)
            if playersAvailable:
                dayOverlaps.append((startHour, endHour, playersAvailable))

        mergedOverlaps = []
        if dayOverlaps:
            currentStart, currentEnd, currentPlayers = dayOverlaps[0]
            for i in range(1, len(dayOverlaps)):
                sh, eh, pl = dayOverlaps[i]
                if pl == currentPlayers and sh == currentEnd:
                    currentEnd = eh
                else:
                    mergedOverlaps.append((currentStart, currentEnd, currentPlayers))
                    currentStart, currentEnd, currentPlayers = sh, eh, pl
            mergedOverlaps.append((currentStart, currentEnd, currentPlayers))

        return mergedOverlaps

    def matchGroups(self, groupSize: int = 4) -> Dict[str, List[Tuple[int, int, List[Player]]]]:
        """
        For each day, return all intervals in which at least `groupSize` players overlap.
        """
        results = {}
        for day in self.days:
            overlaps = self.findDayOverlaps(day)
            validSlots = []
            for (startI, endI, players) in overlaps:
                if len(players) >= groupSize:
                    validSlots.append((startI, endI, players))
            if validSlots:
                results[day] = validSlots
        return results


def createSamplePlayers() -> List[Player]:
    """
    Returns some sample players with time zones and availabilities.
    """
    players = []

    p1Availability = {
        "Mon": [(18, 22)],
        "Thu": [(19, 23)],
        "Sat": [(12, 18)]
    }
    p1 = Player("Player 1", "UTC-5", p1Availability)

    p2Availability = {
        "Mon": [(20, 24)],
        "Wed": [(18, 22)],
        "Sat": [(12, 14)]
    }
    p2 = Player("Player 2", "UTC-8", p2Availability)

    p3Availability = {
        "Mon": [(16, 21)],
        "Thu": [(18, 22)],
        "Sat": [(12, 18)]
    }
    p3 = Player("Player 3", "UTC-3", p3Availability)

    p4Availability = {
        "Mon": [(18, 20)],
        "Wed": [(20, 24)],
        "Sat": [(16, 20)]
    }
    p4 = Player("Player 4", "UTC+1", p4Availability)

    p5Availability = {
        "Thu": [(19, 23)],
        "Fri": [(18, 22)],
        "Sat": [(12, 18)]
    }
    p5 = Player("Player 5 ", "UTC", p5Availability)

    players.extend([p1, p2, p3, p4, p5])
    return players


def main():
    matchMaker = MatchMaker()
    samplePlayers = createSamplePlayers()

    for sp in samplePlayers:
        matchMaker.addPlayer(sp)

    groupSize = 3
    matchedGroups = matchMaker.matchGroups(groupSize=groupSize)

    print(f"Overlapping intervals with at least {groupSize} players:")

    dayScores = {}
    for day, intervals in matchedGroups.items():
        totalHours = sum((endI - startI) for (startI, endI, _) in intervals)
        dayScores[day] = totalHours

        print(f"\nDay: {day}")
        for (startI, endI, players) in intervals:
            playerNames = [p.name for p in players]
            print(f"  {startI:02d}:00 - {endI:02d}:00 --> {playerNames}")

    if dayScores:
        bestDay = max(dayScores, key=dayScores.get)
        print(f"\nThe best day to schedule (by total overlapping hours for {groupSize}+ players) is: {bestDay}")
    else:
        print("\nNo day has enough players at the same time.")


if __name__ == "__main__":
    main()
