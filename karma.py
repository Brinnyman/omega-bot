import configparser
import os

path = os.path.dirname(os.path.abspath(__file__))
scores = path + '/points/scores.ini'


class Karma:

    def __init__(self):
        check_folder()
        check_file()

    def _process_scores(self, ctx, score_to_add):
        config = configparser.ConfigParser()
        config.read(scores)
        member_id = ctx.id

        sections = config.sections()
        for option in sections:
            if member_id == option:
                config.set('points', member_id, str(score_to_add))
                with open(scores, 'w') as config_file:
                    config.write(config_file)
            else:
                old_score = config.get('points', member_id)
                config.set('points', member_id, str(score_to_add + int(old_score)))
                with open(scores, 'w') as config_file:
                    config.write(config_file)

    # def _check_score(self, ctx):
    #     config = configparser.ConfigParser()
    #     config.read(scores)
    #     member_id = ctx.id

    #     sections = config.sections()
    #     for option in sections:
    #         if member_id == option:
    #             score = config.get('points', member_id)
    #             print(score)
    #             return score


def check_folder():
    if not os.path.exists("points"):
        print("Creating points folder...")
        os.makedirs("points")


def check_file():
    path = os.path.dirname(os.path.abspath(__file__))
    scores = path + '/points/scores.ini'
    if not os.path.exists(scores):
        print('Creating scores file...')
        config = configparser.ConfigParser()
        config.add_section('points')
        with open(scores, 'w') as config_file:
            config.write(config_file)
