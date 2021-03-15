from api import db,ma

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_created = db.Column(db.DateTime, auto_now_add=True)

    def __repr__(self):
        return '<User %r>' % self.username

class UserSchema(ma.Schema):
    class Meta:
        # fields to expose
        fields = ("email", "date_created", "_links")

    _links = ma.Hyperlinks(
        {
            "self": ma.URLFor("user_detail", values=dict(id="<id>")),
            "collection": ma.URLFor("users"),
        }
    )

user_schema = UserSchema()
users_schema = UserSchema(many=True)