import sublime
import sublime_plugin
import datetime


class Clock(object):
	CLOCK_STATUS_ID = "AA_CLOCK_STATUS"
	ACTIVE = False
	FORMAT = ""
	UPDATE_INTERVAL = 1000 

	@classmethod
	def start(cls):
		settings = sublime.load_settings('StatusBarClock.sublime-settings')
		
		if settings.get("alignment") == "right":
			CLOCK_STATUS_ID = "ZZ_CLOCK_STATUS"
		else:
			CLOCK_STATUS_ID = "AA_CLOCK_STATUS"

		cls.ACTIVE = settings.get("active")
		cls.FORMAT = settings.get("format")
		cls.UPDATE_INTERVAL = settings.get("updateInterval")

	@classmethod
	def stop(cls):
		for window in sublime.windows():
			try:
				window.active_view().erase_status(cls.CLOCK_STATUS_ID)
			except Exception as err:
				print(f"SublimeClock: {err}")

	@classmethod
	def update(cls):
		now = datetime.datetime.now()
		try:
			if cls.ACTIVE:
				sublime.set_timeout(cls.update, 1000)
				for window in sublime.windows():
					window.active_view().set_status(cls.CLOCK_STATUS_ID, now.strftime(cls.FORMAT))
			else:
				cls.stop()
		except Exception as err:
			print(f"SublimeClock: {err}")


def plugin_loaded():
	Clock.start()
	Clock.update()


def plugin_unloaded():
	Clock.stop()

