# Energywut

This is live at [http://energywut.us](energywut.us).

This is a demo Django project that takes advantage of the [Open Government Initiative](https://www.whitehouse.gov/open) to show a clear picture of the fuel sources we rely on for generating energy. And if you're reading this, you're consuming some of that energy. `:)`

It's a very simple Django app that queries the [Energy Information Administration API](http://www.eia.gov/), and uses Redis to cache the results for speed.

Meaning to run it, you'll need to install and have Redis available.

The core of the business logic is in [lib.py](https://github.com/jar-o/django-eia/blob/master/app/lib.py) so you might want to check that out first to understand how it works.

Additionally, you'll need to do some setup, like set an `API_KEY`, a `REDIS_PASSWORD`, etc. For that look at the bottom section of [settings.py](https://github.com/jar-o/django-eia/blob/master/msite/settings.py)

Licensed under [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
