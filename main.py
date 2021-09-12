from app import create_app
from config import DevelopmentConf

app = create_app(DevelopmentConf)

if __name__ == '__main__':
    app.run()
