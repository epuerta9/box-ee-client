

.PHONY: upload

upload-config:
	mpremote cp config.json :config.json

upload-main:
	mpremote cp main.py :main.py

upload: upload-main upload-config
	mpremote fs cp -r lib/ :