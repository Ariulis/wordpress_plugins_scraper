import peewee

db = peewee.PostgresqlDatabase(
    database='wordpress_plugins',
    host='localhost',
    user='postgres',
    password='1'
)


class WordpressPluginDB(peewee.Model):
    title = peewee.CharField()
    link = peewee.CharField()
    rating = peewee.CharField()
    src = peewee.CharField()

    class Meta:
        database = db
