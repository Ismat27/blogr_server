from flaskr import create_app
from config import DevelopmentConfig, TestingConfig, ProductionConfig

app = create_app(ProductionConfig)

if __name__ == '__main__':
    app.run()
