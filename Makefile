clean-all:
	rm database.db || true
	rm -rf flask_session || true
	rm -rf __pycache__  || true
	rm -rf web/flask_session || true
	rm -rf web/__pycache__  || true
