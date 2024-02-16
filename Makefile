deploy:
	cd src && zip -vr ../dist.zip . -x "*.DS_Store" && cd ..
	yc serverless function version create\
		--function-name=uunit-schedule\
		--runtime=python39\
		--entrypoint=main.handler\
		--memory=128M\
		--execution-timeout=3s\
		--source-path=./dist.zip
	rm -r dist.zip