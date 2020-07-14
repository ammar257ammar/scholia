"""app."""


from __future__ import absolute_import, division, print_function

from flask import Flask
from flask_bootstrap import Bootstrap, StaticCDN

from flask_caching import Cache
from scholia.app.extensions import cache

from ..text import load_text_to_topic_q_text


def create_app(text_to_topic_q_text_enabled=True, third_parties_enabled=False):
    """Create webapp.

    Factory for webapp.

    Parameters
    ----------
    text_to_topic_q_text_enabled : bool
        Determines whether the text-to-topics functionality should be enabled.
        The loading of the matching model takes long time and it may be
        convenient during development to disable the functionality
        [default: true].
    third_parties_enabled : bool
        Determines whether third-party webservices can be enabled.
        Due to privacy reason this is disabled by default [default: false].

    Returns
    -------
    app : flask.app.Flask
        Flask app object.

    """
    
    config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "filesystem", # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 3600,
    "CACHE_DIR": "/cache"
    }
    app = Flask(__name__)
    
    app.config.from_mapping(config)
    
    cache.init_app(app, config)

    Bootstrap(app)

    # Serve assets from wmflabs for privacy reasons
    app.extensions['bootstrap']['cdns']['jquery'] = StaticCDN()
    app.extensions['bootstrap']['cdns']['bootstrap'] = StaticCDN()

    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.text_to_topic_q_text_enabled = text_to_topic_q_text_enabled
    if text_to_topic_q_text_enabled:
        app.text_to_topic_q_text = load_text_to_topic_q_text()

    app.third_parties_enabled = third_parties_enabled

    return app
