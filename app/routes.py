from . import app
from flask import jsonify, request, url_for
from .entities.user import User, UserSchema
from .entities.opportunity import Opportunity, OpportunitySchema
from .entities.entity import Base, session
from .controller import Controller
from .utils.customEncoder import CustomEncoder
from .ql import qlschema, GraphQLView
from .api.user_api import user_api
from .api.profile_api import profile_api
from .api.opportunity_api import opportunity_api

app.debug = True

c = Controller(session)

app.json_encoder = CustomEncoder
app.register_blueprint(user_api, url_prefix='/api/user')
app.register_blueprint(profile_api, url_prefix='/api/profile')
app.register_blueprint(opportunity_api, url_prefix='/api/opportunity')

# create test user
initial_users = session.query(User).all()
if len(initial_users) == 0:
    test_user = User("test2", "script", "123")
    test_user.is_valid = True
    session.add(test_user)
    session.commit()
    session.close()


# public methods
@app.route('/')
def get_users():
    users_object = session.query(User).all()
    user_schema = UserSchema(many=True)
    users = user_schema.dump(users_object)
    session.close()
    return jsonify(users)


@app.route('/tag')
def list_tags():
    return jsonify(c.getTags())


@app.route("/tag/create/<name>")
def create_tag(name):
    id = c.createTag(name)
    return "Tag %s created with id %s" % (name, id)


@app.route("/test")
def test_action():
    opo_id = 1
    user_id = 1
    sch_id = c.createOpportunitySchedule(user_id, opo_id, "8:00", "16:30")
    return "Schedule created with id: %s" % sch_id
    db_sch = session.query(OpportunitySchedule).all()
    session.close()
    o_sch = OpportunityScheduleSchema(many=True)
    schedules = o_sch.dump(db_sch)

    return jsonify(schedules)


# GraphQL Interface

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=qlschema,
        graphiql=True  # for having the GraphiQL interface
    )
)
