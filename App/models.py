from App import db, app

class Block(db.Model):
    __tablename__='t_block'
    Fid=db.Column(db.Integer,primary_key=True)
    Fname=db.Column(db.String(128))
    Fhots=db.Column(db.String(128))

    @classmethod
    def addBlock(cls,name):
        try:
            block=Block(Fname=name)
            db.session.add(block)
            db.session.commit()
            return 0
        except:
            print('rolllback')
            db.session.rollback()
            return 1

    @classmethod
    def getBlocks(cls):
        return Block.query.all()

class Hot(db.Model):
    __tablename__='t_hot'
    Fid = db.Column(db.Integer, primary_key=True)
    Ftitle=db.Column(db.Text())
    Fcontent=db.Column(db.Text(),nullable=True)
    Furl=db.Column(db.Text())
    Fblock_id=db.Column(db.Integer)

    @classmethod
    def addHot(cls,block,title,content,url):
        try:
            b=Block.query.filter_by(name=block).first().id
            hot=Hot(Ftitle=title,Fcontent=content,Furl=url,Fblock_id=b)
            db.session.add(hot)
            db.session.commit()
            return 0
        except:
            print('rolllback')
            db.session.rollback()
            return 1


if __name__ == "__main__":
    with app.app_context():
        db.create_all()