from api import db, ma

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)
    day = db.Column(db.String(), nullable=False)
    reminder = db.Column(db.Boolean(), nullable=False)

    def __repr__(self):
        return '<Task %r>' % self.text

class TaskSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Task
        # fields to expose
        fields = ("id", "text", "day", "reminder")

    id = ma.auto_field()
    text = ma.auto_field()
    day = ma.auto_field()
    reminder = ma.auto_field()
    
    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("user_detail", values=dict(id="<id>")),
            "collection": ma.URLFor("users"),
        }
    )

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)