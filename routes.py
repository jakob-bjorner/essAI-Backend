from flask_restful import Api
from resources import *

api = Api()

api.add_resource(NewRephraseRequest, '/rephrase')
api.add_resource(NewSentenceCompletionRequest, '/sentence-complete')
api.add_resource(NewEssayOutlineRequest, '/essay-outline')

api.add_resource(RephraseLogListResource, '/rephrase-logs/')
api.add_resource(AcceptedRephraseLogListResource, '/rephrase-logs/accepted')
api.add_resource(RejectedRephraseLogListResource, '/rephrase-logs/rejected')
api.add_resource(RephraseLogResource, '/rephrase-logs/<int:request_id>')

api.add_resource(SentenceCompletionLogListResource, '/sentence-completion-logs/')
api.add_resource(AcceptedSentenceCompletionLogListResource, '/sentence-completion-logs/accepted')
api.add_resource(RejectedSentenceCompletionLogListResource, '/sentence-completion-logs/rejected')
api.add_resource(SentenceCompletionLogResource, '/sentence-completion-logs/<int:request_id>')

api.add_resource(EssayOutlineLogListResource, '/essay-outline-logs/')
api.add_resource(AcceptedEssayOutlineLogListResource, '/essay-outline-logs/accepted')
api.add_resource(RejectedEssayOutlineLogListResource, '/essay-outline-logs/rejected')
api.add_resource(EssayOutlineLogResource, '/essay-outline-logs/<int:request_id>')