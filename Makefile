install-config:
	mkdir -p ~/.local/share/kservices5/
	cp plasma-runner-Dict.desktop ~/.local/share/kservices5/
	mkdir -p ~/.config/KRS/
	cp Dict.py ~/.config/KRS/
	python3 ~/.config/KRS/Dict.py &
	kquitapp5 krunner; kstart5 krunner

create-autostart:
	# Configure the path in the .desktop file first
	mkdir -p ~/.config/autostart/
	cp Dict_autostart.desktop ~/.config/autostart/
