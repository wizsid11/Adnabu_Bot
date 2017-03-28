import logging
from logging.handlers import TimedRotatingFileHandler
from api_endpoint.views import app
import settings

if __name__ == '__main__':
    formatter = logging.Formatter("[%(asctime)s] [PROCESS - %(process)d THREAD - %(thread)d] "
                                  "{%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")

    handler = TimedRotatingFileHandler('logs/adnabubot.log', when='midnight', backupCount=10)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)

    app.run(debug=settings.DEBUG, host='0.0.0.0')