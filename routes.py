from flask_restful import Api
from resources import *

api = Api()

api.add_resource(NewRephraseRequest, '/rephrase')
api.add_resource(NewSentenceCompletionRequest, '/sentence-complete')
api.add_resource(NewEssayOutlineRequest, '/essay-outline')
api.add_resource(AcceptedRephraseLogListResource, '/rephrase-logs/accepted')
api.add_resource(SentenceCompletionLogListResource, '/sentence-completion-logs/')
api.add_resource(AcceptedSentenceCompletionLogListResource, '/sentence-completion-logs/accepted') #Change 2: created an accepted request
api.add_resource(AcceptedEssayOutlineLogListResource, '/essay-outline-logs/accepted')
api.add_resource(RephraseLogListResource, '/rephrase-logs')
api.add_resource(RephraseLogResource, '/rephrase-logs/<int:request_id>')