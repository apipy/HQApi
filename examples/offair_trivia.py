from HQApi import HQApi
from HQApi.exceptions import ApiResponseError

token = "Token"
api = HQApi(token)

try:
    offair_id = api.start_offair()['gameUuid']
except ApiResponseError:
    offair_id = api.get_schedule()['offairTrivia']['games'][0]['gameUuid']
while True:
    offair = api.offair_trivia(offair_id)
    print("Question {0}/{1}".format(offair['question']['questionNumber'], offair['questionCount']))
    print(offair['question']['question'])
    for answer in offair['question']['answers']:
        print('{0}. {1}'.format(answer['answerId'], answer['text']))
    select = int(input('Select answer [1-3] > '))
    answer = api.send_offair_answer(offair_id, offair['question']['answers'][select - 1]['offairAnswerId'])
    print('You got it right: ' + str(answer['youGotItRight']))
    if answer['gameSummary']:
        print('Game ended')
        print('Earned:')
        print('Coins: ' + str(answer['gameSummary']['coinsEarned']))
        print('Points: ' + str(answer['gameSummary']['pointsEarned']))
        break
